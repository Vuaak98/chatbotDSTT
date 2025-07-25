import logging
from typing import Dict, List, Optional, Tuple

from langchain_core.documents import Document

from ..config import get_settings
from .qdrant_connector import QdrantConnector
from .config.config import rag_settings
from .query_extractor import QueryMetadataExtractor

logger = logging.getLogger(__name__)

class RAGService:
    """
    Service cho Retrieval Augmented Generation (RAG)
    """
    
    def __init__(self, qdrant_connector: Optional[QdrantConnector] = None):
        """
        Khởi tạo RAG Service
        
        Args:
            qdrant_connector: QdrantConnector instance (tạo mới nếu không có)
        """
        self.settings = get_settings()
        self.rag_settings = rag_settings
        try:
            self.qdrant = qdrant_connector or QdrantConnector()
        except Exception as e:
            logger.error(f"Failed to initialize QdrantConnector: {str(e)}")
            self.qdrant = None
            logger.warning("RAG Service initialized without Qdrant connection. Fallback will be used.")
        
    def _extract_metadata_from_query(self, query: str) -> Dict:
        """
        Trích xuất metadata từ câu truy vấn để cải thiện tìm kiếm
        
        Args:
            query: Câu truy vấn người dùng
            
        Returns:
            Dict: Các bộ lọc phù hợp với truy vấn
        """
        try:
            extracted_metadata = QueryMetadataExtractor.extract_metadata(query)
            if extracted_metadata:
                logger.info(f"Extracted metadata from query: {extracted_metadata}")
            return extracted_metadata
        except Exception as e:
            logger.warning(f"Error extracting metadata from query: {str(e)}")
            return {}
    
    async def get_context(
        self, 
        query: str, 
        filter: Optional[Dict] = None,
        k: Optional[int] = None,
        use_query_metadata: bool = True
    ) -> Tuple[List[Document], bool]:
        """
        Lấy ngữ cảnh cho truy vấn từ vector database
        Bao gồm cơ chế fallback
        
        Args:
            query: Truy vấn người dùng
            filter: Bộ lọc metadata
            k: Số lượng documents lấy về
            use_query_metadata: Có trích xuất metadata từ câu truy vấn không
            
        Returns:
            Tuple[List[Document], bool]: (documents, success_flag)
            - documents: danh sách documents tìm được hoặc rỗng nếu lỗi
            - success_flag: True nếu retrieval thành công, False nếu fallback
        """
        # Kiểm tra nếu RAG bị tắt trong settings hoặc không có kết nối Qdrant
        if not self.settings.rag_enabled or self.qdrant is None:
            logger.info("RAG is disabled or Qdrant connection not available. Returning empty context.")
            return [], False
            
        try:
            k = k or self.rag_settings.top_k
            
            # Trích xuất và kết hợp metadata từ câu truy vấn (nếu được bật)
            combined_filter = filter or {}
            if use_query_metadata:
                extracted_filter = self._extract_metadata_from_query(query)
                if extracted_filter:
                    # Kết hợp filter đã có với filter trích xuất
                    for key, value in extracted_filter.items():
                        if key in combined_filter:
                            # Nếu cùng là list, merge chúng
                            if isinstance(combined_filter[key], list) and isinstance(value, list):
                                combined_filter[key].extend([v for v in value if v not in combined_filter[key]])
                            # Nếu không, ưu tiên giá trị đã tồn tại
                        else:
                            combined_filter[key] = value
            
            # Truy vấn với filter đã kết hợp (hoặc None nếu không có filter)
            search_filter = combined_filter if combined_filter else None
            documents = await self.qdrant.similarity_search(
                query=query, 
                k=k, 
                filter=search_filter
            )
            
            if not documents:
                logger.warning(f"No documents found for query: {query}")
                return [], False
                
            logger.info(f"Retrieved {len(documents)} documents for context")
            return documents, True
            
        except Exception as e:
            # Cơ chế fallback - ghi log lỗi nhưng không làm hỏng trải nghiệm người dùng
            error_type = type(e).__name__
            logger.error(f"Error retrieving context: {error_type} - {e}")
            
            # Log chi tiết hơn về lỗi filter
            if "validation error" in str(e).lower():
                logger.error(f"Filter validation error. Filter: {combined_filter}")
                # Thử lại mà không có filter
                try:
                    logger.info("Retrying search without filter")
                    documents = await self.qdrant.similarity_search(
                        query=query, 
                        k=k
                    )
                    if documents:
                        logger.info(f"Retry successful: found {len(documents)} documents")
                        return documents, True
                except Exception as retry_e:
                    logger.error(f"Retry also failed: {retry_e}")
            
            return [], False
    
    def format_context_for_prompt(self, documents: List[Document]) -> str:
        """
        Định dạng documents thành context cho prompt
        
        Args:
            documents: Danh sách Document objects
            
        Returns:
            String định dạng để thêm vào prompt
        """
        if not documents:
            return ""
            
        formatted_docs = []
        
        for i, doc in enumerate(documents):
            # Lấy thông tin nguồn từ metadata nếu có
            source = doc.metadata.get("source", "Unknown source")
            title = doc.metadata.get("title", "")
            doc_type = doc.metadata.get("type", "")
            
            # Format document với nguồn
            doc_content = f"[Document {i+1}]"
            if title:
                doc_content += f" {title}"
            if doc_type:
                doc_content += f" ({doc_type})"
            
            doc_content += f"\nSource: {source}\n\n{doc.page_content}\n"
            formatted_docs.append(doc_content)
            
        # Gộp tất cả thành một context string
        return "\n".join([
            "# Relevant Context for Question",
            "-" * 50,
            "\n\n".join(formatted_docs),
            "-" * 50,
        ])
    
    async def get_formatted_context(
        self, query: str, filter: Optional[Dict] = None, k: Optional[int] = None,
        use_query_metadata: bool = True
    ) -> Tuple[str, bool]:
        """
        Lấy và định dạng context cho query
        
        Args:
            query: Truy vấn người dùng
            filter: Bộ lọc metadata
            k: Số lượng documents lấy về
            use_query_metadata: Có trích xuất metadata từ câu truy vấn không
            
        Returns:
            Tuple[str, bool]: (formatted_context, success_flag)
            - formatted_context: Context đã định dạng hoặc rỗng nếu lỗi
            - success_flag: True nếu retrieval thành công, False nếu fallback
        """
        documents, success = await self.get_context(query, filter, k, use_query_metadata)
        if not success:
            return "", False
            
        return self.format_context_for_prompt(documents), True 
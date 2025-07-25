import logging
from typing import Dict, List, Optional, Union

from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, Filter, FieldCondition, MatchValue, MatchAny
from qdrant_client.http.exceptions import UnexpectedResponse

from .config.config import rag_settings
from ..config import OPENAI_API_KEY

logger = logging.getLogger(__name__)

class QdrantConnector:
    """
    Lớp kết nối với Qdrant Vector Database
    """
    
    def __init__(
        self,
        api_key: str = OPENAI_API_KEY,
        embedding_model: str = rag_settings.embedding_model_name,
        collection_name: str = rag_settings.qdrant_collection_name,
        url: str = rag_settings.qdrant_url,
        qdrant_api_key: Optional[str] = None
    ):
        """
        Khởi tạo kết nối Qdrant
        
        Args:
            api_key: OpenAI API key
            embedding_model: Tên model embedding
            collection_name: Tên collection trong Qdrant
            url: URL của Qdrant server
            qdrant_api_key: API key cho Qdrant Cloud (nếu có)
        """
        self.embedding_model_name = embedding_model
        self.collection_name = collection_name
        self.url = url
        
        # Khởi tạo embedding model
        self.embeddings = OpenAIEmbeddings(
            model=embedding_model,
            api_key=api_key
        )
        
        # Kết nối Qdrant client
        client_params = {"url": url, "prefer_grpc": False}
        
        # Lấy API key từ tham số hoặc rag_settings
        qdrant_api_key = qdrant_api_key or (
            rag_settings.qdrant_api_key.get_secret_value() 
            if rag_settings.qdrant_api_key.get_secret_value() 
            else None
        )
        
        if qdrant_api_key:
            client_params["api_key"] = qdrant_api_key
            logger.info("Using Qdrant API key from configuration")
        else:
            logger.warning("No Qdrant API key provided, this may cause authentication issues with Qdrant Cloud")
        
        try:
            self.client = QdrantClient(**client_params)
            logger.info(f"Connected to Qdrant at {url}")
        except Exception as e:
            logger.error(f"Error connecting to Qdrant: {e}")
            raise
        
        # Khởi tạo Vector Store (có xử lý lỗi)
        try:
            self.vector_store = self._init_vector_store()
        except Exception as e:
            logger.error(f"Error initializing vector store: {e}")
            # Vẫn lưu trữ self.client, nhưng vector_store sẽ là None
            self.vector_store = None
        
    def _init_vector_store(self) -> QdrantVectorStore:
        """
        Khởi tạo hoặc kết nối đến Vector Store.
        Tạo collection mới nếu chưa tồn tại.
        
        Returns:
            QdrantVectorStore object
        """
        try:
            # Kiểm tra collection có tồn tại chưa
            collections = self.client.get_collections().collections
            collection_names = [collection.name for collection in collections]
            
            # Tạo mới nếu chưa tồn tại
            if self.collection_name not in collection_names:
                logger.info(f"Creating new collection: {self.collection_name}")
                # Lấy kích thước vector từ model OpenAI
                if "text-embedding-3" in self.embedding_model_name:
                    vector_size = 1536  # text-embedding-3-small/large
                else:
                    vector_size = 1536  # Mặc định cho nhiều model khác
                    
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=vector_size, 
                        distance=Distance.COSINE
                    ),
                )
                logger.info(f"Collection {self.collection_name} created successfully")
            
            # Kết nối đến Vector Store - truyền embedding (số ít) trực tiếp vào constructor
            vector_store = QdrantVectorStore(
                client=self.client,
                collection_name=self.collection_name,
                embedding=self.embeddings,  # Sửa từ embeddings thành embedding
            )
            
            return vector_store
            
        except UnexpectedResponse as e:
            logger.error(f"Error initializing vector store - Unexpected response from Qdrant: {e}")
            # Log body if available
            if hasattr(e, 'body'):
                logger.error(f"Response body: {e.body}")
            raise
        except Exception as e:
            logger.error(f"Error initializing vector store: {e}")
            raise
    
    async def add_documents(self, documents: List[Document]) -> List[str]:
        """
        Thêm documents vào vector store
        
        Args:
            documents: Danh sách Document objects
            
        Returns:
            List of IDs của documents đã thêm
        """
        if self.vector_store is None:
            logger.error("Vector store is not initialized")
            return []
            
        try:
            logger.info(f"Adding {len(documents)} documents to collection {self.collection_name}")
            # Sử dụng phương thức add_texts
            texts = [doc.page_content for doc in documents]
            metadatas = [doc.metadata for doc in documents]
            
            # Không cần truyền embedding_function vì vector_store đã có embeddings
            ids = self.vector_store.add_texts(
                texts=texts,
                metadatas=metadatas
            )
            logger.info(f"Successfully added {len(ids)} documents")
            return ids
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {e}")
            return []
            
    def _convert_dict_to_langchain_filter(self, filter_dict: Dict) -> Optional[Dict]:
        """
        Chuyển đổi filter từ dictionary sang định dạng filter của Qdrant (không phải LangChain)
        
        Args:
            filter_dict: Dictionary chứa các điều kiện lọc
            
        Returns:
            Dict: Filter trực tiếp cho Qdrant client
        """
        if not filter_dict:
            return None
            
        # Qdrant yêu cầu filter có định dạng điều kiện trực tiếp như sau:
        # {"must": [{"key": "field", "match": {"value": value}}]}
        must_conditions = []
        
        for key, value in filter_dict.items():
            # Xử lý danh sách (ví dụ: tags)
            if isinstance(value, list) and value:
                # Tạo điều kiện OR cho danh sách giá trị
                should_conditions = []
                for item in value:
                    should_conditions.append({
                        "key": key,
                        "match": {"value": item}
                    })
                
                if should_conditions:
                    # Thêm điều kiện OR (should) vào must
                    must_conditions.append({
                        "should": should_conditions
                    })
            # Xử lý giá trị đơn (số nguyên, chuỗi)
            elif isinstance(value, (int, str)):
                must_conditions.append({
                    "key": key,
                    "match": {"value": value}
                })
        
        if not must_conditions:
            return None
            
        # Tạo filter cuối cùng
        final_filter = {"must": must_conditions}
        logger.debug(f"Converted filter for Qdrant: {final_filter}")
        return final_filter
    
    async def similarity_search(
        self, query: str, k: int = rag_settings.top_k, filter: Optional[Dict] = None
    ) -> List[Document]:
        """
        Thực hiện tìm kiếm tương đồng
        
        Args:
            query: Truy vấn cần tìm kiếm
            k: Số lượng kết quả trả về
            filter: Bộ lọc metadata (tùy chọn)
            
        Returns:
            Danh sách Document liên quan nhất
        """
        if self.vector_store is None or self.client is None:
            logger.error("Vector store or Qdrant client is not initialized")
            return []
            
        try:
            logger.info(f"Searching for '{query}' in collection {self.collection_name}")
            
            # Log filter gốc trước khi chuyển đổi
            if filter:
                logger.debug(f"Original filter before conversion: {filter}")
                
            # Chuyển đổi filter từ dict sang định dạng Qdrant native
            qdrant_filter = self._convert_dict_to_langchain_filter(filter) if filter else None
            
            # Tạo embedding cho query
            embeddings = await self.embeddings.aembed_query(query)
            
            # Tìm kiếm trực tiếp với Qdrant client API thay vì thông qua LangChain
            # Qdrant API yêu cầu tham số là "query_vector", không phải "vector"
            search_params = {
                "query_vector": embeddings,
                "limit": k,
            }
            
            if qdrant_filter:
                search_params["query_filter"] = qdrant_filter
                logger.info(f"Applied Qdrant filter: {qdrant_filter}")
                
            # Tìm kiếm trong Qdrant
            search_results = self.client.search(
                collection_name=self.collection_name,
                **search_params
            )
            
            # Chuyển đổi kết quả tìm kiếm thành Documents
            documents = []
            for result in search_results:
                payload = result.payload
                if not payload:
                    continue
                
                # Lấy nội dung và metadata từ payload
                page_content = payload.get("page_content", "") or payload.get("text", "")
                
                # Tạo metadata từ payload, loại bỏ các trường không phải metadata
                metadata = {k: v for k, v in payload.items() 
                           if k not in ["page_content", "text"] and v is not None}
                
                # Tạo Document
                documents.append(Document(page_content=page_content, metadata=metadata))
            
            logger.info(f"Found {len(documents)} relevant documents")
            return documents
        except Exception as e:
            logger.error(f"Error searching in vector store: {e}")
            return [] 
import sys
import os
import logging
import importlib.util
from typing import List, Optional, Dict, Any, Tuple
try:
    from langchain_core.documents import Document
except ImportError:
    # Fallback for development environment
    class Document:
        def __init__(self, page_content: str = "", metadata: dict = None):
            self.page_content = page_content
            self.metadata = metadata or {}

# Import trực tiếp từ config/__init__.py
from ..config import get_settings

# Đường dẫn tuyệt đối đến các module
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
rag_path = os.path.abspath(os.path.dirname(__file__))

# Import app/rag/config/config.py
rag_config_path = os.path.join(rag_path, "config", "config.py")
spec = importlib.util.spec_from_file_location("rag_config", rag_config_path)
rag_config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rag_config)

# Lấy các biến config cần thiết
rag_settings = rag_config.rag_settings

# Import các module khác
from .qdrant_connector import QdrantConnector
# from .query_extractor import QueryMetadataExtractor  # Deprecated - using VN parser
from .query_extractor_vn import parse_query, build_qdrant_filter
from ..services.llm.metadata_extractor import MetadataExtractor, MathQueryMetadata
from .context_builder import assemble_context

logger = logging.getLogger(__name__)

class RAGService:
    """
    Service cho Retrieval Augmented Generation (RAG)
    """
    
    def __init__(self, qdrant_connector: Optional[QdrantConnector] = None, metadata_extractor: Optional[MetadataExtractor] = None):
        """
        Khởi tạo RAG Service
        
        Args:
            qdrant_connector: QdrantConnector instance (tạo mới nếu không có)
            metadata_extractor: MetadataExtractor instance (tạo mới nếu không có)
        """
        self.settings = get_settings()
        self.rag_settings = rag_settings
        try:
            self.qdrant = qdrant_connector or QdrantConnector()
        except Exception as e:
            logger.error(f"Failed to initialize QdrantConnector: {str(e)}")
            self.qdrant = None
            logger.warning("RAG Service initialized without Qdrant connection. Fallback will be used.")
        
        # Khởi tạo metadata extractor mới
        try:
            self.metadata_extractor = metadata_extractor or MetadataExtractor()
        except Exception as e:
            logger.error(f"Failed to initialize MetadataExtractor: {str(e)}")
            self.metadata_extractor = None
            logger.warning("RAG Service initialized without MetadataExtractor. Will use old method.")
        
    def _extract_metadata_from_query(self, query: str) -> Dict:
        """
        Trích xuất metadata từ câu truy vấn để cải thiện tìm kiếm
        
        Args:
            query: Câu truy vấn người dùng
            
        Returns:
            Dict: Các bộ lọc phù hợp với truy vấn
        """
        try:
            # Use VN parser instead of old QueryMetadataExtractor
            vn_parsed = parse_query(query)
            extracted_metadata = {
                "category": vn_parsed.category,
                "subcategory": vn_parsed.subcategory,
                "year": vn_parsed.year,
                "question_code": vn_parsed.question_code,
                "question_num": vn_parsed.question_num
            }
            if any(extracted_metadata.values()):
                logger.info(f"VN parsed metadata from query: {extracted_metadata}")
            return extracted_metadata
        except Exception as e:
            logger.warning(f"Error extracting metadata from query: {str(e)}")
            return {}
    
    def _log_document_details(self, documents: List[Document], prefix: str = ""):
        """
        Log chi tiết về các documents tìm được để debug
        
        Args:
            documents: Danh sách documents cần log
            prefix: Tiền tố thông tin log
        """
        logger.info(f"{prefix} Found {len(documents)} documents")
        
        for i, doc in enumerate(documents[:3]):  # Log tối đa 3 documents
            logger.info(f"{prefix} Document {i+1}:")
            
            # Log metadata
            if hasattr(doc, "metadata") and isinstance(doc.metadata, dict):
                metadata_str = ", ".join([f"{k}={v}" for k, v in doc.metadata.items() 
                                         if k in ["question", "year", "tags", "type", "source", "title"]])
                logger.info(f"{prefix} - Metadata: {metadata_str}")
            
            # Log content summary
            if hasattr(doc, "page_content"):
                content_preview = doc.page_content[:100].replace("\n", " ")
                logger.info(f"{prefix} - Content preview: {content_preview}...")
    
    async def get_context(
        self, 
        query: str, 
        filter: Optional[Dict] = None,
        k: Optional[int] = None,
        use_query_metadata: bool = True,
        problem_only: bool = False
    ) -> Tuple[List[Document], bool]:
        """
        Lấy ngữ cảnh cho truy vấn từ vector database
        Bao gồm cơ chế fallback
        
        Args:
            query: Truy vấn người dùng
            filter: Bộ lọc metadata
            k: Số lượng documents lấy về
            use_query_metadata: Có trích xuất metadata từ câu truy vấn không
            problem_only: Chỉ lấy đề bài không lấy lời giải
            
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
            import time
            start_time = time.time()
            logger.info(f"🔍 RAG QUERY: '{query}' (k={k}, use_metadata={use_query_metadata})")
            
            # Trích xuất và kết hợp metadata từ câu truy vấn (nếu được bật)
            combined_filter = filter or {}

            # Lấy số lượng kết quả cần trả về
            k = k or self.rag_settings.top_k

            # Ưu tiên parser VN theo schema hiện tại (category/subcategory/metadata.year)
            vn = parse_query(query)
            vn_filter = {}
            if vn.category:
                vn_filter["category"] = vn.category
            if vn.subcategory:
                vn_filter["subcategory"] = vn.subcategory
            if vn.year is not None:
                vn_filter["year"] = vn.year

            # If exam board is specified explicitly in query (bangA/bangB), enforce it
            if vn.subcategory in ("bangA", "bangB"):
                vn_filter["category"] = "dethi"
                vn_filter["subcategory"] = vn.subcategory

            # Handle question filtering
            if vn.question_code:  # "1.2", "3.1" - exact match for both dethi and baitap
                vn_filter["question_number"] = vn.question_code
            elif vn.question_num:  # "1", "2" - depends on category
                if vn_filter.get("category") == "dethi":
                    # For dethi: exact match on question number
                    vn_filter["question_number"] = vn.question_num
                elif vn_filter.get("category") == "baitap":
                    # For baitap: section match using problem_section field
                    vn_filter["problem_section"] = vn.question_num
            
            logger.info(f"🔧 VN FILTER: {vn_filter}")

            # Gộp filter VN vào combined_filter (ưu tiên filter đã có nếu trùng)
            for key, value in vn_filter.items():
                combined_filter.setdefault(key, value)

            logger.info(f"Filter for query_points: {combined_filter}")
            
            # Tối ưu k cho Olympic context
            if combined_filter.get("_search_priority") == "olympic":
                k = min(k * 2, 10)  # Tối đa 10 documents cho Olympic
                logger.info(f"Olympic context detected, increased top_k to {k}")
            else:
                logger.info(f"Using standard top_k = {k}")
            
            # Chiến lược tìm kiếm theo thứ tự ưu tiên
            documents = []
            search_success = False
            
            # 1. Tìm kiếm chính xác với số bài
            if "question_number" in combined_filter or "problem_section" in combined_filter:
                # Determine filter type and value
                if "question_number" in combined_filter:
                    q_val = str(combined_filter["question_number"]).strip()
                    logger.info(f"STRATEGY 1: Exact search with question_number: {q_val}")
                    exact_search_filter = {"question_number": q_val}
                elif "problem_section" in combined_filter:
                    section_val = str(combined_filter["problem_section"]).strip()
                    logger.info(f"STRATEGY 1: Section search with problem_section: {section_val}")
                    exact_search_filter = {"problem_section": section_val}
                else:
                    logger.warning("STRATEGY 1: No valid question filter found")
                    exact_search_filter = None
                
                # Thêm năm nếu có và filter hợp lệ
                if exact_search_filter and "year" in combined_filter:
                    exact_search_filter["year"] = combined_filter["year"]
                    logger.info(f"Adding year {combined_filter['year']} to exact search filter")
                
                # Bảng nếu có và filter hợp lệ
                if exact_search_filter and "subcategory" in combined_filter and combined_filter["subcategory"] in ("bangA", "bangB"):
                    exact_search_filter["subcategory"] = combined_filter["subcategory"]
                    exact_search_filter["category"] = "dethi"
                
                if exact_search_filter:
                    try:
                        # Tìm kiếm chính xác theo số bài (và năm/board nếu có)
                        logger.info(f"Executing exact search with filter: {exact_search_filter}")
                        exact_docs = await self.qdrant.similarity_search(
                            query=query, 
                            k=k,
                            filter=exact_search_filter
                        )
                    
                        if exact_docs:
                            self._log_document_details(exact_docs, "STRATEGY 1:")
                            documents = exact_docs
                            search_success = True
                            logger.info("STRATEGY 1 successful - using these results")
                        else:
                            logger.info("STRATEGY 1: No documents found with exact question match")
                    except Exception as e:
                        logger.warning(f"STRATEGY 1: Error during exact search: {e}")
            
            # 2. Nếu không tìm thấy theo số bài, tìm theo chủ đề (tags) và số bài kết hợp
            if not documents and "tags" in combined_filter and "question" in combined_filter:
                logger.info(f"STRATEGY 2: Topic + Question search with tags: {combined_filter['tags']} and question: {combined_filter['question']}")
                topic_question_filter = {
                    "tags": combined_filter["tags"],
                    "question": combined_filter["question"]
                }
                
                try:
                    logger.info(f"Executing topic+question search with filter: {topic_question_filter}")
                    topic_question_docs = await self.qdrant.similarity_search(
                        query=query, 
                        k=k,
                        filter=topic_question_filter
                    )
                    
                    if topic_question_docs:
                        self._log_document_details(topic_question_docs, "STRATEGY 2:")
                        documents = topic_question_docs
                        search_success = True
                        logger.info("STRATEGY 2 successful - using these results")
                    else:
                        logger.info("STRATEGY 2: No documents found with topic + question match")
                except Exception as e:
                    logger.warning(f"STRATEGY 2: Error during topic + question search: {e}")
            
            # 3. Nếu không tìm thấy theo số bài kết hợp tags, tìm theo chỉ riêng tags
            if not documents and "tags" in combined_filter:
                logger.info(f"STRATEGY 3: Topic search with tags: {combined_filter['tags']}")
                topic_search_filter = {"tags": combined_filter["tags"]}
                
                # Thêm năm nếu có
                if "year" in combined_filter:
                    topic_search_filter["year"] = combined_filter["year"]
                    logger.info(f"Adding year {combined_filter['year']} to topic search filter")
                
                try:
                    logger.info(f"Executing topic search with filter: {topic_search_filter}")
                    topic_docs = await self.qdrant.similarity_search(
                        query=query, 
                        k=k,
                        filter=topic_search_filter
                    )
                    
                    if topic_docs:
                        self._log_document_details(topic_docs, "STRATEGY 3:")
                        documents = topic_docs
                        search_success = True
                        logger.info("STRATEGY 3 successful - using these results")
                    else:
                        logger.info("STRATEGY 3: No documents found with topic match")
                except Exception as e:
                    logger.warning(f"STRATEGY 3: Error during topic search: {e}")
            
            # 4. Cuối cùng, tìm kiếm với filter đầy đủ, hoặc không có filter nếu các cách trên thất bại
            if not documents:
                search_filter = combined_filter if combined_filter else None
                logger.info(f"STRATEGY 4: Full semantic search with filter: {search_filter}")
                
                try:
                    logger.info(f"Executing semantic search with filter: {search_filter}")
                    semantic_docs = await self.qdrant.similarity_search(
                        query=query, 
                        k=k, 
                        filter=search_filter
                    )
                    
                    if semantic_docs:
                        self._log_document_details(semantic_docs, "STRATEGY 4:")
                        documents = semantic_docs
                        search_success = True
                        logger.info("STRATEGY 4 successful - using these results")
                    else:
                        logger.warning(f"STRATEGY 4: No documents found for query with filter: {query}")
                except Exception as e:
                    logger.error(f"STRATEGY 4: Error in semantic search: {e}")
                    
                    # Thử lại lần cuối không có filter nếu trước đó có dùng filter
                    if search_filter:
                        try:
                            logger.info("STRATEGY 5: Final attempt - semantic search without filter")
                            final_docs = await self.qdrant.similarity_search(
                                query=query, 
                                k=k
                            )
                            
                            if final_docs:
                                self._log_document_details(final_docs, "STRATEGY 5:")
                                documents = final_docs
                                search_success = True
                                logger.info("STRATEGY 5 successful - using these results")
                            else:
                                logger.warning("STRATEGY 5: No documents found even without filter")
                        except Exception as retry_e:
                            logger.error(f"STRATEGY 5: Final attempt failed: {retry_e}")
            
            # Đánh dấu documents nếu người dùng chỉ muốn xem đề bài
            if documents and problem_only:
                logger.info(f"Marking documents as problem_only = {problem_only}")
                for doc in documents:
                    # Thêm flag vào metadata để format_document biết chỉ lấy đề bài
                    if not hasattr(doc, "metadata"):
                        doc.metadata = {}
                    doc.metadata["_looking_for_problem_only"] = True
            
            # No post-filtering needed - problem_section field handles baitap section queries directly
            
            # Nếu tìm thấy bất kỳ kết quả nào
            if documents:
                elapsed = time.time() - start_time
                top_titles = [doc.metadata.get("title", "No title")[:50] for doc in documents[:3]]
                logger.info(f"✅ RAG SUCCESS: {len(documents)} docs in {elapsed:.2f}s")
                logger.info(f"📋 Top results: {top_titles}")
                return documents, True
            
            # Không tìm thấy gì cả
            elapsed = time.time() - start_time
            logger.warning(f"❌ RAG FAILED: No documents found in {elapsed:.2f}s")
            return [], False
            
        except Exception as e:
            # Cơ chế fallback - ghi log lỗi nhưng không làm hỏng trải nghiệm người dùng
            error_type = type(e).__name__
            logger.error(f"Error retrieving context: {error_type} - {e}")
            return [], False
    
    def format_context_for_prompt(self, documents: List[Document]) -> str:
        """
        Định dạng documents thành context cho prompt (ưu tiên natural_*)
        Sử dụng context_builder để ghép và thêm citation title/source_file/year.
        """
        if not documents:
            return ""
        budget = getattr(self.rag_settings, 'context_token_budget', 1200)
        context, _ = assemble_context(documents, budget_tokens=budget)
        return context
    
    def format_context_for_display(self, documents: List[Document], query: str) -> str:
        """
        Format context đặc biệt cho việc hiển thị đề bài nguyên văn
        """
        from .prompts.templates import LinearAlgebraTemplates
        return LinearAlgebraTemplates.get_problem_display_prompt(query, documents)
    
    async def get_formatted_context(
        self, query: str, filter: Optional[Dict] = None, k: Optional[int] = None,
        use_query_metadata: bool = True
    ) -> Tuple[str, bool]:
        """
        Lấy và định dạng context cho query với hỗ trợ display_mode
        
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
        # Trích xuất metadata để xác định display_mode
        metadata = None
        if self.metadata_extractor and use_query_metadata:
            try:
                metadata = await self.metadata_extractor.extract_metadata(query)
                logger.info(f"Extracted metadata for formatting: {metadata}")
            except Exception as e:
                logger.warning(f"Error extracting metadata for formatting: {str(e)}")
        
        documents, success = await self.get_context(query, filter, k, use_query_metadata)
        if not success:
            return "", False
        
        # Sử dụng display_mode nếu có
        if metadata and hasattr(metadata, 'display_mode') and metadata.display_mode:
            logger.info("Using display mode for problem presentation")
            return self.format_context_for_display(documents, query), True
        else:
            return self.format_context_for_prompt(documents), True
    
    async def get_context_with_tiered_search(self, query: str, top_k: int = 5) -> List[Document]:
        """
        Truy xuất context sử dụng tiered search strategy
        """
        try:
            # Bước 1: Trích xuất metadata
            if self.metadata_extractor:
                metadata = await self.metadata_extractor.extract_metadata(query)
                logger.info(f"Extracted metadata: {metadata}")
            else:
                # Fallback to old method
                metadata_dict = self._extract_metadata_from_query(query)
                metadata = MathQueryMetadata(
                    year=metadata_dict.get('year'),
                    exam=metadata_dict.get('exam'),
                    question=metadata_dict.get('question'),
                    level=metadata_dict.get('level'),
                    tags=metadata_dict.get('tags'),
                    requesting_solution=metadata_dict.get('requesting_solution', False)
                )
            
            # Bước 2: Tiered search
            documents = await self._tiered_search(metadata, query, top_k)
            
            # Bước 3: Tag context
            tagged_documents = self._tag_retrieved_context(documents, metadata.requesting_solution)
            
            return tagged_documents
            
        except Exception as e:
            logger.error(f"Error in get_context_with_tiered_search: {str(e)}")
            # Fallback: semantic search
            return await self._semantic_search_fallback(query, top_k)
    
    async def _tiered_search(self, metadata: MathQueryMetadata, query: str, top_k: int) -> List[Document]:
        """
        Thực hiện tìm kiếm 3 tầng
        """
        
        # Tầng 1: Exact metadata matching
        if self._has_sufficient_metadata(metadata):
            logger.info("Trying Tier 1: Exact metadata matching")
            documents = await self._exact_metadata_search(metadata, top_k)
            if documents:
                logger.info(f"Tier 1 successful: found {len(documents)} documents")
                return documents
        
        # Tầng 2: Hybrid search (metadata + semantic)
        logger.info("Trying Tier 2: Hybrid search")
        documents = await self._hybrid_search(metadata, query, top_k)
        if documents:
            logger.info(f"Tier 2 successful: found {len(documents)} documents")
            return documents
        
        # Tầng 3: Pure semantic search
        logger.info("Trying Tier 3: Pure semantic search")
        documents = await self._semantic_search_fallback(query, top_k)
        logger.info(f"Tier 3 successful: found {len(documents)} documents")
        return documents

    def _has_sufficient_metadata(self, metadata: MathQueryMetadata) -> bool:
        """Kiểm tra xem có đủ metadata để thực hiện exact search không - DEPRECATED"""
        # DEPRECATED: Using VN parser instead
        return False

    async def _exact_metadata_search(self, metadata: MathQueryMetadata, top_k: int) -> List[Document]:
        """Tầng 1: Tìm kiếm chính xác theo metadata"""
        try:
            if not self.qdrant:
                return []
                
            # Tạo filter cho Qdrant
            query_filter = {
                "year": metadata.year,
                "question": metadata.question,
                "level": metadata.level
            }
            if getattr(metadata, "exam", None):
                query_filter["exam"] = metadata.exam
            if getattr(metadata, "source", None):
                query_filter["source"] = metadata.source
            # Nếu chỉ filter, dùng HTTP API
            results = self.qdrant.search_with_filter_http(query_filter, limit=top_k)
            # Chuyển đổi kết quả HTTP thành Document nếu cần
            # ... giữ nguyên logic chuyển đổi ...
            return results
        except Exception as e:
            logger.error(f"Error in exact metadata search: {str(e)}")
            return []

    async def _hybrid_search(self, metadata: MathQueryMetadata, query: str, top_k: int) -> List[Document]:
        """Tầng 2: Tìm kiếm lai (metadata + semantic)"""
        try:
            if not self.qdrant:
                return await self._semantic_search_fallback(query, top_k)
                
            # Tạo filter nới lỏng
            query_filter = {}
            if metadata.year:
                query_filter["year"] = metadata.year
            if metadata.level:
                query_filter["level"] = metadata.level
            if metadata.tags:
                query_filter["tags"] = metadata.tags
            if getattr(metadata, "exam", None):
                query_filter["exam"] = metadata.exam
            if getattr(metadata, "source", None):
                query_filter["source"] = metadata.source
            # Nếu không có filter nào, chuyển sang semantic
            if not query_filter:
                return await self._semantic_search_fallback(query, top_k)
            # Nếu chỉ filter, dùng HTTP API
            if not query:
                results = self.qdrant.search_with_filter_http(query_filter, limit=top_k)
                # Chuyển đổi kết quả HTTP thành Document nếu cần
                # ... giữ nguyên logic chuyển đổi ...
                return results
            # Nếu có vector, dùng similarity_search như cũ
            results = await self.qdrant.similarity_search(
                query=query,
                k=top_k,
                filter=query_filter
            )
            return results
        except Exception as e:
            logger.error(f"Error in hybrid search: {str(e)}")
            return await self._semantic_search_fallback(query, top_k)

    async def _semantic_search_fallback(self, query: str, top_k: int) -> List[Document]:
        """Tầng 3: Tìm kiếm ngữ nghĩa thuần túy"""
        try:
            if not self.qdrant:
                return []
            results = await self.qdrant.similarity_search(
                query=query,
                k=top_k,
                filter=None
            )
            return results
        except Exception as e:
            logger.error(f"Error in semantic search: {str(e)}")
            return []
    
    def _tag_retrieved_context(self, documents: List[Document], requesting_solution: bool) -> List[Document]:
        """
        Gắn thẻ context với <problem> và <solution> tags
        Hỗ trợ cấu trúc mới với problem_statement và problem_parts
        """
        tagged_documents = []
        
        for doc in documents:
            try:
                # Lấy content từ cấu trúc mới hoặc cũ
                problem_statement = doc.metadata.get('problem_statement', '')
                problem_parts = doc.metadata.get('problem_parts', {})
                
                # Fallback cho cấu trúc cũ
                if not problem_statement:
                    problem_statement = doc.metadata.get('content', '')
                
                # Tạo nội dung đề bài đầy đủ
                full_problem_content = problem_statement
                
                # Thêm problem_parts nếu có
                if problem_parts and isinstance(problem_parts, dict):
                    full_problem_content += "\n\n"
                    for part_key, part_content in problem_parts.items():
                        full_problem_content += f"\n**({part_key})** {part_content}\n"
                
                # Tạo tagged content
                tagged_content = f"<problem>{full_problem_content}</problem>"
                
                # Thêm solution nếu được yêu cầu
                if requesting_solution:
                    # Ưu tiên cấu trúc mới
                    solution_data = doc.metadata.get('solution', {})
                    if solution_data and isinstance(solution_data, dict):
                        full_solution = solution_data.get('full_solution', '')
                        solution_parts = solution_data.get('solution_parts', {})
                        
                        if full_solution or solution_parts:
                            solution_content = full_solution
                            if solution_parts and isinstance(solution_parts, dict):
                                solution_content += "\n\n"
                                for part_key, part_solution in solution_parts.items():
                                    solution_content += f"**{part_key})** {part_solution}\n"
                            tagged_content += f"\n<solution_hints>{solution_content}</solution_hints>"
                    else:
                        # Fallback cho cấu trúc cũ
                        suggested_solution = doc.metadata.get('suggested_solution', '')
                        if suggested_solution:
                            tagged_content += f"\n<solution>{suggested_solution}</solution>"
                
                # Tạo document mới với content đã tag
                tagged_doc = Document(
                    page_content=tagged_content,
                    metadata=doc.metadata
                )
                
                tagged_documents.append(tagged_doc)
                
            except Exception as e:
                logger.error(f"Error tagging document: {str(e)}")
                # Fallback: giữ nguyên document
                tagged_documents.append(doc)
        
        return tagged_documents

    async def get_context_with_history(
        self, 
        query: str, 
        chat_history: List = None,
        filter: Optional[Dict] = None,
        k: Optional[int] = None,
        use_query_metadata: bool = True,
        problem_only: bool = False
    ) -> Tuple[List[Document], bool]:
        """
        Lấy ngữ cảnh với xem xét chat history để xử lý follow-up questions
        
        Args:
            query: Truy vấn người dùng
            chat_history: Lịch sử chat để xử lý follow-up
            filter: Bộ lọc metadata
            k: Số lượng documents lấy về
            use_query_metadata: Có trích xuất metadata từ câu truy vấn không
            problem_only: Chỉ lấy đề bài không lấy lời giải
            
        Returns:
            Tuple[List[Document], bool]: (documents, success_flag)
        """
        try:
            # Trích xuất metadata từ query
            extracted_filter = {}
            if use_query_metadata:
                extracted_filter = self._extract_metadata_from_query(query)
            
            # Xử lý follow-up questions
            if extracted_filter.get("is_follow_up", False) and chat_history:
                logger.info("Processing follow-up question with chat history")
                return await self._handle_follow_up_with_history(query, chat_history)
            
            # Nếu không phải follow-up, dùng method thông thường
            return await self.get_context(
                query=query,
                filter=filter,
                k=k,
                use_query_metadata=use_query_metadata,
                problem_only=problem_only
            )
            
        except Exception as e:
            logger.error(f"Error in get_context_with_history: {str(e)}", exc_info=True)
            return [], False

    async def _handle_follow_up_with_history(self, query: str, chat_history: List) -> Tuple[List[Document], bool]:
        """
        Xử lý follow-up questions bằng cách tìm context từ chat history
        """
        try:
            logger.info("Handling follow-up question with chat history")
            
            # Tìm response gần nhất của AI trong chat history
            last_ai_response = None
            for message in reversed(chat_history):
                if hasattr(message, 'role') and message.role == 'model':
                    last_ai_response = message.content
                    break
            
            if not last_ai_response:
                logger.info("No previous AI response found, using regular search")
                return await self.get_context(query, use_query_metadata=False)
            
            # Trích xuất thông tin bài toán từ response trước
            problem_info = self._extract_problem_info_from_response(last_ai_response)
            
            if problem_info:
                logger.info(f"Found problem info from previous response: {problem_info}")
                # Tìm kiếm với thông tin bài toán cụ thể
                return await self.get_context(
                    query=f"bài {problem_info.get('question', '')} {problem_info.get('category', '')}",
                    filter=problem_info,
                    use_query_metadata=False
                )
            else:
                # Fallback: tìm kiếm rộng với intent solution
                return await self.get_context(
                    query=query,
                    filter={"intent": "solution"},
                    use_query_metadata=False
                )
                
        except Exception as e:
            logger.error(f"Error handling follow-up: {str(e)}")
            return await self.get_context(query, use_query_metadata=False)

    def _extract_problem_info_from_response(self, response: str) -> Dict:
        """
        Trích xuất thông tin bài toán từ response trước đó - Tối ưu cho dữ liệu Olympic
        """
        import re
        problem_info = {}
        
        try:
            # Tìm "Bài X" trong response với nhiều pattern
            patterns = [
                r'Bài\s+(\d+)',  # Bài 1
                r'bài\s+(\d+)',  # bài 1
                r'Đề\s+bài:\s*Bài\s+(\d+)',  # Đề bài: Bài 1
            ]
            
            for pattern in patterns:
                bai_match = re.search(pattern, response)
                if bai_match:
                    problem_info["question"] = bai_match.group(1)
                    break
            
            # Tìm loại đề thi với độ ưu tiên cao
            if any(keyword in response for keyword in ["ĐỀ THI BẢNG A", "Đề thi Bảng A", "BẢNG A", "Bảng A"]):
                problem_info["subcategory"] = "bangA"
                problem_info["category"] = "dethi"
                problem_info["exam_board"] = "BANGA"
            elif any(keyword in response for keyword in ["ĐỀ THI BẢNG B", "Đề thi Bảng B", "BẢNG B", "Bảng B"]):
                problem_info["subcategory"] = "bangB"
                problem_info["category"] = "dethi"
                problem_info["exam_board"] = "BANGB"
            
            # Tìm dạng bài tập
            elif any(keyword in response for keyword in ["BÀI TẬP", "Bài tập"]):
                problem_info["category"] = "baitap"
                # Xác định subcategory dựa trên nội dung
                if any(keyword in response for keyword in ["ma trận", "Ma trận"]):
                    problem_info["subcategory"] = "mt"
                elif any(keyword in response for keyword in ["định thức", "Định thức"]):
                    problem_info["subcategory"] = "dt"
                elif any(keyword in response for keyword in ["hệ phương trình", "Hệ phương trình"]):
                    problem_info["subcategory"] = "hpt"
                elif any(keyword in response for keyword in ["giá trị riêng", "Giá trị riêng"]):
                    problem_info["subcategory"] = "gtr"
            
            # Tìm năm với pattern cải thiện
            year_patterns = [
                r'năm\s+(\d{4})',  # năm 2024
                r'(\d{4})',        # 2024
                r'Năm:\s*(\d{4})', # Năm: 2024
            ]
            
            for pattern in year_patterns:
                year_match = re.search(pattern, response)
                if year_match:
                    year = int(year_match.group(1))
                    if 2020 <= year <= 2030:  # Validate year range
                        problem_info["year"] = year
                        break
            
            # Thêm metadata Olympic
            if problem_info.get("category") == "dethi":
                problem_info["difficulty_level"] = "quoc_gia"
                problem_info["subject_area"] = "dai_so_tuyen_tinh"
            
            logger.info(f"Extracted problem info: {problem_info}")
            return problem_info
            
        except Exception as e:
            logger.error(f"Error extracting problem info: {e}")
            return {} 
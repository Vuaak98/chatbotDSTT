import sys
import os
import json
import requests
import logging
import importlib.util
from typing import List, Optional, Dict, Any, Union
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
from qdrant_client.http import models
from langchain_qdrant import QdrantVectorStore

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

logger = logging.getLogger(__name__)

class QdrantConnector:
    """
    Kết nối và tương tác với Qdrant
    """
    
    def __init__(self, qdrant_url=None, qdrant_api_key=None, collection_name=None, client=None, embeddings=None, *args, **kwargs):
        self.qdrant_url = qdrant_url or rag_settings.qdrant_url
        # Nếu là Secret, dùng get_secret_value, nếu không thì lấy trực tiếp
        if qdrant_api_key is not None:
            self.qdrant_api_key = qdrant_api_key
        else:
            api_key = getattr(rag_settings, 'qdrant_api_key', None)
            if hasattr(api_key, 'get_secret_value'):
                self.qdrant_api_key = api_key.get_secret_value()
            else:
                self.qdrant_api_key = api_key
        self.collection_name = collection_name or rag_settings.qdrant_collection_name
        
        # Lấy API key từ config
        self.openai_api_key = os.getenv("OPENAI_API_KEY") or get_settings().openai_api_key
        
        # Cài đặt Qdrant client
        if client:
            self.client = client
        else:
            try:
                logger.info(f"Connecting to Qdrant at {self.qdrant_url}")
                self.client = QdrantClient(
                    url=self.qdrant_url,
                    api_key=self.qdrant_api_key,
                    timeout=60  # Tăng timeout để xử lý mạng chậm
                )
                # Kiểm tra kết nối
                self.client.get_collections()
                logger.info(f"Connected to Qdrant at {self.qdrant_url}")
            except Exception as e:
                logger.error(f"Failed to connect to Qdrant: {e}")
                raise ConnectionError(f"Could not connect to Qdrant: {e}") from e
                
        # Cài đặt embeddings model với error handling
        try:
            if not self.openai_api_key:
                raise ValueError("OpenAI API key is required for embeddings")
                
            logger.info(f"Initializing OpenAI embeddings with model: {rag_settings.embedding_model_name}")
            self.embeddings = embeddings or OpenAIEmbeddings(
                model=rag_settings.embedding_model_name,
                openai_api_key=self.openai_api_key  # Sử dụng openai_api_key thay vì api_key
            )
            # Test embedding để kiểm tra quota
            test_result = self.embeddings.embed_query("test")
            logger.info("OpenAI embeddings initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize vector store: {e}")
            logger.warning("Could not initialize vector store: Could not initialize vector store: " + str(e))
            self.embeddings = None
        
        # Khởi tạo vector store
        try:
            self._init_vector_store()
        except Exception as e:
            logger.warning(f"Could not initialize vector store: {e}")
            logger.warning("QdrantConnector initialized without vector store. Only HTTP API will be available.")
        
    def _init_vector_store(self):
        """
        Khởi tạo Vector Store
        """
        try:
            # Kiểm tra xem collection đã tồn tại chưa
            collections = self.client.get_collections().collections
            collection_names = [c.name for c in collections]
            
            if self.collection_name not in collection_names:
                logger.warning(f"Collection {self.collection_name} not found. Available collections: {collection_names}")
            else:
                logger.info(f"Collection {self.collection_name} exists")
                
            # Tạo vector store
            self.vector_store = QdrantVectorStore(
                client=self.client,
                collection_name=self.collection_name,
                embedding=self.embeddings,  # Lưu ý: langchain-qdrant mới dùng embedding thay vì embeddings
                vector_name="semantic_vector",  # Named vector in your collection
            )
            
            logger.info(f"Vector store initialized for collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Failed to initialize vector store: {e}")
            raise RuntimeError(f"Could not initialize vector store: {e}") from e
    
    async def add_documents(self, documents: List[Document], batch_size: int = 100) -> bool:
        """
        Thêm documents vào Qdrant
        
        Args:
            documents: Danh sách Document objects
            batch_size: Số lượng documents mỗi batch
            
        Returns:
            Boolean: True nếu thành công
        """
        try:
            # Kiểm tra nếu collection không tồn tại, tạo mới
            try:
                self.client.get_collection(collection_name=self.collection_name)
                logger.info(f"Collection {self.collection_name} exists")
            except Exception:
                logger.info(f"Creating new collection: {self.collection_name}")
                # Lấy kích thước vector từ embedding model
                vector_size = len(await self.embeddings.aembed_query("Test"))
                
                # Tạo collection mới với cấu hình phù hợp
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=rest.VectorParams(
                        size=vector_size,
                        distance=rest.Distance.COSINE
                    ),
                )
                logger.info(f"Created new collection: {self.collection_name}")
            
            # Thêm documents vào vector store
            for i in range(0, len(documents), batch_size):
                batch = documents[i:i + batch_size]
                logger.info(f"Adding batch {i//batch_size + 1}/{(len(documents)-1)//batch_size + 1} " 
                           f"({len(batch)} documents)")
                
                # Sử dụng add_texts thay vì add_documents để tương thích
                texts = [doc.page_content for doc in batch]
                metadatas = [doc.metadata for doc in batch]
                
                # Sử dụng phương thức từ vector store
                ids = await self.vector_store.aadd_texts(
                    texts=texts,
                    metadatas=metadatas
                )
                
                logger.info(f"Added {len(ids)} documents to collection {self.collection_name}")
                
            return True
        except Exception as e:
            logger.error(f"Failed to add documents: {e}")
            raise RuntimeError(f"Could not add documents: {e}") from e
    
    def _convert_dict_to_langchain_filter(self, filter_dict: Dict) -> Dict:
        """
        Chuyển đổi dict filter thành filter format của Qdrant
        
        Args:
            filter_dict: Dict filter (e.g., {"year": 2023, "tags": ["linear algebra"]})
            
        Returns:
            Dict: Qdrant filter format
        """
        if not filter_dict:
            return {}
            
        conditions = []
        
        for key, value in filter_dict.items():
            if isinstance(value, list):
                # Trường hợp là list (như tags)
                list_conditions = []
                for item in value:
                    list_conditions.append(
                        {"key": key, "match": {"value": item}}
                    )
                if list_conditions:
                    # Nếu có nhiều điều kiện, dùng "should" (tương đương OR)
                    conditions.append({"should": list_conditions})
            else:
                # Trường hợp là giá trị đơn lẻ
                conditions.append(
                    {"key": key, "match": {"value": value}}
                )
                
        if not conditions:
            return {}
            
        # Nếu chỉ có 1 điều kiện, trả về luôn điều kiện đó
        if len(conditions) == 1:
            return {"filter": {"must": conditions}}
            
        # Nếu có nhiều điều kiện, dùng "must" (tương đương AND)
        return {"filter": {"must": conditions}}
    
    async def similarity_search(
        self, 
        query: str, 
        k: int = 5, 
        filter: Optional[Dict] = None
    ) -> List[Document]:
        """
        Tìm kiếm theo vector similarity
        
        Args:
            query: Câu truy vấn
            k: Số lượng kết quả
            filter: Bộ lọc metadata
            
        Returns:
            List[Document]: Kết quả tìm kiếm
        """
        logger.info(f"Searching for '{query}' in collection {self.collection_name}")
        
        # Kiểm tra xem embeddings có khả dụng không
        if self.embeddings is None:
            logger.error("Embeddings not available - cannot perform similarity search")
            raise Exception("Embeddings service not available")
        
        try:
            # Kiểm tra filter và log
            qdrant_filter = None
            if filter:
                logger.info(f"Original filter: {filter}")
                # Chuyển đổi filter sang định dạng của Qdrant
                if isinstance(filter, dict):
                    # Xử lý filter dạng đặc biệt
                    must_conditions = []
                    
                    # Xử lý trường hợp question_number (exact match)
                    if "question_number" in filter:
                        q_value = str(filter["question_number"]).strip()
                        must_conditions.append({
                            "key": "question_number", 
                            "match": {"value": q_value}
                        })
                    
                    # Xử lý trường hợp problem_section (section match for baitap)
                    if "problem_section" in filter:
                        section_value = str(filter["problem_section"]).strip()
                        must_conditions.append({
                            "key": "problem_section", 
                            "match": {"value": section_value}
                        })

                    # Xử lý trường hợp năm - cần phải match chính xác
                    if "year" in filter:
                        must_conditions.append({
                            "key": "metadata.year", 
                            "match": {"value": filter["year"]}
                        })
                        
                    # Xử lý trường hợp tags - cần phải kiểm tra xem tag có trong danh sách
                    if "tags" in filter and isinstance(filter["tags"], list):
                        tag_conditions = []
                        for tag in filter["tags"]:
                            tag_conditions.append({
                                "key": "tags", 
                                "match": {"value": tag}
                            })
                        # Nếu chỉ cần 1 tag match
                        if tag_conditions:
                            must_conditions.append({"should": tag_conditions})
                    
                    # Xử lý các trường hợp còn lại
                    for key, value in filter.items():
                        if key not in ["question", "question_number", "year", "tags"]:
                            must_conditions.append({
                                "key": key, 
                                "match": {"value": value}
                            })
                    
                    if must_conditions:
                        qdrant_filter = {"must": must_conditions}
                        logger.info(f"Converted filter: {qdrant_filter}")
            
            # Tìm kiếm bằng phương pháp search với error handling
            try:
                query_vector = await self.embeddings.aembed_query(query)
            except Exception as e:
                logger.error(f"Failed to search in Qdrant: {e}")
                raise Exception(f"Failed to generate embeddings: {e}")

            # Temporary: use deprecated search for compatibility, with named vector tuple
            search_params = {
                "collection_name": self.collection_name,
                "query_vector": ("semantic_vector", query_vector),
                "limit": k,
                "with_payload": True,
                "with_vectors": False,
            }
            if qdrant_filter:
                search_params["query_filter"] = qdrant_filter

            search_results = self.client.search(**search_params)

            # Chuyển đổi kết quả thành documents
            documents = []
            for result in search_results:
                # Lấy metadata và content từ payload (ưu tiên trường natural_*)
                payload = result.payload or {}
                page_content = (
                    payload.get("problem_statement_natural")
                    or payload.get("natural_language_desc")
                    or payload.get("latex_string")
                    or ""
                )
                metadata = payload.copy()
                # Thêm score vào metadata nếu có
                metadata["score"] = getattr(result, "score", None)

                documents.append(Document(
                    page_content=page_content,
                    metadata=metadata
                ))
            
            logger.info(f"Found {len(documents)} documents")
            
            # Log kết quả đầu tiên để debug
            if documents and len(documents) > 0:
                first_doc = documents[0]
                metadata_preview = {k: v for k, v in first_doc.metadata.items() 
                                   if k in ["question", "year", "tags", "type", "source", "score"]}
                logger.info(f"Top result metadata: {metadata_preview}")
                logger.info(f"Top result content preview: {first_doc.page_content[:100]}...")
            
            return documents
        except Exception as e:
            logger.error(f"Failed to search in Qdrant: {e}")
            # Trả về danh sách rỗng thay vì ném exception để tăng khả năng chịu lỗi
            return [] 

    def search_with_filter_http(self, filter_query, limit=5):
        """Truy vấn filter tới Qdrant Cloud qua HTTP API, trả về kết quả tương tự search."""
        qdrant_url = self.qdrant_url
        api_key = self.qdrant_api_key
        collection_name = self.collection_name
        VECTOR_SIZE = 1536  # Sửa nếu dùng embedding khác
        search_url = f"{qdrant_url}/collections/{collection_name}/points/search"
        headers = {
            "Content-Type": "application/json",
        }
        if api_key:
            headers["api-key"] = api_key
            
        # Chuyển đổi filter_query thành định dạng Qdrant filter hợp lệ
        qdrant_filter = {"must": []}
        
        # Log chi tiết filter gốc
        logger.info(f"Filter gốc: {filter_query}")
        
        # Xử lý đặc biệt cho trường level (chuyển thành tìm kiếm trong topic)
        if "level" in filter_query:
            level_value = filter_query.pop("level")
            # Chuyển level thành chữ hoa để tìm trong topic
            level_upper = level_value.upper() if isinstance(level_value, str) else level_value
            
            # Tìm kiếm trong topic với pattern "bảng A", "bảng B", "bảng C"
            qdrant_filter["must"].append({
                "key": "topic",
                "match": {"value": f"đề thi bảng {level_upper}"}
            })
            logger.info(f"Chuyển filter level='{level_value}' thành tìm kiếm trong topic: đề thi bảng {level_upper}")
        
        for key, value in filter_query.items():
            # Xử lý đặc biệt cho trường question/question_number
            if key in ("question", "question_number"):
                # Tạo điều kiện tương thích cả hai khóa, hỗ trợ 1 hoặc 1.2
                q_val = str(value).strip()
                question_should = [
                    {"key": "question", "match": {"value": q_val}},
                    {"key": "question_number", "match": {"value": q_val}},
                ]
                qdrant_filter["must"].append({"should": question_should})
                logger.info(f"Điều kiện question OR question_number = {q_val}")
            elif key == "tags" and isinstance(value, list):
                tag_conditions = []
                for tag in value:
                    tag_conditions.append({
                        "key": "tags", 
                        "match": {"value": tag}
                    })
                if tag_conditions:
                    qdrant_filter["must"].append({"should": tag_conditions})
            else:
                qdrant_filter["must"].append({
                    "key": key,
                    "match": {"value": value}
                })
        
        # Nếu không có điều kiện, không dùng filter
        if not qdrant_filter["must"]:
            qdrant_filter = None
            
        logger.info(f"HTTP filter query chi tiết: {qdrant_filter}")
        
        data = {
            "vector": [0.0] * VECTOR_SIZE,  # Vector zero đúng kích thước
            "filter": qdrant_filter,
            "limit": limit,
            "with_payload": True,  # Đảm bảo luôn lấy payload
            "with_vectors": False  # Không cần vector để tiết kiệm băng thông
        }
        
        try:
            response = requests.post(search_url, headers=headers, data=json.dumps(data))
            if response.status_code == 200:
                result_data = response.json().get("result", [])
                # Chuyển đổi kết quả thành documents
                documents = []
                
                for result in result_data:
                    try:
                        # Lấy payload từ kết quả
                        payload = result.get("payload", {})
                        
                        # Lấy nội dung từ các trường khác nhau
                        page_content = payload.get("content", "")
                        if not page_content and "suggested_solution" in payload:
                            page_content = payload.get("suggested_solution", "")
                        
                        # Nếu không có content, bỏ qua point này
                        if not page_content:
                            continue
                            
                        # Tạo metadata từ payload
                        metadata = {k: v for k, v in payload.items() if k not in ["content", "suggested_solution"]}
                        
                        # Thêm score vào metadata
                        metadata["score"] = result.get("score", 0.0)
                        
                        documents.append(Document(
                            page_content=page_content,
                            metadata=metadata
                        ))
                    except Exception as e:
                        logger.error(f"Lỗi khi xử lý point: {e}")
                
                # Log chi tiết kết quả
                logger.info(f"Tìm thấy {len(documents)} documents qua HTTP API")
                if documents:
                    for i, doc in enumerate(documents[:3]):  # Log tối đa 3 kết quả đầu tiên
                        meta_info = {k: v for k, v in doc.metadata.items() 
                                    if k in ["id", "question", "year", "tags", "type", "score", "topic"]}
                        logger.info(f"Kết quả {i+1}: {meta_info}")
                else:
                    logger.warning("Không tìm thấy kết quả nào cho filter")
                
                return documents
            else:
                error_msg = f"Qdrant HTTP filter error: {response.status_code} {response.text}"
                logger.error(error_msg)
                return []
        except Exception as e:
            logger.error(f"Exception in HTTP filter: {str(e)}")
            return [] 
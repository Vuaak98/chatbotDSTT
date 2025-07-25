import os
from typing import Optional

from pydantic_settings import BaseSettings
from pydantic import SecretStr

class RAGSettings(BaseSettings):
    """
    Cấu hình cho RAG
    """
    # Qdrant cấu hình
    qdrant_url: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    qdrant_api_key: SecretStr = SecretStr(os.getenv("QDRANT_API_KEY", ""))
    qdrant_collection_name: str = os.getenv("QDRANT_COLLECTION_NAME", "linear_algebra")

    # Cấu hình embedding
    embedding_model_name: str = os.getenv("EMBEDDING_MODEL_NAME", "text-embedding-3-small")
    
    # Cấu hình retrieval
    top_k: int = int(os.getenv("RAG_TOP_K", "3"))
    
    # Đường dẫn dữ liệu
    data_dir: str = os.getenv("RAG_DATA_DIR", "data/linear_algebra")
    
    model_config = {
        "env_file": ".env",
        "extra": "ignore"  # Bỏ qua các trường không được định nghĩa
    }

rag_settings = RAGSettings()
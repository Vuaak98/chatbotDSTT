# Không import get_settings từ config.py để tránh circular import
# Thay vào đó, chúng ta sẽ định nghĩa get_settings trực tiếp ở đây
import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
# Get the backend directory path
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env_path = os.path.join(backend_dir, '.env')
load_dotenv(env_path)

# Định nghĩa Settings class
class Settings(BaseSettings):
    # Database Configuration
    database_url: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///aichatbot.db"
    )

    # API Keys
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")

    # Model Configuration
    gemini_model_name: str = os.getenv("GEMINI_MODEL_NAME", "gemini-1.5-flash")
    openai_model_name: str = os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo")

    # RAG Configuration
    rag_enabled: bool = os.getenv("RAG_ENABLED", "True").lower() == "true"
    use_openai: bool = os.getenv("USE_OPENAI", "False").lower() == "true"

    # File Upload Settings
    upload_dir: str = os.getenv("UPLOAD_DIR", "/tmp/ai-math-chatbot-uploads")
    max_file_size: int = 20 * 1024 * 1024  # 20MB default
    max_files_per_prompt: int = 5  # Maximum files per prompt

    # Server Settings
    allowed_origins: str = os.getenv("ALLOWED_ORIGINS", "*")

    # In Pydantic v2, Config is replaced with model_config
    model_config = {
        "env_file": ".env",
        "extra": "ignore"  # Allow extra fields in environment variables
    }

@lru_cache()
def get_settings():
    return Settings()

# Các biến để tương thích ngược
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo") 
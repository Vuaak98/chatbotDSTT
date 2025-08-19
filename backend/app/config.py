import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from functools import lru_cache

# Load environment variables from .env file
# Get the backend directory path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(backend_dir, '.env')
load_dotenv(env_path)

def parse_int_env(var_name: str, default: int) -> int:
    value = os.getenv(var_name, str(default))
    # Remove comments and strip whitespace
    value = value.split('#')[0].strip()
    return int(value)

class Settings(BaseSettings):
    # Database Configuration
    database_url: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://neondb_owner:npg_9YwFtd2mhBfz@ep-spring-salad-a13yb5qy-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
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
    max_file_size: int = parse_int_env("MAX_FILE_SIZE", 20 * 1024 * 1024)  # 20MB default

    # Server Settings
    allowed_origins: str = os.getenv("ALLOWED_ORIGINS", "*")

    # In Pydantic v2, Config is replaced with model_config
    model_config = {
        "env_file": ".env",
        "extra": "ignore"  # Allow extra fields in environment variables
    }

# Chúng ta sẽ sử dụng get_settings từ config/__init__.py
# Để tránh circular import, không import từ .config

# Các biến để tương thích ngược
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo")
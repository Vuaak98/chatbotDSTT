from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import time
import logging
from sqlalchemy.pool import QueuePool

logger = logging.getLogger(__name__)

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://neondb_owner:npg_9YwFtd2mhBfz@ep-spring-salad-a13yb5qy-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
)

# Configure the engine based on the database type
engine_args = {}
if DATABASE_URL.startswith("sqlite"):
    # For SQLite, connect_args is needed to allow multithreading
    engine_args["connect_args"] = {"check_same_thread": False}
elif DATABASE_URL.startswith("postgresql"):
    # For PostgreSQL, add connection pool settings and retry mechanism
    engine_args["pool_size"] = 5  # Số kết nối trong pool
    engine_args["max_overflow"] = 10  # Số kết nối tạm thời tối đa
    engine_args["pool_timeout"] = 30  # Thời gian chờ kết nối từ pool (seconds)
    engine_args["pool_recycle"] = 1800  # Tái sử dụng kết nối sau 30 phút
    engine_args["pool_pre_ping"] = True  # Kiểm tra kết nối trước khi sử dụng
    engine_args["connect_args"] = {
        "connect_timeout": 10,  # Timeout khi kết nối tới DB (seconds)
        "keepalives": 1,  # Bật keepalive
        "keepalives_idle": 30,  # Thời gian idle trước khi gửi keepalive (seconds)
        "keepalives_interval": 10,  # Thời gian giữa các keepalive (seconds)
        "keepalives_count": 5  # Số lần thử keepalive trước khi bỏ kết nối
    }
    engine_args["poolclass"] = QueuePool

# Thử kết nối với DB với cơ chế retry
max_retries = 3
retry_delay = 2  # seconds

for attempt in range(max_retries):
    try:
        engine = create_engine(
            DATABASE_URL, **engine_args
        )
        # Test connection - Sử dụng text() để tạo câu lệnh SQL có thể thực thi
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection established successfully")
        break
    except Exception as e:
        if attempt < max_retries - 1:
            logger.warning(f"Database connection attempt {attempt+1} failed: {e}. Retrying in {retry_delay}s...")
            time.sleep(retry_delay)
            retry_delay *= 2  # Exponential backoff
        else:
            logger.error(f"Failed to connect to database after {max_retries} attempts: {e}")
            raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Add SQLite specific configurations only if using SQLite
if DATABASE_URL.startswith("sqlite"):
    from sqlalchemy import event
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e: # Catch any exception to trigger a rollback
        logger.error(f"Database error: {e}")
        db.rollback()
        raise # Re-raise the exception to be handled by FastAPI
    finally:
        db.close()
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

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

engine = create_engine(
    DATABASE_URL, **engine_args
)
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
    except Exception: # Catch any exception to trigger a rollback
        db.rollback()
        raise # Re-raise the exception to be handled by FastAPI
    finally:
        db.close()
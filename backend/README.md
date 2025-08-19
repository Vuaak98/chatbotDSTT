# 🚀 Backend README - Trợ Lý Học Toán

## 📋 Tổng quan

Backend của Trợ Lý Học Toán được xây dựng với FastAPI, tích hợp Google Gemini LLM và RAG system tiên tiến. Hệ thống hỗ trợ xử lý toán học, semantic search, và context-aware responses.

## 🏗️ Cấu trúc thư mục backend

```
backend/
│
├── app/                    # Code chính của ứng dụng
│   ├── __init__.py
│   ├── main.py            # FastAPI application entry point
│   ├── config.py          # Cấu hình ứng dụng
│   ├── database.py        # Database connection và models
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas
│   ├── services.py        # Business logic services
│   ├── adapters/          # Service adapters
│   ├── crud/              # Database CRUD operations
│   ├── middleware/        # Custom middleware
│   ├── rag/               # RAG system components
│   │   ├── rag_service.py
│   │   ├── qdrant_connector.py
│   │   ├── retriever_semantic.py
│   │   └── context_builder.py
│   ├── routers/           # API route handlers
│   ├── services/          # Core services
│   │   ├── llm/           # LLM integration
│   │   ├── embeddings/    # Vector embeddings
│   │   └── rag_integration.py
│   └── utils/             # Utility functions
├── data_ingestion/         # Data processing pipelines
├── migrations/             # Database migrations (Alembic)
├── requirements.txt        # Python dependencies
├── alembic.ini            # Alembic configuration
├── .env.example           # Environment variables template
├── Dockerfile             # Docker configuration
└── README.md              # Hướng dẫn này
```

## 🔧 Cài đặt môi trường

### 1. Cài đặt dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Cấu hình biến môi trường
Copy `.env.example` thành `.env` và cập nhật:
```env
# Gemini API
GOOGLE_API_KEY=your_gemini_api_key_here

# Database
DATABASE_URL=sqlite:///./aichatbot.db

# Qdrant Vector Database
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION=math_problems

# Security
SECRET_KEY=your_secret_key_here
```

### 3. Khởi tạo database
```bash
# Chạy migrations
alembic upgrade head

# Hoặc sử dụng script
python migrate.py
```

## 🚀 Khởi chạy ứng dụng

### Development mode
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production mode
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Docker
```bash
docker build -t ai-math-chatbot-backend .
docker run -p 8000:8000 ai-math-chatbot-backend
```

## 📚 API Documentation

Sau khi khởi chạy, truy cập:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Endpoints chính
- `POST /chat/` - Chat với LLM
- `POST /chat/stream` - Streaming chat
- `POST /files/upload` - Upload file
- `GET /chat/history` - Lịch sử chat
- `POST /rag/search` - RAG search
- `GET /rag/health` - Health check

## 🧠 RAG System

### Components
- **RAGService**: Core logic cho retrieval và generation
- **QdrantConnector**: Kết nối vector database
- **SemanticRetriever**: Semantic search với embeddings
- **ContextBuilder**: Xây dựng context từ retrieved documents

### Usage
```python
from app.rag.rag_service import RAGService

rag_service = RAGService()

# Get context
context, success = await rag_service.get_context(
    query="giải phương trình bậc 2",
    problem_only=True
)

# Generate response
response = await rag_service.generate_response(
    query="giải phương trình bậc 2",
    context=context
)
```

## 📊 Database

### Models
- **Chat**: Lưu trữ lịch sử chat
- **Message**: Tin nhắn trong chat
- **File**: Thông tin file đã upload
- **MessageFile**: Liên kết message và file

### Migrations
Sử dụng Alembic để quản lý database schema:
```bash
# Tạo migration mới
alembic revision --autogenerate -m "Description"

# Áp dụng migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## 🔍 Testing

### Unit Tests
```bash
# Chạy tất cả tests
pytest

# Chạy tests cụ thể
pytest tests/test_rag.py
```

### Integration Tests
```bash
# Test RAG pipeline
python -m pytest tests/test_integration.py -v
```

## 📈 Monitoring & Logging

### Logging
```python
import logging

logger = logging.getLogger(__name__)
logger.info("RAG query processed successfully")
logger.error("Failed to connect to Qdrant")
```

### Health Checks
- Database connection
- Qdrant connection
- Gemini API availability
- Memory usage

## 🐳 Docker

### Build
```bash
docker build -t ai-math-chatbot-backend .
```

### Run
```bash
docker run -d \
  --name math-chatbot-backend \
  -p 8000:8000 \
  --env-file .env \
  ai-math-chatbot-backend
```

### Docker Compose
```bash
docker-compose up -d backend
```

## 🔧 Development

### Code Style
- Sử dụng **Black** cho code formatting
- **isort** cho import sorting
- **flake8** cho linting

### Pre-commit hooks
```bash
# Cài đặt pre-commit
pip install pre-commit
pre-commit install

# Chạy manual
pre-commit run --all-files
```

### Adding new features
1. Tạo model trong `app/models.py`
2. Tạo schema trong `app/schemas.py`
3. Tạo CRUD operations trong `app/crud/`
4. Tạo router trong `app/routers/`
5. Thêm tests
6. Cập nhật documentation

## 🚨 Troubleshooting

### Common Issues

#### 1. Qdrant Connection Error
```bash
# Kiểm tra Qdrant status
python -c "from app.rag.qdrant_connector import QdrantConnector; print(QdrantConnector().health_check())"
```

#### 2. Database Migration Issues
```bash
# Reset database
rm aichatbot.db
alembic upgrade head
```

#### 3. Import Errors
```bash
# Kiểm tra PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

## 📚 Tài liệu tham khảo

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)

## 🤝 Contributing

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## 📞 Liên hệ

- **GitHub:** [EvanGks](https://github.com/EvanGks)
- **Email:** [evangks88@gmail.com](mailto:evangks88@gmail.com)

---

**Backend AI Math Chatbot với RAG system đã sẵn sàng cho production! 🚀✨**
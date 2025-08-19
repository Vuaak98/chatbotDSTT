# 🚀 HƯỚNG DẪN CẤU TRÚC MỚI - AI MATH CHATBOT

## 📋 Tổng quan

Hệ thống AI Math Chatbot đã được cập nhật với cấu trúc dữ liệu mới và RAG system tiên tiến, hỗ trợ các field:
- `category`: dethi, baitap
- `subcategory`: bangA, bangB, gtr, hpt, dstuyentinh
- `subject_area`: dai_so_tuyen_tinh, giai_tich, hinh_hoc, xac_suat_thong_ke
- `difficulty_level`: co_ban, trung_binh, kho, quoc_gia
- `problem_type`: dethi, baitap, thuchanh

## 🔄 Các thay đổi chính

### 1. MetadataExtractor (✅ Đã cập nhật)

**File:** `backend/app/services/llm/metadata_extractor.py`

**Thay đổi:**
- Thêm các field mới vào `MathQueryMetadata`
- Cập nhật prompt để extract cấu trúc mới
- Giữ backward compatibility với cấu trúc cũ
- Tích hợp với RAG system

**Ví dụ sử dụng:**
```python
from app.services.llm.metadata_extractor import MetadataExtractor

extractor = MetadataExtractor()
metadata = await extractor.extract_metadata("Cho tôi bài 1 đề thi bảng A về ma trận")

# Cấu trúc mới
print(metadata.category)        # "dethi"
print(metadata.subcategory)    # "bangA"
print(metadata.subject_area)   # "dai_so_tuyen_tinh"

# Cấu trúc cũ (vẫn hoạt động)
print(metadata.level)          # "a"
print(metadata.year)           # 2024 (nếu có)
```

### 2. RAG System (✅ Đã hoàn thiện)

**Files:**
- `backend/app/rag/rag_service.py` - Core RAG logic
- `backend/app/rag/qdrant_connector.py` - Vector database connection
- `backend/app/rag/retriever_semantic.py` - Semantic search
- `backend/app/rag/context_builder.py` - Context building

**Tính năng:**
- Retrieval-Augmented Generation với Qdrant
- Semantic search thông minh
- Metadata filtering nâng cao
- Context building tự động
- Integration với Gemini LLM

**Ví dụ sử dụng:**
```python
from app.rag.rag_service import RAGService

rag_service = RAGService()

# Tìm kiếm với RAG
context, success = await rag_service.get_context(
    query="giải phương trình bậc 2",
    problem_only=True
)

# Generate response với context
response = await rag_service.generate_response(
    query="giải phương trình bậc 2",
    context=context
)
```

### 3. Data Pipeline (✅ Đã hoàn thiện)

**Files:**
- `data/scripts/final_md_to_json_processor.py` - Markdown → JSON
- `data/scripts/import_to_qdrant_hybrid.py` - Upload to Qdrant
- `data/scripts/smart_latex_translator.py` - LaTeX translation

**Workflow:**
```
Markdown Files → JSON Processing → Vector Embeddings → Qdrant Storage
```

### 4. MathProblemTemplates (✅ Mới tạo)

**File:** `backend/app/services/llm/prompt_templates.py`

**Chức năng:**
- Format context từ documents với cấu trúc mới
- Hỗ trợ cả problem_statement và page_content
- Hiển thị metadata phong phú (difficulty, subject_area, etc.)
- Template cho search summary và no results message
- Integration với RAG system

**Ví dụ sử dụng:**
```python
from app.services.llm.prompt_templates import MathProblemTemplates

# Format context
formatted = MathProblemTemplates.format_problem_context(documents, problem_only=False)

# Format search summary
summary = MathProblemTemplates.format_search_summary(query, documents, metadata)
```

### 5. QdrantConnector (✅ Đã hoàn thiện)

**File:** `backend/app/rag/qdrant_connector.py`

**Trạng thái:** 
- Hỗ trợ filter tổng quát với các field mới
- Vector search với embeddings
- Metadata filtering nâng cao
- Batch operations cho data upload

## 🔗 Mapping cấu trúc cũ sang mới

| Cấu trúc cũ | Cấu trúc mới |
|-------------|--------------|
| `level: "a"` | `category: "dethi", subcategory: "bangA"` |
| `level: "b"` | `category: "dethi", subcategory: "bangB"` |
| `topic: "đề thi bảng A"` | `category: "dethi", subcategory: "bangA"` |
| `tags: ["ma trận"]` | `subject_area: "dai_so_tuyen_tinh"` |

## 🚀 Cách sử dụng hệ thống mới

### 1. Khởi tạo RAG Service
```python
from app.rag.rag_service import RAGService
from app.services.llm.metadata_extractor import MetadataExtractor

# Khởi tạo services
rag_service = RAGService()
metadata_extractor = MetadataExtractor()
```

### 2. Xử lý query với metadata
```python
# Extract metadata
metadata = await metadata_extractor.extract_metadata(
    "Cho tôi bài tập về ma trận khó"
)

# Sử dụng RAG để tìm kiếm
context, success = await rag_service.get_context(
    query="Cho tôi bài tập về ma trận khó",
    metadata=metadata,
    problem_only=True
)
```

### 3. Generate response
```python
# Generate response với context
response = await rag_service.generate_response(
    query="Cho tôi bài tập về ma trận khó",
    context=context,
    metadata=metadata
)
```

## 📊 Cấu trúc dữ liệu mới

### Document Schema
```json
{
  "id": "unique_id",
  "content": "Nội dung bài tập/lời giải",
  "metadata": {
    "category": "dethi|baitap",
    "subcategory": "bangA|bangB|gtr|hpt|dstuyentinh",
    "subject_area": "dai_so_tuyen_tinh|giai_tich|hinh_hoc|xac_suat_thong_ke",
    "difficulty_level": "co_ban|trung_binh|kho|quoc_gia",
    "problem_type": "dethi|baitap|thuchanh",
    "year": 2024,
    "source": "Olympic Bách Khoa"
  },
  "vector": [0.1, 0.2, ...],
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Filter Examples
```python
# Filter theo category và difficulty
filters = {
    "category": "baitap",
    "difficulty_level": "kho"
}

# Filter theo subject area
filters = {
    "subject_area": "dai_so_tuyen_tinh"
}

# Filter kết hợp
filters = {
    "category": "dethi",
    "subcategory": "bangA",
    "subject_area": "giai_tich"
}
```

## 🔧 Cấu hình hệ thống

### Environment Variables
```env
# Qdrant Configuration
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION=math_problems

# Gemini API
GOOGLE_API_KEY=your_api_key_here

# Database
DATABASE_URL=sqlite:///./aichatbot.db
```

### Docker Compose
```yaml
version: '3.8'
services:
  qdrant:
    image: qdrant/qdrant
    ports:
      - "6333:6333"
    volumes:
      - qdrant_storage:/qdrant/storage

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - qdrant
```

## 📈 Performance & Monitoring

### Metrics
- Query response time
- Context retrieval accuracy
- Vector search performance
- Memory usage

### Logging
```python
import logging

logger = logging.getLogger(__name__)
logger.info(f"RAG query processed: {query}")
logger.info(f"Context retrieved: {len(context)} documents")
```

## 🎯 Roadmap tương lai

### Giai đoạn ngắn hạn
- [ ] Performance optimization
- [ ] Advanced filtering
- [ ] Caching layer

### Giai đoạn trung hạn
- [ ] Multi-language support
- [ ] Advanced analytics
- [ ] A/B testing framework

### Giai đoạn dài hạn
- [ ] Cloud deployment
- [ ] Auto-scaling
- [ ] Advanced ML models

---

**Hệ thống AI Math Chatbot với RAG system đã sẵn sàng cho production! 🚀✨**
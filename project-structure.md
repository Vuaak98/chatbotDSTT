# 📁 Cấu trúc dự án Chatbot Toán AI

Tài liệu này mô tả cấu trúc chi tiết của dự án Chatbot Toán AI – một ứng dụng full-stack chất lượng portfolio, trình diễn kỹ năng AI và hỗ trợ toán học qua giao diện chat hiện đại.

## 🎯 Tổng quan dự án

Dự án gồm 2 thành phần chính:
1. **Backend**: API server Python (FastAPI), tích hợp Google Gemini LLM và RAG system
2. **Frontend**: Web app React (Next.js), UI responsive, dễ truy cập

## 📂 Sơ đồ thư mục chi tiết

```
ai-math-chatbot-main/
├── 📄 .gitignore                # Quy tắc ignore Git
├── 📄 README.md                 # Tài liệu dự án chính
├── 📄 project-structure.md      # Tài liệu cấu trúc dự án (này)
├── 📄 aichatbot.db              # CSDL SQLite
├── 📄 docker-compose.yml        # Cấu hình Docker Compose
├── 📁 docs/                     # Tài liệu, quy tắc, tham khảo
│   ├── 📄 gemini_api_doc.md
│   ├── 📄 AI_ Math_Chatbot_Development_Roadmap.md
│   ├── 📄 AI-MATH-CHATBOT-PRD.md
│   ├── 📄 Global_Rules.md
│   └── 📄 Project_Rules.md
├── 📁 assets/                   # Ảnh demo, screenshot
│   ├── 📄 demo.png
│   ├── 📄 file_upload_demo.png
│   ├── 📄 Initial_page_dark_mode.png
│   ├── 📄 Initial_page_light_mode.png
├── 📁 backend/                  # Backend FastAPI
│   ├── 📄 .gitignore
│   ├── 📄 Dockerfile
│   ├── 📄 README.md
│   ├── 📄 alembic.ini
│   ├── 📄 aichatbot.db
│   ├── 📄 db_manager.py
│   ├── 📄 migrate.py
│   ├── 📄 requirements.txt
│   ├── 📄 env.example          # Mẫu biến môi trường
│   ├── 📁 app/                  # Code chính
│   │   ├── 📄 __init__.py
│   │   ├── 📄 cleanup_tasks.py
│   │   ├── 📄 config.py
│   │   ├── 📄 database.py
│   │   ├── 📄 main.py           # Entry point
│   │   ├── 📄 models.py
│   │   ├── 📄 schemas.py
│   │   ├── 📄 seed_db.py
│   │   ├── 📄 services.py
│   │   ├── 📄 tasks.py
│   │   ├── 📁 adapters/         # Service adapters
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 services_adapter.py
│   │   │   └── 📄 streaming_adapter.py
│   │   ├── 📁 config/           # Configuration
│   │   │   └── 📄 __init__.py
│   │   ├── 📁 crud/             # CRUD DB operations
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 chat_crud.py
│   │   │   ├── 📄 file_crud.py
│   │   │   └── 📄 message_crud.py
│   │   ├── 📁 middleware/       # Middleware
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 error_handler.py
│   │   │   ├── 📄 error_utils.py
│   │   │   ├── 📄 exception_handlers.py
│   │   │   ├── 📄 rate_limiter.py
│   │   │   └── 📄 README.md
│   │   ├── 📁 rag/              # RAG system - Core feature
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📁 config/
│   │   │   │   └── 📄 __init__.py
│   │   │   ├── 📄 context_builder.py
│   │   │   ├── 📄 full_pipeline_test.py
│   │   │   ├── 📄 manual_smoke_test.py
│   │   │   ├── 📁 prompts/
│   │   │   │   ├── 📄 __init__.py
│   │   │   │   └── 📄 templates.py
│   │   │   ├── 📄 qdrant_connector.py
│   │   │   ├── 📄 query_extractor_vn.py
│   │   │   ├── 📄 rag_service.py
│   │   │   └── 📄 retriever_semantic.py
│   │   ├── 📁 routers/          # API routes
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 chat_router.py
│   │   │   ├── 📄 file_router.py
│   │   │   ├── 📄 message_router.py
│   │   │   ├── 📄 streaming_router.py
│   │   │   ├── 📄 rag_router.py
│   │   │   └── 📄 README_FILE_UPLOAD.md
│   │   ├── 📁 services/         # Business logic
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📁 embeddings/
│   │   │   ├── 📁 llm/
│   │   │   │   ├── 📄 __init__.py
│   │   │   │   ├── 📄 base.py
│   │   │   │   ├── 📄 gemini_service.py
│   │   │   │   ├── 📄 metadata_extractor.py
│   │   │   │   ├── 📄 openai_service.py
│   │   │   │   └── 📄 prompt_templates.py
│   │   │   ├── 📄 openai_integration.py
│   │   │   ├── 📄 rag_integration.py
│   │   │   └── 📄 topic_classifier.py
│   │   └── 📁 utils/            # Utilities
│   │       ├── 📄 __init__.py
│   │       ├── 📄 sanitizer.py
│   │       └── 📄 README.md
│   ├── 📁 data_ingestion/       # Data processing
│   │   ├── 📄 __init__.py
│   │   ├── 📄 main.py
│   │   └── 📁 pipelines/
│   │       ├── 📄 __init__.py
│   │       └── 📄 text_loader.py
│   ├── 📁 migrations/           # Database migrations
│   │   ├── 📄 env.py
│   │   ├── 📄 script.py.mako
│   │   ├── 📄 README
│   │   └── 📁 versions/
│   │       ├── 📄 57fce4e59ffd_apply_recent_model_changes.py
│   │       ├── 📄 8f928dbf8482_add_message_files_table_and_permanent_.py
│   │       ├── 📄 b3f8436f0f59_apply_recent_model_changes.py
│   │       └── 📄 deea166656d4_initial_migration.py
│   └── 📄 NEW_STRUCTURE_GUIDE.md
├── 📁 data/                     # Data files và scripts - Core feature
│   ├── 📁 scripts/              # Data processing scripts
│   │   ├── 📄 README_USAGE.md   # Hướng dẫn upload Qdrant
│   │   ├── 📄 final_md_to_json_processor.py
│   │   ├── 📄 import_to_qdrant_hybrid.py
│   │   ├── 📄 qdrant_smoke_check.py
│   │   └── 📄 smart_latex_translator.py
│   ├── 📁 raw/                  # Raw data files
│   │   ├── 📁 2018/
│   │   │   ├── 📁 BT/           # Bài tập
│   │   │   └── 📁 LG/           # Lời giải
│   │   └── 📁 2024/
│   │       ├── 📁 BT/           # Bài tập
│   │       └── 📁 LG/           # Lời giải
│   └── 📁 processed/            # Processed data
│       ├── 📁 final/
│       │   ├── 📁 2018/
│       │   │   ├── 📁 baitap/
│       │   └── 📁 dethi/
│       │   └── 📁 2024/
│       │       ├── 📁 baitap/
│       │       └── 📁 dethi/
│       └── 📄 processing_summary.json
└── 📁 frontend/                 # Frontend Next.js
    ├── 📄 .gitignore
    ├── 📄 Dockerfile
    ├── 📄 README.md
    ├── 📄 package.json
    ├── 📄 package-lock.json
    ├── 📄 pnpm-lock.yaml
    ├── 📄 next.config.mjs
    ├── 📄 postcss.config.mjs
    ├── 📄 tailwind.config.ts
    ├── 📄 tsconfig.json
    ├── 📄 components.json
    ├── 📁 app/                  # Next.js app directory
    │   ├── 📄 globals.css
    │   ├── 📄 layout.tsx
    │   └── 📄 page.tsx
    ├── 📁 components/           # React components
    │   ├── 📄 chat-input.tsx
    │   ├── 📄 chat-message.tsx
    │   ├── 📄 markdown-renderer.tsx
    │   ├── 📄 mode-toggle.tsx
    │   ├── 📄 sidebar.tsx
    │   ├── 📄 theme-provider.tsx
    │   ├── 📄 topic-selector.tsx
    │   └── 📁 ui/               # UI components
    │       ├── 📄 accordion.tsx
    │       ├── 📄 alert-dialog.tsx
    │       ├── 📄 alert.tsx
    │       ├── 📄 animated-text.tsx
    │       ├── 📄 aspect-ratio.tsx
    │       ├── 📄 avatar.tsx
    │       ├── 📄 badge.tsx
    │       ├── 📄 breadcrumb.tsx
    │       ├── 📄 button.tsx
    │       ├── 📄 calendar.tsx
    │       ├── 📄 card.tsx
    │       ├── 📄 carousel.tsx
    │       ├── 📄 chart.tsx
    │       ├── 📄 checkbox.tsx
    │       ├── 📄 collapsible.tsx
    │       ├── 📄 command.tsx
    │       ├── 📄 context-menu.tsx
    │       ├── 📄 dialog.tsx
    │       ├── 📄 drawer.tsx
    │       ├── 📄 dropdown-menu.tsx
    │       ├── 📄 form.tsx
    │       ├── 📄 hover-card.tsx
    │       ├── 📄 input-otp.tsx
    │       ├── 📄 input.tsx
    │       ├── 📄 label.tsx
    │       ├── 📄 menubar.tsx
    │       ├── 📄 navigation-menu.tsx
    │       ├── 📄 pagination.tsx
    │       ├── 📄 popover.tsx
    │       ├── 📄 progress.tsx
    │       ├── 📄 radio-group.tsx
    │       ├── 📄 resizable.tsx
    │       ├── 📄 scroll-area.tsx
    │       ├── 📄 select.tsx
    │       ├── 📄 separator.tsx
    │       ├── 📄 sheet.tsx
    │       ├── 📄 sidebar.tsx
    │       ├── 📄 skeleton.tsx
    │       ├── 📄 slider.tsx
    │       ├── 📄 switch.tsx
    │       ├── 📄 table.tsx
    │       ├── 📄 tabs.tsx
    │       ├── 📄 textarea.tsx
    │       ├── 📄 toast.tsx
    │       ├── 📄 toaster.tsx
    │       ├── 📄 toggle-group.tsx
    │       ├── 📄 toggle.tsx
    │       ├── 📄 tooltip.tsx
    │       └── 📄 use-mobile.tsx
    ├── 📁 hooks/                # Custom hooks
    │   ├── 📄 use-media-query.ts
    │   ├── 📄 use-mobile.tsx
    │   └── 📄 use-toast.ts
    ├── 📁 lib/                  # Utilities và services
    │   ├── 📄 api-config.ts
    │   ├── 📄 api-service.ts
    │   ├── 📄 store.ts
    │   ├── 📄 types.ts
    │   └── 📄 utils.ts
    ├── 📁 public/               # Static assets
    │   ├── 📄 placeholder-logo.png
    │   ├── 📄 placeholder-logo.svg
    │   ├── 📄 placeholder-user.jpg
    │   ├── 📄 placeholder.jpg
    │   └── 📄 placeholder.svg
    └── 📁 styles/               # CSS styles
        └── 📄 globals.css
```

## 🔧 Thành phần chính

### Backend (FastAPI)

- **Framework**: FastAPI - Web framework hiện đại cho API
- **LLM Integration**: Google Gemini Pro API cho xử lý toán học nâng cao
- **RAG System**: Retrieval-Augmented Generation với Qdrant vector database
- **Database**: SQLite với SQLAlchemy ORM và Alembic migrations
- **File Processing**: Hỗ trợ đa định dạng (PDF, DOCX, ảnh, text)
- **Middleware**: Rate limiting, error handling, CORS, logging
- **API Documentation**: Tự động tạo với Swagger UI và ReDoc

### Frontend (Next.js)

- **Framework**: Next.js 14 với App Router
- **UI Library**: React với TypeScript
- **Styling**: Tailwind CSS + Shadcn/ui components
- **Math Rendering**: KaTeX cho hiển thị LaTeX
- **State Management**: Zustand cho quản lý trạng thái
- **Responsive Design**: Tối ưu cho mọi thiết bị
- **Accessibility**: WCAG 2.1 AA compliance

### RAG System (Core Feature)

- **Vector Database**: Qdrant cho semantic search
- **Embeddings**: Text embeddings cho tìm kiếm thông minh
- **Retrieval**: Semantic search với metadata filtering
- **Generation**: LLM responses dựa trên retrieved context
- **Data Pipeline**: Tự động xử lý và upload dữ liệu toán học

### Data Management (Core Feature)

- **Data Processing**: Chuyển đổi Markdown → JSON → Qdrant
- **LaTeX Translation**: Dịch công thức toán học thành tiếng Việt
- **Metadata Extraction**: Thông tin về năm, loại, chủ đề toán học
- **Batch Processing**: Xử lý hàng loạt dữ liệu lớn
- **Quality Control**: Kiểm tra và validate dữ liệu

## 🚀 Thiết lập phát triển

### Yêu cầu hệ thống
- Python 3.9+
- Node.js 18+
- Docker & Docker Compose (khuyến nghị)
- Qdrant vector database

### Biến môi trường
- **Backend**: Copy `.env.example` từ `backend/` và tạo `.env`
- **Frontend**: Sử dụng `.env.local` cho API base URL
- **Qdrant**: Cấu hình host và port trong backend

### Docker Compose
Điều phối cả frontend, backend và Qdrant khi phát triển local:
```bash
docker-compose up -d
```

## 📊 Trạng thái dự án

### ✅ Đã hoàn thành
- Backend API với FastAPI
- Frontend UI với Next.js
- Tích hợp Google Gemini LLM
- Hệ thống chat với streaming
- Upload và xử lý file
- Database với SQLite
- **RAG system hoàn chỉnh** với Qdrant
- **Data pipeline** xử lý và upload dữ liệu
- Docker containerization

### 🚧 Đang phát triển
- Tối ưu hóa RAG system performance
- Cải thiện prompt engineering
- Mở rộng dataset toán học

### 📋 Kế hoạch tương lai
- Unit/Integration/E2E testing
- User authentication system
- Admin dashboard
- Multi-language support
- Mobile application
- Cloud deployment

## 🔍 RAG System Workflow

### 1. Data Ingestion
```
Markdown Files → JSON Processing → Qdrant Upload
```

### 2. Query Processing
```
User Question → Query Extraction → Vector Search → Context Retrieval
```

### 3. Response Generation
```
Retrieved Context + User Question → LLM Processing → AI Response
```

## 📈 Data Pipeline

### Input Sources
- Bài tập toán học (2018, 2024)
- Lời giải chi tiết
- Đề thi Olympic
- Các chủ đề: Đa thức, Định thức, Giải tích, v.v.

### Processing Steps
1. **Markdown Parsing**: Trích xuất nội dung và metadata
2. **LaTeX Translation**: Dịch công thức toán học
3. **JSON Conversion**: Chuẩn hóa dữ liệu
4. **Vector Embedding**: Tạo embeddings cho semantic search
5. **Qdrant Storage**: Upload với metadata phong phú


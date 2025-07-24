# Cấu trúc dự án Chatbot Toán AI

Tài liệu này mô tả cấu trúc dự án Chatbot Toán AI – một ứng dụng full-stack chất lượng portfolio, trình diễn kỹ năng AI và hỗ trợ toán học qua giao diện chat hiện đại.

## Tổng quan dự án

Dự án gồm 2 thành phần chính:
1. **Backend**: API server Python (FastAPI), tích hợp Google Gemini LLM
2. **Frontend**: Web app React (Next.js), UI responsive, dễ truy cập

## Sơ đồ thư mục

```
AI_MATH_CHATBOT/
├── .gitignore                # Quy tắc ignore Git
├── LICENSE                   # Giấy phép MIT
├── README.md                 # Tài liệu dự án
├── project-structure.md      # Tài liệu cấu trúc dự án
├── aichatbot.db              # CSDL SQLite
├── docker-compose.yml        # Cấu hình Docker Compose
├── docs/                     # Tài liệu, quy tắc, tham khảo
│   ├── gemini_api_doc.md
│   ├── AI_ Math_Chatbot_Development_Roadmap.md
│   ├── AI-MATH-CHATBOT-PRD.md
│   ├── Global_Rules.md
│   └── Project_Rules.md
├── assets/                   # Ảnh demo, screenshot
│   ├── demo.png
│   ├── file_upload_demo.png
│   ├── Initial_page_dark_mode.png
│   ├── Initial_page_light_mode.png
│   └── voice_input_demo.png
├── backend/                  # Backend
│   ├── .gitignore
│   ├── Dockerfile
│   ├── README.md
│   ├── alembic.ini
│   ├── aichatbot.db
│   ├── db_manager.py
│   ├── migrate.py
│   ├── requirements.txt
│   ├── .env.example          # Mẫu biến môi trường
│   └── app/                  # Code chính
│       ├── __init__.py
│       ├── cleanup_tasks.py
│       ├── config.py
│       ├── database.py
│       ├── main.py           # Entry point
│       ├── models.py
│       ├── schemas.py
│       ├── seed_db.py
│       ├── services.py
│       ├── tasks.py
│       ├── crud/             # CRUD DB
│       │   ├── __init__.py
│       │   ├── chat_crud.py
│       │   └── file_crud.py
│       ├── middleware/       # Middleware
│       │   ├── __init__.py
│       │   ├── error_handler.py
│       │   ├── exception_handlers.py
│       │   ├── error_utils.py
│       │   ├── rate_limiter.py
│       │   └── README.md
│       ├── routers/          # API route
│       │   ├── chat_router.py
│       │   ├── file_router.py
│       │   ├── message_router.py
│       │   ├── streaming_router.py
│       │   └── README_FILE_UPLOAD.md
│       ├── utils/            # Tiện ích
│       │   ├── __init__.py
│       │   ├── sanitizer.py
│       │   └── README.md
│       ├── tests/            # (Chưa triển khai) Test
│       └── migrations/       # Migration DB
│           ├── env.py
│           ├── script.py.mako
│           ├── README
│           └── versions/
├── frontend/                 # Frontend
    ├── .gitignore
    ├── Dockerfile
    ├── README.md
    ├── package.json
    ├── package-lock.json
    ├── pnpm-lock.yaml
    ├── next.config.mjs
    ├── next-env.d.ts
    ├── postcss.config.mjs
    ├── tailwind.config.ts
    ├── tsconfig.json
    ├── .env.local            # Biến môi trường frontend
    ├── .env.example          # Mẫu biến môi trường
    ├── app/                  # Next.js app
    │   ├── globals.css
    │   ├── layout.tsx
    │   └── page.tsx
    ├── components/           # React component
    │   ├── chat-input.tsx
    │   ├── chat-message.tsx
    │   ├── markdown-renderer.tsx
    │   ├── mode-toggle.tsx
    │   ├── sidebar.tsx
    │   ├── theme-provider.tsx
    │   └── ui/               # UI subcomponents
    ├── hooks/                # Custom hook
    │   ├── use-toast.ts
    │   ├── use-media-query.ts
    │   └── use-mobile.tsx
    ├── lib/                  # API, store, utils
    │   ├── api-config.ts
    │   ├── api-service.ts
    │   ├── store.ts
    │   ├── types.ts
    │   └── utils.ts
    ├── public/               # Ảnh tĩnh
    │   ├── placeholder.jpg
    │   ├── placeholder.svg
    │   ├── placeholder-user.jpg
    │   ├── placeholder-logo.svg
    │   └── placeholder-logo.png
    ├── styles/               # CSS
        └── globals.css
```

## Thành phần chính

### Backend

- **FastAPI**: Framework web hiện đại cho API
- **Google Gemini LLM**: Xử lý toán nâng cao, streaming, đa phương thức
- **SQLite**: Lưu lịch sử chat
- **Pydantic**: Quản lý dữ liệu, cấu hình
- **Middleware**: Xử lý request, CORS
- **Xử lý lỗi mạnh mẽ**: Exception handler, logging

### Frontend

- **Next.js & React**: App React server-rendered hiện đại
- **Tailwind CSS**: CSS tiện ích, responsive, dễ truy cập
- **TypeScript**: Kiểu dữ liệu mạnh mẽ
- **KaTeX**: Hiển thị công thức toán
- **Zustand**: Quản lý trạng thái
- **A11y**: Chuẩn WCAG 2.1 AA, HTML ngữ nghĩa, bàn phím
- **Streaming & File Upload**: Phản hồi LLM thời gian thực, upload file nhiều phần

## Thiết lập phát triển

- **Biến môi trường:**
  - Backend: Copy `.env.example` từ `backend/` và tạo `.env`
  - Frontend: Dùng `.env.local` cho API base URL
- **Docker Compose:** Điều phối cả frontend và backend khi phát triển local
- **Kiểm thử:**
  - **Lưu ý:** Unit, integration, E2E test sẽ bổ sung sau. Dự án đã cấu trúc sẵn để dễ tích hợp test (pytest, jest, react-testing-library, Playwright/Cypress).

## Định hướng phát triển

- **Nâng cao toán học:** Tính toán ký hiệu (SymPy), giải phương trình
- **Đăng nhập:** Lưu lịch sử chat, tuỳ chỉnh
- **Dashboard quản trị:** Thống kê, kiểm duyệt
- **Đa ngôn ngữ:** Hỗ trợ nhiều ngôn ngữ
- **Mobile app:** React Native/Flutter
- **A11y nâng cao:** Cải thiện cho screen reader
- **Triển khai cloud:** Một click lên GCP, AWS, Azure
- **Tự động kiểm thử:** CI/CD tích hợp test
- **Plugin:** Mở rộng chatbot bằng plugin
- **Máy tính:** Thêm máy tính cơ bản/khoa học
- **Đồ thị, biểu đồ:** Vẽ đồ thị, biểu đồ từ dữ liệu
- **Vẽ canvas:** Vẽ biểu thức, hình học, đồ thị
- **Kiểm thử:** Bổ sung test các cấp
- **UX/UI:** Cải thiện UI/UX

---

**Dự án này hướng tới chất lượng production, portfolio AI hiện đại.**

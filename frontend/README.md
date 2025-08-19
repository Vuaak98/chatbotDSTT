# 🚀 Trợ Lý Học Toán - Frontend

Đây là **frontend** cho ứng dụng Trợ Lý Học Toán, xây dựng với Next.js 14, React, TypeScript và Tailwind CSS. Giao diện hiện đại, dễ truy cập, đáp ứng tốt cho việc tương tác với trợ lý toán học AI và RAG system.

## 🌟 Tính năng nổi bật

- **Giao diện chat tương tác** với trợ lý toán học AI (phản hồi dạng streaming)
- **RAG System Integration** - Tìm kiếm thông minh với vector database
- **Tải lên file** (PDF, ảnh, file text, Word) với xem trước và xóa (**tối đa 5 file/lần**)
- **Quản lý lịch sử chat** (đa lượt, lưu trữ bền vững)
- **Thiết kế responsive** với chế độ sáng/tối
- **Giao diện dễ truy cập** (chuẩn WCAG 2.1 AA, HTML ngữ nghĩa, điều hướng bàn phím)
- **Hiển thị công thức toán (LaTeX/Math)** với KaTeX
- **Quản lý trạng thái** với Zustand
- **Real-time streaming** responses từ AI

## 👨‍💻 Kỹ thuật & Thực hành hiện đại

- **Next.js 14** với App Router cho performance tối ưu
- **TypeScript** đảm bảo an toàn kiểu dữ liệu, dễ bảo trì
- **Tailwind CSS** cho style tiện lợi, responsive
- **shadcn/ui** cho các thành phần UI dễ truy cập, dễ mở rộng
- **Zustand** quản lý trạng thái linh hoạt
- **Tích hợp API** với backend FastAPI và RAG system
- **A11y:** HTML ngữ nghĩa, ARIA, điều hướng bàn phím, tương phản màu sắc
- **Hiệu năng:** Tách code, tối ưu tài nguyên, giảm kích thước bundle

## 🚀 Bắt đầu sử dụng

### Yêu cầu

- Node.js 18 trở lên
- Backend API đã chạy (xem hướng dẫn backend ở [README chính](../README.md))
- Qdrant vector database (cho RAG system)

### Cài đặt

1. Cài đặt thư viện:

```bash
npm install
# hoặc
yarn install
# hoặc
pnpm install
```

2. Tạo file `.env.local` trong thư mục frontend:

```env
# Địa chỉ API backend
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000

# Qdrant configuration (optional)
NEXT_PUBLIC_QDRANT_HOST=localhost
NEXT_PUBLIC_QDRANT_PORT=6333
```

3. Chạy server phát triển:

```bash
npm run dev
# hoặc
yarn dev
# hoặc
pnpm dev
```

4. Mở [http://localhost:3000](http://localhost:3000) trên trình duyệt.

## 🔗 Kết nối với Backend & RAG System

Frontend giao tiếp với backend qua các endpoint:

### Chat & File Management
- `/chats`, `/chats/{chat_id}`: Quản lý lịch sử chat
- `/chats/{chat_id}/stream`: Nhận phản hồi chat dạng streaming
- `/upload-file`: Tải file (tối đa 5 file/lần)

### RAG System
- `/rag/search`: Tìm kiếm với RAG system
- `/rag/health`: Health check cho RAG system
- `/rag/context`: Lấy context cho câu hỏi

Xem [project-structure.md](../project-structure.md) để biết chi tiết cấu trúc dự án.

## 🧠 RAG System Integration

### Components
- **RAG Search**: Tìm kiếm thông minh trong vector database
- **Context Display**: Hiển thị context được retrieve
- **Semantic Search**: Tìm kiếm dựa trên ý nghĩa, không chỉ từ khóa

### Features
- **Vector Search**: Tìm kiếm với embeddings
- **Metadata Filtering**: Lọc theo category, difficulty, subject area
- **Context Building**: Xây dựng context từ retrieved documents
- **Real-time Results**: Kết quả tìm kiếm tức thì

## 🛠️ Kiến trúc & Tích hợp API

### Core Files
- `lib/api-service.ts`: Hàm API chính cho chat, tải file, RAG search
- `lib/api-config.ts`: Cấu hình API và endpoints
- `lib/store.ts`: Zustand store tích hợp backend và RAG
- `lib/types.ts`: TypeScript types cho API responses

### Components
- `components/chat-input.tsx`: Input cho chat và RAG queries
- `components/chat-message.tsx`: Hiển thị tin nhắn và RAG context
- `components/markdown-renderer.tsx`: Render LaTeX và markdown
- `components/sidebar.tsx`: Quản lý lịch sử chat
- `components/ui/`: Shadcn/ui components

### Hooks
- `hooks/use-toast.ts`: Toast notifications
- `hooks/use-media-query.ts`: Responsive design
- `hooks/use-mobile.tsx`: Mobile detection

## 🧪 Kiểm thử

**Lưu ý:** Frontend sẽ được bổ sung test ở giai đoạn sau. Dự án đã cấu trúc sẵn để dễ tích hợp test:

- `jest` và `react-testing-library` cho test component và tích hợp
- Playwright hoặc Cypress cho test luồng người dùng
- RAG system testing với mock data

## 🏗️ Cấu trúc dự án

```
frontend/
├── app/                    # Next.js App Router
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/             # React components
│   ├── chat-input.tsx     # Chat input component
│   ├── chat-message.tsx   # Message display
│   ├── markdown-renderer.tsx # LaTeX renderer
│   ├── sidebar.tsx        # Chat history sidebar
│   └── ui/                # Shadcn/ui components
├── hooks/                  # Custom React hooks
├── lib/                    # Utilities and services
├── public/                 # Static assets
└── styles/                 # Additional styles
```

Xem [project-structure.md](../project-structure.md) để biết chi tiết frontend và toàn bộ dự án.

## 🏭 Build production

```bash
npm run build
# hoặc
yarn build
# hoặc
pnpm build
```

## 🚢 Triển khai

Frontend có thể triển khai lên Vercel, Netlify hoặc bất kỳ dịch vụ nào hỗ trợ Next.js.

### Environment Variables
```env
# Production
NEXT_PUBLIC_API_BASE_URL=https://your-backend-api.com
NEXT_PUBLIC_QDRANT_HOST=your-qdrant-host.com
NEXT_PUBLIC_QDRANT_PORT=6333
```

### Docker
```bash
# Build image
docker build -t ai-math-chatbot-frontend .

# Run container
docker run -p 3000:3000 ai-math-chatbot-frontend
```

## 🔮 Định hướng phát triển

### Giai đoạn ngắn hạn
- [x] **RAG System Integration** - Tìm kiếm thông minh
- [x] **Real-time Streaming** - Phản hồi tức thì
- [ ] **Advanced Search UI** - Giao diện tìm kiếm nâng cao

### Giai đoạn trung hạn
- **Giao diện máy tính:** Thêm máy tính cơ bản/khoa học
- **Đồ thị, biểu đồ:** Vẽ đồ thị, biểu đồ tương tác từ dữ liệu
- **Vẽ canvas:** Vẽ, chú thích biểu thức toán, hình học, đồ thị
- **Ứng dụng di động:** React Native hoặc PWA cho mobile

### Giai đoạn dài hạn
- **A11y nâng cao:** Cải thiện cho trình đọc màn hình, người dùng đặc biệt
- **Đa ngôn ngữ:** Hỗ trợ nhiều ngôn ngữ
- **Hệ thống plugin:** Cho phép mở rộng chatbot bằng UI plugin
- **Kiểm thử tự động:** Bổ sung test unit/tích hợp/E2E

## 🔧 Development

### Code Style
- **ESLint** cho code quality
- **Prettier** cho code formatting
- **TypeScript strict mode** cho type safety

### Pre-commit hooks
```bash
# Cài đặt husky
npm install -D husky
npx husky install

# Thêm pre-commit hook
npx husky add .husky/pre-commit "npm run lint && npm run type-check"
```

## 🚨 Troubleshooting

### Common Issues

#### 1. API Connection Error
```bash
# Kiểm tra backend status
curl http://localhost:8000/health

# Kiểm tra environment variables
echo $NEXT_PUBLIC_API_BASE_URL
```

#### 2. RAG System Not Working
```bash
# Kiểm tra Qdrant connection
curl http://localhost:6333/health

# Kiểm tra backend RAG endpoints
curl http://localhost:8000/rag/health
```

#### 3. Build Errors
```bash
# Clear cache
rm -rf .next
npm run build
```

## 📚 Tài liệu tham khảo

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Shadcn/ui](https://ui.shadcn.com/)
- [Zustand](https://github.com/pmndrs/zustand)

## 🤝 Contributing

1. Fork repository
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📞 Liên hệ

- **GitHub:** [EvanGks](https://github.com/EvanGks)
- **Email:** [evangks88@gmail.com](mailto:evangks88@gmail.com)

---

**Thể hiện kỹ năng frontend của bạn:** Dự án này hướng tới chất lượng portfolio, sẵn sàng production, là ví dụ điển hình về phát triển ứng dụng web AI hiện đại với RAG system. Rất hoan nghênh đóng góp và phản hồi! 🚀✨ 
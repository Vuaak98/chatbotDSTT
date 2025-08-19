# 🚀 Đặc tả sản phẩm (PRD) - Trợ Lý Học Toán

## 📋 Tổng quan

Trợ Lý Học Toán là một ứng dụng AI tiên tiến tích hợp RAG (Retrieval-Augmented Generation) system, được thiết kế để hỗ trợ học sinh và người đi làm giải các bài toán từ cơ bản đến nâng cao. Ứng dụng sử dụng Google Gemini LLM kết hợp với vector database để cung cấp câu trả lời chính xác và có ngữ cảnh.

## 🎯 Mục tiêu sản phẩm

- **Giải toán thông minh:** Sử dụng RAG system để cung cấp câu trả lời dựa trên dữ liệu toán học thực tế
- **Trải nghiệm người dùng:** Giao diện hiện đại, dễ sử dụng, responsive trên mọi thiết bị
- **Độ chính xác cao:** Kết hợp LLM với vector search để đảm bảo thông tin chính xác
- **Khả năng mở rộng:** Kiến trúc modular, dễ dàng thêm tính năng mới

## 1. 🎭 Luồng trải nghiệm người dùng tổng quan

### **Trạng thái ban đầu:** 
Người dùng truy cập ứng dụng, giao diện chính sạch sẽ, thanh input ở giữa màn hình, hiển thị lời chào ("Hãy hỏi tôi bất cứ điều gì về toán!"). Sidebar bên trái có nút "Chat mới" và danh sách lịch sử chat (ẩn trên mobile, thu gọn mặc định trên desktop).

### **Luồng hỏi đáp bằng text với RAG:**
1. Người dùng nhập câu hỏi toán vào ô input. Input tự co giãn chiều cao, tối đa 200px, sau đó xuất hiện scrollbar.
2. Nhấn nút gửi hoặc Enter để gửi.
3. Nút gửi chuyển thành nút dừng, tin nhắn user hiển thị bên phải (bọc bong bóng).
4. AI hiển thị "Đang suy nghĩ..." bên trái.
5. **RAG System hoạt động:** Tìm kiếm trong vector database để lấy context liên quan.
6. **Context hiển thị:** Hiển thị các bài tập/lời giải liên quan (có thể thu gọn).
7. Phản hồi AI stream từng token vào khung chat (bên trái, không bọc bong bóng, có render công thức KaTeX).
8. Có thể nhấn dừng để ngắt AI.
9. Khi xong, nút dừng trở lại thành nút gửi.

### **Luồng hỏi đáp với file:**
1. Nhấn nút tải file (paperclip), chọn file PDF, ảnh, text, Word.
2. File hiển thị dạng chip trong input, có nút xóa.
3. Nhập câu hỏi liên quan file vào input.
4. Nhấn gửi.
5. Tin nhắn user hiển thị, AI xử lý file (trích text hoặc gửi Gemini), kết hợp với RAG search.
6. Phản hồi AI stream vào chat với context từ file và database.

### **Quản lý lịch sử chat:**
1. Nhấn "Chat mới" để xóa khung chat, bắt đầu mới. Chat cũ lưu vào sidebar.
2. Nhấn vào chat cũ để xem lại lịch sử.
3. Đổi tên/xóa chat qua menu (hover hoặc click, xác nhận khi xóa).

### **Xóa nhanh chat hiện tại:**
1. Nhấn icon thùng rác (góc trên phải).
2. Hiện dialog xác nhận.
3. Xác nhận sẽ xóa khung chat hiện tại (không lưu vào lịch sử).

### **Responsive:**
- **Mobile:** Sidebar ẩn, truy cập qua menu hamburger. Input, chức năng vẫn đầy đủ.
- **Tablet/Desktop:** Sidebar hiện, có thể thu gọn.

## 2. 🎨 Giao diện & style

### **Tổng thể:** 
Tối giản, tập trung nội dung, giống ChatGPT (sáng/tối, font, spacing). **Không cần đăng nhập.**

### **Thành phần:**
- **Khung chính:** Full màn hình.
- **Sidebar:**
  - Cố định desktop (260px), thu gọn được. Off-canvas trên mobile.
  - Có nút "Chat mới", danh sách lịch sử, chuyển theme, cài đặt.
- **Khu vực chat:**
  - Header mỏng trên cùng (chuyển theme, thùng rác, tiêu đề chatbot).
  - Khu vực chat cuộn được.
  - **RAG Context Area:** Hiển thị context được retrieve (có thể thu gọn).
  - Tin nhắn user: căn phải, bọc bong bóng.
  - Tin nhắn AI: căn trái, không bọc bong bóng, text rộng hơn input.
  - Input cố định dưới cùng, gồm: nút tải file, textarea, nút gửi/dừng.

### **Chi tiết style:**
- **Màu sắc:**
  - Sáng: nền trắng, bong bóng xám nhạt, text đen, input trắng.
  - Tối: nền xám đậm, bong bóng xám, input xám, text trắng.
  - Màu nhấn xanh lá/teal nhẹ cho nút, icon, link.
- **Font:** Sans-serif, đồng nhất kích thước.
- **Spacing:** Padding/margin theo lưới 8px, bong bóng chat rộng rãi.
- **Icon:** Bộ icon đồng nhất (Heroicons, Feather Icons).
- **Công thức toán:** KaTeX render LaTeX đẹp, tích hợp mượt trong chat.
- **Code block:** Font mono, highlight, nền riêng, nút copy.
- **RAG Context:** Card design với metadata (năm, loại, độ khó).

## 3. 🚀 Tính năng & tương tác

### **Input:**
- Textarea đa dòng.
- Placeholder động gợi ý ("Giải thích định lý Pytago", "Tìm bài tập về ma trận", ...).
- Nút gửi bật khi có text/file.
- Shift+Enter xuống dòng, Enter gửi (nếu AI đang trả lời thì Enter ngắt).
- Hiển thị file chip khi upload.

### **RAG System Integration:**
- **Semantic Search:** Tìm kiếm dựa trên ý nghĩa, không chỉ từ khóa.
- **Context Display:** Hiển thị các bài tập/lời giải liên quan.
- **Metadata Filtering:** Lọc theo category, difficulty, subject area.
- **Real-time Results:** Kết quả tìm kiếm tức thì.

### **Nút tải file:**
- Mở file picker.
- Nhận `.pdf`, `.png`, `.jpg`, `.jpeg`, `.webp`, `.heic`, `.heif`, `.txt`, `.docx`.
- Hiển thị chip file, có nút xóa.
- Kiểm tra dung lượng, loại file phía client và server.

### **Tin nhắn:**
- User: bọc bong bóng, căn phải, hover hiện nút Copy/Edit/Regenerate.
- AI: text block, căn trái, hover hiện Copy/Regenerate.
- Hỗ trợ markdown, KaTeX, code block có nút copy.
- **RAG Context:** Hiển thị trong tin nhắn AI với metadata.

### **Lịch sử chat:**
- Highlight chat đang chọn.
- Hiển thị tiêu đề rút gọn.
- Đổi tên/xóa chat (hover/click, xác nhận).

### **Loading:** 
Hiện "Đang suy nghĩ..." khi AI trả lời, "Đang tìm kiếm..." khi RAG search.

### **Copy:** 
Khi copy, icon đổi thành tick, hiện toast "Đã copy!".

## 4. 🛡️ Phản hồi & xử lý lỗi

### **Feedback:**
- Gửi: nút gửi thành dừng.
- Loading: "Đang suy nghĩ...", "Đang tìm kiếm context...".
- AI trả lời: stream từng token.
- **RAG Context:** Hiển thị số lượng documents tìm được.
- Tải file: chip file hiện trong input, lỗi hiển thị gần input.
- Copy: icon đổi, toast "Đã copy!".
- Ngắt: dừng AI, nút dừng về gửi.

### **Xử lý lỗi:**
- Lỗi mạng: thông báo rõ, có nút thử lại.
- Lỗi backend/API: thông báo thân thiện, log server. Lỗi Gemini trả về rõ ràng.
- **Lỗi RAG:** "Không tìm thấy context liên quan", "Lỗi kết nối vector database".
- Lỗi file: "File quá lớn", "Loại file không hỗ trợ", "Tải file thất bại", "Không trích xuất được text Word".
- Lỗi input: disable gửi nếu không có text/file. Kiểm tra prompt quá dài.
- Vị trí hiển thị: lỗi input gần input, lỗi chung là toast hoặc AI message.

## 5. ♿ Accessibility (A11y)

### **HTML ngữ nghĩa:** 
Dùng `<nav>`, `<main>`, `<aside>`, `<button>`, `<input>`, `textarea`, heading hợp lý.

### **ARIA Labels:**
- RAG context area: `aria-label="Related mathematical content"`
- Search results: `aria-label="Search results"`
- Context metadata: `aria-label="Content metadata"`

### **Keyboard Navigation:**
- Tab navigation qua tất cả interactive elements
- Enter/Space để activate buttons
- Arrow keys để navigate RAG context

### **Screen Reader Support:**
- Announce RAG search results
- Describe mathematical content
- Provide context information

## 6. 🧠 RAG System Specifications

### **Vector Database:**
- **Qdrant:** Vector database cho semantic search
- **Embeddings:** Text embeddings cho mathematical content
- **Metadata:** Rich metadata cho filtering và context

### **Search Capabilities:**
- **Semantic Search:** Tìm kiếm dựa trên ý nghĩa
- **Metadata Filtering:** Lọc theo category, difficulty, year
- **Hybrid Search:** Kết hợp semantic và keyword search

### **Context Building:**
- **Document Retrieval:** Lấy documents liên quan
- **Context Formatting:** Format context cho LLM
- **Relevance Scoring:** Đánh giá độ liên quan

## 7. 📱 Technical Requirements

### **Frontend:**
- Next.js 14 với App Router
- React 18+ với TypeScript
- Tailwind CSS + Shadcn/ui
- Zustand state management

### **Backend:**
- FastAPI với Python 3.9+
- Google Gemini LLM integration
- Qdrant vector database
- SQLite với SQLAlchemy

### **Performance:**
- **Response Time:** < 2s cho RAG search
- **Streaming:** Real-time AI responses
- **Caching:** Vector search results caching

## 8. 🔮 Future Enhancements

### **Phase 1:**
- [x] RAG System integration
- [x] Vector database setup
- [ ] Advanced search filters

### **Phase 2:**
- [ ] Multi-language support
- [ ] Advanced mathematical visualization
- [ ] User authentication

### **Phase 3:**
- [ ] Mobile app
- [ ] Advanced analytics
- [ ] Plugin system

---

**AI Math Chatbot với RAG system đã sẵn sàng cho production! 🚀✨**

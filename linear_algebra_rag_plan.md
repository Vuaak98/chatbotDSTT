# Kế hoạch tích hợp RAG (Phiên bản cải tiến)

## 1. Tổng quan dự án

Dự án tích hợp kiến trúc RAG (Retrieval-Augmented Generation) vào chatbot toán học hiện có, chuyên biệt hóa thành chatbot đại số tuyến tính Olympic tiếng Việt. Dự án sẽ giữ nguyên cơ sở dữ liệu PostgreSQL, chuyển sang sử dụng OpenAI GPT API, kết nối với Qdrant, và được xây dựng với kiến trúc module hóa, linh hoạt và có khả năng phục hồi cao.

## 2. Mục tiêu

- Chuyển đổi từ Gemini API sang OpenAI GPT API một cách linh hoạt.
- Tích hợp kiến trúc RAG module hóa với cơ chế fallback.
- Chuyên biệt hóa chatbot cho đại số tuyến tính Olympic tiếng Việt, tập trung vào chất lượng dữ liệu.
- Duy trì giao diện người dùng hiện tại, giảm độ trễ cảm nhận.
- Xây dựng hệ thống dễ bảo trì, mở rộng và có khả năng đánh giá định lượng.

## 3. Kiến trúc hệ thống mới

### 3.1. Flow xử lý cải tiến
1.  **User gửi câu hỏi** qua frontend.
2.  **Frontend hiển thị ngay lập tức** thông báo: "Đang tìm kiếm trong tài liệu chuyên ngành..."
3.  **Backend (`message_router`)** nhận request.
4.  **Backend (`message_service`)** gọi **`topic_classifier`** để phân loại.
    *   *Giai đoạn đầu:* Dùng regex/keywords.
    *   *Nâng cao:* Dùng mô hình phân loại nhỏ hoặc LLM chi phí thấp.
5.  **Nếu là chủ đề ĐSTT Olympic:**
    *   Gọi **`rag_service.py`** (module độc lập).
    *   `rag_service` truy vấn Qdrant, lấy ngữ cảnh liên quan.
    *   **Cơ chế Fallback:** Nếu Qdrant lỗi hoặc không có kết quả, `rag_service` trả về `None`.
6.  **Backend (`message_service`)** xây dựng prompt cuối cùng:
    *   Nếu có ngữ cảnh từ RAG -> prompt được tăng cường.
    *   Nếu không (do fallback hoặc chủ đề khác) -> prompt thông thường.
7.  **Backend (`message_service`)** gọi **`LLMService`** (lớp trừu tượng đã được cấu hình để dùng `OpenAIService`).
8.  **OpenAI API** trả về kết quả dạng stream cho frontend.
9.  **Lưu lịch sử** vào PostgreSQL.

## 4. Các thành phần cần phát triển

### 4.1. Backend

#### 4.1.1. Cấu trúc thư mục (cập nhật)
```
backend/
├── app/
│   ├── rag/
│   │   ├── config.py
│   │   ├── chunking_strategy.py  # Chiến lược cắt khối (semantic chunking)
│   │   ├── metadata_enricher.py # Làm giàu metadata
│   │   ├── qdrant_connector.py
│   │   └── rag_service.py       # Module RAG độc lập
│   ├── services/
│   │   ├── llm/                  # Thư mục cho các LLM service
│   │   │   ├── base.py           # Lớp trừu tượng LLMService
│   │   │   ├── openai_service.py # Lớp triển khai OpenAI
│   │   │   └── gemini_service.py # (Tùy chọn) Lớp triển khai Gemini
│   │   ├── message_service.py    # Service chính, gọi các service khác
│   │   └── topic_classifier.py # Module phân loại chủ đề
│   └── ... (các thư mục khác)
├── data_ingestion/             # Quy trình nhập liệu tự động
│   ├── main.py
│   └── pipelines/
```

### 4.2. Dữ liệu và Embeddings (Trái tim của RAG)
- **Quy trình nhập liệu (Ingestion Pipeline):** Xây dựng script tự động để:
    - [ ] Tiền xử lý tài liệu (chuẩn hóa, giữ LaTeX).
    - [ ] Áp dụng **Semantic Chunking** (cắt khối theo định lý, ví dụ, bài giải).
    - [ ] Gắn **Metadata chi tiết** (`source`, `chapter`, `topic`, `type`).
    - [ ] Tạo embedding và đẩy vào Qdrant.

## 5. Lộ trình triển khai

### Giai đoạn 1: Thiết lập nền tảng (2-3 ngày)
- [ ] Cập nhật `requirements.txt`.
- [ ] Tạo cấu trúc thư mục RAG và `data_ingestion`.
- [ ] Xây dựng lớp trừu tượng `LLMService` và lớp `OpenAIService`.
- [ ] Chuyển đổi toàn bộ hệ thống sang sử dụng `OpenAIService` (chưa có RAG).

### Giai đoạn 2: Xây dựng Module RAG độc lập (4-5 ngày)
- [ ] Xây dựng quy trình nhập liệu cơ bản, đưa một vài tài liệu mẫu vào Qdrant.
- [ ] Xây dựng `rag_service.py` với logic retrieval và cơ chế fallback.
- [ ] Xây dựng `topic_classifier.py` đơn giản (dùng keywords).

### Giai đoạn 3: Tích hợp và Tối ưu (4-5 ngày)
- [ ] Tích hợp `rag_service` và `topic_classifier` vào `message_service`.
- [ ] Triển khai logic gửi thông báo "Đang tìm kiếm..." từ backend.
- [ ] Tinh chỉnh prompt engineering cho đại số tuyến tính Olympic.
- [ ] Cải thiện quy trình nhập liệu với Semantic Chunking và Metadata.

### Giai đoạn 4: Kiểm thử và Đánh giá (3-4 ngày)
- [ ] Xây dựng **"Bộ câu hỏi Vàng"** (Golden Dataset) cho ĐSTT Olympic.
- [ ] Thực hiện kiểm thử hồi quy (Regression Testing) sau mỗi thay đổi lớn.
- [ ] (Tùy chọn) Tích hợp RAGAs để đánh giá định lượng `faithfulness` và `answer_relevancy`.
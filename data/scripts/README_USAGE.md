# 🚀 AI Math Chatbot - Hướng Dẫn Upload Dữ Liệu Lên Qdrant

## 📁 Tổng Quan Các File Cần Thiết

### 🔧 **Core Files (Files chính để upload dữ liệu)**

#### 1. `final_md_to_json_processor.py` ✨ **Xử lý dữ liệu gốc**
- **Tác dụng:** Chuyển đổi file Markdown thành JSON để import vào Qdrant
- **Input:** Thư mục `data/raw/` chứa các file `.md`
- **Output:** Thư mục `data/processed/final/` chứa các file `.json`
- **Cách dùng:** Chạy để chuẩn bị dữ liệu trước khi upload

#### 2. `import_to_qdrant_hybrid.py` ✨ **Upload dữ liệu lên Qdrant**
- **Tác dụng:** Import dữ liệu đã xử lý vào Qdrant vector database
- **Input:** Các file JSON từ `data/processed/final/`
- **Output:** Collection trong Qdrant với schema tối ưu
- **Cách dùng:** Chạy để tạo/rebuild collection với dữ liệu mới

#### 3. `qdrant_smoke_check.py` ✨ **Kiểm tra kết nối Qdrant**
- **Tác dụng:** Kiểm tra kết nối và trạng thái Qdrant
- **Khi nào dùng:** Trước khi upload để đảm bảo Qdrant hoạt động
- **Cách dùng:** Chạy để verify connection

#### 4. `smart_latex_translator.py` ✨ **Dịch LaTeX thành tiếng Việt**
- **Tác dụng:** Dịch các công thức toán học LaTeX thành tiếng Việt
- **Khi nào dùng:** Khi cần xử lý dữ liệu toán học có LaTeX
- **Cách dùng:** Tích hợp trong pipeline xử lý dữ liệu

---

## 🧠 **RAG System - Retrieval-Augmented Generation**

### **RAG là gì?**
RAG (Retrieval-Augmented Generation) là hệ thống kết hợp:
- **Retrieval**: Tìm kiếm thông tin liên quan từ vector database
- **Generation**: Tạo câu trả lời dựa trên thông tin tìm được

### **Lợi ích của RAG:**
- ✅ **Chính xác hơn**: Dựa trên dữ liệu thực tế thay vì kiến thức chung
- ✅ **Cập nhật**: Luôn có thông tin mới nhất từ dataset
- ✅ **Đáng tin cậy**: Nguồn thông tin rõ ràng, có thể kiểm chứng
- ✅ **Chuyên môn**: Tập trung vào toán học với dataset chuyên biệt

### **Cách RAG hoạt động:**
1. **User hỏi câu hỏi toán học**
2. **System tìm kiếm** trong Qdrant vector database
3. **Retrieve** các bài tập/lời giải liên quan
4. **Combine** với câu hỏi của user
5. **Generate** câu trả lời chi tiết với Gemini LLM

---

## 🎯 **Quy Trình Upload Dữ Liệu Lên Qdrant**

### **Bước 1: Kiểm tra kết nối Qdrant**
```bash
python data/scripts/qdrant_smoke_check.py
```

### **Bước 2: Xử lý dữ liệu gốc (Markdown → JSON)**
```bash
python data/scripts/final_md_to_json_processor.py
```

### **Bước 3: Upload dữ liệu lên Qdrant**
```bash
python data/scripts/import_to_qdrant_hybrid.py
```

---

## 📂 **Cấu Trúc Dữ Liệu**

### **Input (Dữ liệu gốc)**
```
data/raw/
├── 2018/
│   ├── BT/          # Bài tập
│   └── LG/          # Lời giải
└── 2024/
    ├── BT/          # Bài tập
    └── LG/          # Lời giải
```

### **Output (Dữ liệu đã xử lý)**
```
data/processed/final/
├── 2018/
│   ├── baitap/      # Bài tập đã xử lý
│   └── dethi/       # Đề thi đã xử lý
└── 2024/
    ├── baitap/      # Bài tập đã xử lý
    └── dethi/       # Đề thi đã xử lý
```

---

## ⚙️ **Cấu Hình Cần Thiết**

### **1. Qdrant Connection**
- **Host:** localhost (hoặc địa chỉ Qdrant server)
- **Port:** 6333 (default)
- **Collection Name:** math_problems (hoặc tên tùy chọn)

### **2. Dữ liệu cần có**
- File Markdown trong `data/raw/`
- Cấu trúc thư mục theo năm và loại (BT/LG)

### **3. Dependencies**
- Python 3.9+
- Các thư viện trong `requirements.txt` của backend

---

## 🚀 **Quick Start - Upload Dữ Liệu**

```bash
# 1. Kiểm tra Qdrant
python data/scripts/qdrant_smoke_check.py

# 2. Xử lý dữ liệu
python data/scripts/final_md_to_json_processor.py

# 3. Upload lên Qdrant
python data/scripts/import_to_qdrant_hybrid.py
```

**Xong! Dữ liệu đã được upload lên Qdrant! 🎉**

---

## 🔍 **Kiểm Tra RAG System Hoạt Động**

### **1. Test API RAG Search**
```bash
# Gửi request đến backend
curl -X POST "http://localhost:8000/rag/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "giải phương trình bậc 2"}'
```

### **2. Kiểm tra Collection trong Qdrant**
```bash
# Xem thông tin collection
python data/scripts/qdrant_smoke_check.py
```

### **3. Test Chat với RAG**
- Mở frontend tại http://localhost:3000
- Hỏi câu hỏi toán học
- System sẽ tự động sử dụng RAG để trả lời

---

## ❓ **FAQ**

**Q: Tôi cần thay đổi cấu hình Qdrant ở đâu?**
A: Trong file `import_to_qdrant_hybrid.py`, tìm phần cấu hình connection.

**Q: Dữ liệu có bị mất khi upload lại không?**
A: Có thể chọn overwrite hoặc append tùy theo nhu cầu.

**Q: Tôi có thể upload từng phần dữ liệu riêng lẻ không?**
A: Có! Chỉ cần đặt dữ liệu cần upload vào thư mục `data/raw/` tương ứng.

**Q: Làm sao biết upload thành công?**
A: Chạy `qdrant_smoke_check.py` để kiểm tra collection và số lượng documents.

**Q: RAG system có hoạt động ngay sau khi upload không?**
A: Có! Sau khi upload xong, RAG system sẽ tự động sử dụng dữ liệu mới.

**Q: Tôi có thể thêm dữ liệu mới mà không ảnh hưởng dữ liệu cũ không?**
A: Có! Sử dụng append mode để thêm dữ liệu mới vào collection hiện có.

---

## 📊 **Kết Quả Sau Khi Upload**

- **Collection:** math_problems (hoặc tên tùy chọn)
- **Documents:** Số lượng bài tập và lời giải
- **Vectors:** Embeddings cho semantic search
- **Metadata:** Thông tin về năm, loại, chủ đề toán học
- **RAG Ready:** Hệ thống sẵn sàng trả lời câu hỏi toán học

---

## 🔄 **Workflow Hoàn Chỉnh**

```
User Question → RAG System → Qdrant Search → Context Retrieval → LLM Generation → AI Response
```

**Bây giờ bạn có thể sử dụng RAG system để tìm kiếm và trả lời câu hỏi toán học! 🧮✨**

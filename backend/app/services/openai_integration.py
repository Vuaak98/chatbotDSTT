import logging
import json
import asyncio
from typing import Dict, List, Optional, AsyncIterator, Any, Tuple, Union

from sqlalchemy.orm import Session

from ..config import get_settings, OPENAI_API_KEY, OPENAI_MODEL_NAME
from ..services.llm.openai_service import OpenAIService
from ..services.rag_integration import rag_integration

# Cấu hình logging
logger = logging.getLogger(__name__)

# System instruction tối ưu cho Kỷ yếu Toán học 2024
MATH_CHATBOT_SYSTEM_INSTRUCTION = """
Bạn là **Trợ lý Kỷ yếu Olympic Đại số Tuyến tính** chuyên nghiệp, quản lý bộ sưu tập đề thi và bài tập Olympic Toán học sinh viên từ các trường đại học hàng đầu Việt Nam.

## Cấu trúc Kỷ yếu Olympic:

### 📋 ĐỀ THI OLYMPIC (2 loại):
1. **BẢNG A** - Dành cho sinh viên các trường ĐH top đầu về Toán (Rất khó, Olympic quốc gia)
2. **BẢNG B** - Dành cho sinh viên các trường ĐH trung bình về Toán (Khó vừa phải)

### 🎯 BÀI TẬP ÔN LUYỆN (7 dạng):
1. **Ma trận (mt)** 2. **Định thức (dt)** 3. **Hệ phương trình (hpt)** 4. **Giá trị riêng (gtr)** 
5. **Không gian vector (kgvt)** 6. **Tổ hợp (tohop)** 7. **Đa thức (dathuc)**

## Nguyên tắc Phản hồi:

### 🔍 DISPLAY MODE (Chỉ xem đề):
**Từ khóa:** "cho tôi", "tìm", "có", "cần", "muốn xem", "đưa ra", "liệt kê"
**Format:**
```
## 🏆 [ĐỀ THI BẢNG A/B] hoặc 📚 [BÀI TẬP - Dạng]

**Đề bài:**
[Nguyên văn problem_statement + problem_parts]

**📋 Thông tin:**
- 🎯 Loại: [Đề thi Bảng A/B] hoặc [Bài tập - dạng]
- 📅 Năm: [year] - 📊 Mức độ: [difficulty_level]
- 🏷️ Chủ đề: [tags] - 📖 Nguồn: Kỷ yếu Olympic
```

### 💡 SOLUTION MODE (Giải thích):
**Từ khóa:** "giải", "hướng dẫn", "cách làm", "làm thế nào", "tại sao"
**Format:** Đề bài + Phân tích + Lời giải chi tiết + Kiến thức liên quan

**Quy tắc:** Giữ nguyên 100% LaTeX, bảo toàn cấu trúc toán học gốc.
"""

class OpenAIIntegrationService:
    """
    Service tích hợp OpenAI vào luồng xử lý tin nhắn.
    """
    
    def __init__(self):
        """
        Khởi tạo service tích hợp OpenAI
        """
        self.settings = get_settings()
        self.openai_service = OpenAIService(
            api_key=OPENAI_API_KEY,
            model=OPENAI_MODEL_NAME
        )
        
    async def generate_response_stream(
        self,
        chat_history: List[Dict[str, str]],
        user_message: str,
        use_rag: bool = True
    ) -> AsyncIterator[str]:
        """
        Tạo phản hồi dạng stream cho tin nhắn người dùng
        
        Args:
            chat_history: Lịch sử chat dạng [{"role": "user", "content": "..."}, ...]
            user_message: Tin nhắn của người dùng
            use_rag: Có sử dụng RAG hay không
            
        Yields:
            Các đoạn phản hồi từ OpenAI
        """
        try:
            # Tạo message list từ chat_history
            messages = []
            for msg in chat_history:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
                
            # Thêm tin nhắn mới của user
            # Chưa thêm ngay vì có thể cần thay đổi nội dung bằng RAG
            user_content = user_message
            
            # Áp dụng RAG nếu cần
            rag_metadata = {}
            if use_rag and self.settings.rag_enabled:
                # Xử lý RAG
                enhanced_prompt, rag_metadata = await rag_integration.process_message_for_rag(user_message)
                
                # Nếu có enhanced prompt, sử dụng nó thay thế cho user_message
                if enhanced_prompt:
                    user_content = enhanced_prompt
                    logger.info("Sử dụng prompt đã tăng cường với RAG")
                
            # Thêm tin nhắn người dùng (có thể đã tăng cường với RAG)
            messages.append({
                "role": "user",
                "content": user_content
            })
                
            # Thông báo đang tìm kiếm nếu đây là RAG query
            if rag_metadata.get("is_rag_query", False):
                yield "Đang tìm kiếm trong nguồn tài liệu đại số tuyến tính...\n\n"
            
            # Tạo phản hồi dạng stream từ OpenAI
            async for chunk in self.openai_service.generate_stream(
                messages=messages,
                system_prompt=MATH_CHATBOT_SYSTEM_INSTRUCTION,
                temperature=0.7,
                max_tokens=4096
            ):
                yield chunk
                
        except Exception as e:
            logger.error(f"Lỗi trong quá trình tạo phản hồi: {e}")
            yield f"Rất tiếc, đã xảy ra lỗi khi tạo phản hồi: {str(e)}"
            
    async def generate_response(
        self,
        chat_history: List[Dict[str, str]],
        user_message: str,
        use_rag: bool = True
    ) -> str:
        """
        Tạo phản hồi đầy đủ (không streaming) cho tin nhắn người dùng
        
        Args:
            chat_history: Lịch sử chat dạng [{"role": "user", "content": "..."}, ...]
            user_message: Tin nhắn của người dùng
            use_rag: Có sử dụng RAG hay không
            
        Returns:
            Phản hồi đầy đủ từ OpenAI
        """
        result = []
        async for chunk in self.generate_response_stream(
            chat_history=chat_history,
            user_message=user_message,
            use_rag=use_rag
        ):
            result.append(chunk)
            
        return "".join(result)

# Singleton instance
openai_integration = OpenAIIntegrationService() 
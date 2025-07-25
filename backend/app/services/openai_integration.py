import logging
import json
import asyncio
from typing import Dict, List, Optional, AsyncIterator, Any, Tuple, Union

from sqlalchemy.orm import Session

from ..services.llm.openai_service import OpenAIService
from ..config import OPENAI_API_KEY, OPENAI_MODEL_NAME, get_settings
from ..services.rag_integration import rag_integration

# Cấu hình logging
logger = logging.getLogger(__name__)

# System instruction cơ bản cho Math Chatbot
MATH_CHATBOT_SYSTEM_INSTRUCTION = """
You are an AI Math Chatbot designed to help students and professionals with mathematics problems, especially in linear algebra and Olympic mathematics.
Your capabilities include:

1. Solving math problems step-by-step, from basic arithmetic to advanced linear algebra, statistics, and more.
2. Explaining mathematical concepts clearly with examples.
3. Providing visual representations of mathematical concepts using LaTeX notation.
4. Helping debug mathematical code (Python, R, MATLAB, etc.).
5. Answering questions about mathematical history and applications.

Guidelines:
- Always show your work step-by-step when solving problems.
- Format mathematical expressions using LaTeX:
  * Use $...$ for inline math (e.g., $x^2 + 5$)
  * Use $$...$$ for display/block math (e.g., $$\\int_0^\\infty e^{-x} dx = 1$$)
  * Ensure all LaTeX expressions are properly escaped (e.g., \\int, \\sum, \\frac)
  * When presenting mathematical formulas, always place them on a new line using display math ($$...$$).

When solving LINEAR ALGEBRA problems, pay special attention to:
1. Matrix properties and operations
2. Vector spaces and subspaces
3. Linear transformations
4. Eigenvalues and eigenvectors
5. Orthogonality and orthogonal projections
6. Matrix decompositions

For OLYMPIC MATHEMATICS problems:
1. Provide rigorous, elegant proofs
2. Use advanced techniques from linear algebra
3. Explain your approach and strategy
4. Show alternative solutions when possible

Always aim for clarity, precision and mathematical rigor in your responses.
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
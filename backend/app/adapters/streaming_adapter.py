import asyncio
import json
import logging
from typing import Any, AsyncGenerator, Dict, List, Optional, Tuple, Union

from sqlalchemy.orm import Session

from ..config import get_settings
from ..services.llm.openai_service import OpenAIService
from ..services.topic_classifier import topic_classifier
from ..rag.rag_service import RAGService
from ..rag.prompts.templates import linear_algebra_templates

# Configure logging
logger = logging.getLogger(__name__)

class StreamingAdapter:
    """
    Adapter để tích hợp RAG và OpenAI vào luồng streaming hiện tại,
    mà không cần sửa đổi code cũ.
    """
    
    def __init__(self):
        """
        Khởi tạo StreamingAdapter
        """
        self.settings = get_settings()
        self.openai_service = OpenAIService(
            api_key=self.settings.openai_api_key,
            model=self.settings.openai_model_name
        )
        self.rag_service = RAGService()
        
    async def process_with_openai_rag(
        self,
        user_message: str,
        chat_history: List[Dict[str, Any]],
        queue: asyncio.Queue
    ) -> None:
        """
        Xử lý tin nhắn người dùng với OpenAI và RAG, rồi gửi kết quả qua queue
        
        Args:
            user_message: Tin nhắn của người dùng
            chat_history: Lịch sử chat
            queue: Queue để gửi kết quả
        """
        try:
            # 1. Kiểm tra xem có phải câu hỏi đại số tuyến tính không
            is_linear_algebra, topic_metadata = topic_classifier.classify(user_message)
            
            # 2. Nếu không phải ĐSTT, hoặc RAG bị tắt, sử dụng OpenAI thông thường
            if not is_linear_algebra or not self.settings.rag_enabled:
                logger.info(f"Không sử dụng RAG cho tin nhắn này (is_linear_algebra={is_linear_algebra}, rag_enabled={self.settings.rag_enabled})")
                await self._process_with_openai_normal(user_message, chat_history, queue)
                return
                
            # 3. Nếu là ĐSTT và RAG được bật, áp dụng RAG
            logger.info("Áp dụng RAG cho câu hỏi ĐSTT")
            
            # Thông báo đang tìm kiếm
            await queue.put(json.dumps({"text": "Đang tìm kiếm trong tài liệu đại số tuyến tính...\n\n"}))
            
            # Lấy ngữ cảnh từ RAG với trích xuất metadata tự động từ câu truy vấn
            documents, success = await self.rag_service.get_context(
                query=user_message,
                use_query_metadata=True
            )
            
            if not success or not documents:
                logger.info("Không tìm thấy ngữ cảnh phù hợp, sử dụng OpenAI thông thường")
                await self._process_with_openai_normal(user_message, chat_history, queue)
                return
                
            # Ghi log thông tin về tài liệu tìm được
            logger.info(f"Tìm thấy {len(documents)} tài liệu phù hợp:")
            for i, doc in enumerate(documents):
                logger.info(f"Doc #{i+1}: {doc.metadata.get('title', 'Unknown')} - {doc.metadata.get('source', 'Unknown')}")
                
            # Tạo enhanced prompt với ngữ cảnh
            enhanced_prompt = linear_algebra_templates.get_enhanced_prompt(user_message, documents)
            
            # Tạo system prompt phù hợp
            system_prompt = linear_algebra_templates.get_system_prompt(rag_enabled=True)
            
            # Chuẩn bị tin nhắn cho OpenAI
            messages = self._prepare_messages(chat_history, enhanced_prompt)
            
            # Gọi OpenAI và stream kết quả
            async for chunk in self.openai_service.generate_stream(
                messages=messages, 
                system_prompt=system_prompt,
                temperature=0.7
            ):
                await queue.put(json.dumps({"text": chunk}))
                
        except Exception as e:
            logger.error(f"Lỗi trong quá trình xử lý tin nhắn với OpenAI và RAG: {str(e)}", exc_info=True)
            await queue.put(json.dumps({"error": f"Lỗi xử lý: {str(e)}"}))
        finally:
            # Đánh dấu kết thúc stream
            await queue.put("[DONE]")
    
    async def _process_with_openai_normal(
        self,
        user_message: str,
        chat_history: List[Dict[str, Any]],
        queue: asyncio.Queue
    ) -> None:
        """
        Xử lý tin nhắn với OpenAI thông thường (không có RAG)
        
        Args:
            user_message: Tin nhắn của người dùng
            chat_history: Lịch sử chat
            queue: Queue để gửi kết quả
        """
        try:
            # Chuẩn bị system prompt
            system_prompt = linear_algebra_templates.get_system_prompt(rag_enabled=False)
            
            # Chuẩn bị tin nhắn
            messages = self._prepare_messages(chat_history, user_message)
            
            # Gọi OpenAI và stream kết quả
            async for chunk in self.openai_service.generate_stream(
                messages=messages,
                system_prompt=system_prompt,
                temperature=0.7
            ):
                await queue.put(json.dumps({"text": chunk}))
                
        except Exception as e:
            logger.error(f"Lỗi trong quá trình xử lý tin nhắn với OpenAI thông thường: {str(e)}", exc_info=True)
            await queue.put(json.dumps({"error": f"Lỗi xử lý: {str(e)}"}))
        finally:
            # Đánh dấu kết thúc stream
            await queue.put("[DONE]")
    
    def _prepare_messages(
        self, 
        chat_history: List[Dict[str, Any]], 
        user_message: str
    ) -> List[Dict[str, str]]:
        """
        Chuẩn bị danh sách tin nhắn cho OpenAI từ lịch sử chat và tin nhắn người dùng
        
        Args:
            chat_history: Lịch sử chat
            user_message: Tin nhắn mới của người dùng
            
        Returns:
            Danh sách tin nhắn định dạng OpenAI
        """
        # Chuyển đổi lịch sử chat sang định dạng OpenAI
        messages = []
        for msg in chat_history:
            role = msg.get("role", "")
            content = msg.get("content", "")
            
            # Chuyển đổi role để phù hợp với OpenAI
            if role == "ai":
                openai_role = "assistant"
            elif role == "user":
                openai_role = "user"
            else:
                openai_role = role
                
            messages.append({
                "role": openai_role,
                "content": content
            })
            
        # Thêm tin nhắn mới của người dùng
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        return messages

# Singleton instance để sử dụng
streaming_adapter = StreamingAdapter() 
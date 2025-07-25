import logging
from typing import List, Dict, Any, Optional
import os
import openai
from sqlalchemy.orm import Session

from .. import schemas, services
from ..config import get_settings
from ..services.topic_classifier import topic_classifier
from ..rag.rag_service import RAGService
from ..rag.prompts.templates import linear_algebra_templates

# Configure logging
logger = logging.getLogger(__name__)

class ServicesAdapter:
    """
    Adapter để kết nối các services cũ với hệ thống RAG mới
    mà không thay đổi code ban đầu
    """
    
    @staticmethod
    def generate_ai_response(
        chat_history: List[schemas.Message], 
        user_message_content: str,
        current_message_files: Optional[List[schemas.FileMetadataInfo]] = None, 
        db: Session = None
    ) -> str:
        """
        Phiên bản đồng bộ của generate_ai_response sử dụng OpenAI API trực tiếp
        
        Args:
            chat_history: Lịch sử chat
            user_message_content: Nội dung tin nhắn người dùng
            current_message_files: Danh sách file đính kèm (optional)
            db: Database session (optional)
            
        Returns:
            str: Nội dung phản hồi của AI
        """
        logger.info("Sử dụng ServicesAdapter cho generate_ai_response")
        
        try:
            # Lấy cấu hình
            settings = get_settings()
            openai.api_key = settings.openai_api_key
            
            # Kiểm tra xem có phải câu hỏi đại số tuyến tính không
            is_linear_algebra, topic_metadata = topic_classifier.classify(user_message_content)
            
            # Chuẩn bị tin nhắn cho OpenAI
            messages = []
            
            # Thêm system prompt
            system_prompt = linear_algebra_templates.get_system_prompt(rag_enabled=is_linear_algebra and settings.rag_enabled)
            messages.append({
                "role": "system",
                "content": system_prompt
            })
            
            # Thêm lịch sử chat
            for msg in chat_history:
                role = "user" if msg.role == "user" else "assistant"
                messages.append({
                    "role": role,
                    "content": msg.content
                })
            
            user_prompt = user_message_content
            
            # Nếu là câu hỏi ĐSTT và RAG được bật, thì tìm kiếm ngữ cảnh
            if is_linear_algebra and settings.rag_enabled:
                logger.info("Áp dụng RAG cho câu hỏi đại số tuyến tính")
                
                # Tạo RAGService để tìm kiếm ngữ cảnh
                rag_service = RAGService()
                
                # Chạy tìm kiếm ngữ cảnh một cách đồng bộ
                import asyncio
                loop = asyncio.new_event_loop()
                
                # Lấy ngữ cảnh với metadata được trích xuất từ câu truy vấn
                documents, success = loop.run_until_complete(
                    rag_service.get_context(query=user_message_content, use_query_metadata=True)
                )
                loop.close()
                
                if success and documents:
                    logger.info(f"Tìm thấy {len(documents)} tài liệu phù hợp")
                    # Format ngữ cảnh cho prompt
                    context = linear_algebra_templates.format_context(documents)
                    # Tạo enhanced prompt với ngữ cảnh
                    user_prompt = linear_algebra_templates.get_enhanced_prompt_text(user_message_content, context)
                else:
                    logger.info("Không tìm thấy tài liệu phù hợp, sử dụng prompt thông thường")
            
            # Thêm tin nhắn của người dùng
            messages.append({
                "role": "user",
                "content": user_prompt
            })
            
            # Gọi OpenAI API theo cách đồng bộ
            client = openai.OpenAI(api_key=settings.openai_api_key)
            response = client.chat.completions.create(
                model=settings.openai_model_name,
                messages=messages,
                temperature=0.7
            )
            
            # Lấy phản hồi
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Lỗi trong ServicesAdapter.generate_ai_response: {e}", exc_info=True)
            return f"Đã xảy ra lỗi khi tạo phản hồi AI. Chi tiết: {str(e)}"

# "Monkey patch" services.py để thêm hàm generate_ai_response mà không sửa file gốc
if not hasattr(services, "generate_ai_response"):
    services.generate_ai_response = ServicesAdapter.generate_ai_response
    logger.info("Đã thêm generate_ai_response vào module services") 
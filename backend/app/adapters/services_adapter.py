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
            
            # Thử OpenAI trước, fallback sang Gemini nếu lỗi
            try:
                logger.info("Attempting to use OpenAI API...")
                client = openai.OpenAI(api_key=settings.openai_api_key)
                response = client.chat.completions.create(
                    model=settings.openai_model_name,
                    messages=messages,
                    temperature=0.7
                )
                
                # Lấy phản hồi
                return response.choices[0].message.content
                
            except Exception as e:
                logger.error(f"OpenAI API failed: {e}")
                
                # Kiểm tra nếu là lỗi quota (429) thì fallback sang Gemini
                if "429" in str(e) or "quota" in str(e).lower() or "insufficient_quota" in str(e):
                    logger.warning("OpenAI quota exceeded, falling back to Gemini...")
                else:
                    logger.warning(f"OpenAI error: {e}, falling back to Gemini...")
                
                # Fallback sang Gemini
                try:
                    logger.info("Using Gemini API as fallback...")
                    from google import genai
                    
                    # Khởi tạo Gemini client
                    gemini_client = genai.Client(api_key=settings.gemini_api_key)
                    
                    # Chuyển đổi messages format cho Gemini
                    gemini_messages = []
                    for msg in messages:
                        if msg["role"] == "system":
                            # Gemini không có system role, merge vào user message đầu tiên
                            continue
                        elif msg["role"] == "user":
                            content = msg["content"]
                            # Thêm system message vào user message đầu tiên
                            if messages[0]["role"] == "system":
                                content = f"{messages[0]['content']}\n\nUser: {content}"
                            gemini_messages.append({"role": "user", "parts": [{"text": content}]})
                        elif msg["role"] == "assistant":
                            gemini_messages.append({"role": "model", "parts": [{"text": msg["content"]}]})
                    
                    # Gọi Gemini API
                    response = gemini_client.models.generate_content(
                        model=settings.gemini_model_name,
                        contents=gemini_messages,
                        config=genai.GenerateContentConfig(
                            temperature=0.7,
                            max_output_tokens=2048
                        )
                    )
                    
                    return response.text
                    
                except Exception as gemini_error:
                    logger.error(f"Gemini API also failed: {gemini_error}")
                    return "Xin lỗi, có lỗi xảy ra khi xử lý yêu cầu của bạn. Vui lòng thử lại sau."
            
        except Exception as e:
            logger.error(f"Lỗi trong ServicesAdapter.generate_ai_response: {e}", exc_info=True)
            return f"Đã xảy ra lỗi khi tạo phản hồi AI. Chi tiết: {str(e)}"

# Tạo hàm generate_ai_response ở top-level để có thể import trực tiếp
def generate_ai_response(
    chat_history: List[schemas.Message], 
    user_message_content: str,
    current_message_files: Optional[List[schemas.FileMetadataInfo]] = None, 
    db: Session = None
) -> str:
    """
    Wrapper hàm generate_ai_response để import trực tiếp
    """
    return ServicesAdapter.generate_ai_response(
        chat_history, user_message_content, current_message_files, db
    )

# "Monkey patch" services.py để thêm hàm generate_ai_response mà không sửa file gốc
if not hasattr(services, "generate_ai_response"):
    services.generate_ai_response = ServicesAdapter.generate_ai_response
    logger.info("Đã thêm generate_ai_response vào module services") 
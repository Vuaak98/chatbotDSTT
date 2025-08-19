import asyncio
import logging
import traceback
import importlib.util
from typing import Dict, List, Optional, Any, AsyncGenerator
from sqlalchemy.orm import Session

from ..config import get_settings
from ..services.llm.openai_service import OpenAIService
from ..rag.rag_service import RAGService
from ..rag.prompts.templates import LinearAlgebraTemplates
from ..crud import chat_crud, message_crud
from ..database import get_db

logger = logging.getLogger(__name__)

class StreamingAdapter:
    """
    Adapter để kết nối hệ thống streaming cũ với OpenAI và RAG
    """
    
    def __init__(self):
        """
        Khởi tạo các thành phần cần thiết
        """
        self.settings = get_settings()
        
    async def process_with_openai_rag(self, user_message: str, chat_history: List[Dict[str, Any]], queue: asyncio.Queue) -> None:
        """
        Xử lý tin nhắn người dùng với OpenAI và RAG
        
        Args:
            user_message: Tin nhắn người dùng
            chat_history: Lịch sử chat
            queue: Queue để gửi phản hồi
        """
        try:
            # Khởi tạo OpenAI service
            openai_service = OpenAIService(
                api_key=self.settings.openai_api_key,
                model_name=self.settings.openai_model_name
            )
            
            # Tìm kiếm context từ RAG nếu được bật
            system_message = ""
            enhanced_prompt = ""
            
            # Kiểm tra xem người dùng có chỉ muốn xem đề bài không
            problem_only = False
            problem_request_keywords = ["cho tôi một bài tập", "cho tôi bài tập", "cho tôi đề bài", 
                                      "cung cấp bài tập", "cung cấp đề bài", "đề bài", "bài tập", "cho đề"]
            if any(keyword in user_message.lower() for keyword in problem_request_keywords):
                problem_only = True
                logger.info(f"Người dùng chỉ yêu cầu đề bài: {problem_only}")
            
            if self.settings.rag_enabled:
                try:
                    # Khởi tạo RAG service
                    rag_service = RAGService()
                    
                    # Lấy context
                    documents, success = await rag_service.get_context(
                        user_message,
                        use_query_metadata=True
                    )
                    
                    if success and documents:
                        # Tạo prompt với context
                        prompt_templates = LinearAlgebraTemplates()
                        system_message = prompt_templates.get_system_prompt(rag_enabled=True)
                        enhanced_prompt = prompt_templates.get_enhanced_prompt(
                            user_question=user_message,
                            documents=documents
                        )
                    else:
                        system_message = LinearAlgebraTemplates.get_system_prompt(rag_enabled=False)
                        enhanced_prompt = user_message
                except Exception as e:
                    logger.error(f"Error getting RAG context: {e}")
                    system_message = LinearAlgebraTemplates.get_system_prompt(rag_enabled=False)
                    enhanced_prompt = user_message
            else:
                system_message = LinearAlgebraTemplates.get_system_prompt(rag_enabled=False)
                enhanced_prompt = user_message
                
            # Thêm hướng dẫn LaTeX
            latex_preservation_prompt = """
Khi trả lời, hãy LUÔN bảo toàn các ký hiệu toán học LaTeX chính xác như trong dữ liệu gốc.
Đảm bảo mọi biểu thức toán đều được bọc trong $...$ (cho inline) hoặc $$...$$ (cho block).
Tuyệt đối không thay đổi cú pháp LaTeX hay chuyển đổi nó sang văn bản thường.
"""
            system_message += "\n\n" + latex_preservation_prompt
            
            # Stream response từ OpenAI
            async for chunk in openai_service.generate_stream(
                system_message=system_message,
                user_message=enhanced_prompt
            ):
                await queue.put(chunk)
                
            # Đánh dấu kết thúc
            await queue.put("[DONE]")
        except Exception as e:
            logger.error(f"Error in process_with_openai_rag: {e}")
            await queue.put(f"Error: {str(e)}")
            await queue.put("[DONE]")

# Export instance để tương thích với code cũ
streaming_adapter = StreamingAdapter()

async def generate_ai_response_stream_impl(
    chat_id: str, 
    user_message_content: str,
    file_ids: List[str] = None,
    db: Session = None,  # Thêm tham số db
    queue: asyncio.Queue = None,
) -> AsyncGenerator[str, None]:
    """
    Implementation của generate_ai_response_stream sử dụng async generator
    """
    file_ids = file_ids or []
    settings = get_settings()
    
    # Sử dụng db từ tham số nếu được cung cấp, nếu không lấy mới
    if db is None:
        db_generator = get_db()
        db = next(db_generator)
    
    # Initialize RAG service if enabled
    rag_context = ""
    is_linear_algebra_question = True  # Giả định mọi câu đều liên quan đến ĐSTT
    
    # Khởi tạo biến cho system message và enhanced prompt
    system_message = ""
    enhanced_prompt = ""
    
    # Thử lấy context từ RAG nếu được bật
    if settings.rag_enabled and is_linear_algebra_question:
        try:
            logger.info(f"Áp dụng RAG cho câu hỏi ĐSTT")
            rag_service = RAGService()
            
            # Truy vấn context từ RAG với chat history
            documents, success = await rag_service.get_context_with_history(
                user_message_content,
                chat_history=[],  # TODO: Implement chat history properly
                use_query_metadata=True
            )
            
            if success and documents:
                logger.info(f"Tìm thấy {len(documents)} tài liệu liên quan")
                
                # Sử dụng template để định dạng context
                prompt_templates = LinearAlgebraTemplates()
                
                # Log chi tiết về documents tìm thấy với schema mới
                for i, doc in enumerate(documents[:2]):  # Log 2 docs đầu tiên
                    if hasattr(doc, "metadata"):
                        metadata_str = ", ".join([f"{k}={v}" for k, v in doc.metadata.items() 
                                                if k in ["question_number", "category", "subcategory", "year", "title"]])
                        logger.info(f"Doc {i+1} metadata: {metadata_str}")
                    
                    if hasattr(doc, "page_content"):
                        content_preview = doc.page_content[:100].replace("\n", " ")
                        logger.info(f"Doc {i+1} content: {content_preview}...")
                
                # Tạo enhanced prompt với context
                system_message = prompt_templates.get_system_prompt(rag_enabled=True)
                enhanced_prompt = prompt_templates.get_enhanced_prompt(
                    user_question=user_message_content,
                    documents=documents
                )
                
                # Log prompt để debug
                logger.info(f"Enhanced prompt với RAG context được tạo (độ dài: {len(enhanced_prompt)})")
            else:
                logger.info("Không tìm thấy ngữ cảnh phù hợp, sử dụng LLM thông thường")
                system_message = LinearAlgebraTemplates.get_system_prompt(rag_enabled=False)
                enhanced_prompt = user_message_content
        except Exception as e:
            logger.error(f"Error retrieving context: {str(e)}")
            system_message = LinearAlgebraTemplates.get_system_prompt(rag_enabled=False)
            enhanced_prompt = user_message_content
    else:
        logger.info("RAG không được bật, sử dụng LLM thông thường")
        system_message = LinearAlgebraTemplates.get_system_prompt(rag_enabled=False)
        enhanced_prompt = user_message_content
        
    try:
        user_msg_db = chat_crud.create_chat_message(
            db=db,
            chat_id=int(chat_id),
            role="user",
            content=user_message_content
        )
        logger.info(f"User message saved to DB with ID: {user_msg_db.id}")
        
        # Link files if provided
        if file_ids and len(file_ids) > 0:
            for file_id in file_ids:
                message_crud.link_file_to_message(
                    db=db,
                    message_id=user_msg_db.id,
                    file_id=file_id
                )
            logger.info(f"Linked {len(file_ids)} files to message")
    except Exception as e:
        logger.error(f"Failed to save user message or link files: {e}")
        logger.error(traceback.format_exc())
    
    # Khởi tạo AI service với fallback mechanism
    use_openai = settings.use_openai
    logger.info(f"Configuration: use_openai={use_openai}, rag_enabled={settings.rag_enabled}")
    
    # Tạo system prompt đặc biệt để đảm bảo nội dung LaTeX được bảo toàn
    latex_preservation_prompt = """
Khi trả lời, hãy LUÔN bảo toàn các ký hiệu toán học LaTeX chính xác như trong dữ liệu gốc.
Đảm bảo mọi biểu thức toán đều được bọc trong $...$ (cho inline) hoặc $$...$$ (cho block).
Tuyệt đối không thay đổi cú pháp LaTeX hay chuyển đổi nó sang văn bản thường.
Ví dụ: nếu dữ liệu có "\\begin{matrix}", hãy giữ nguyên không thay đổi.
"""
    
    # Thêm vào system_message
    system_message += "\n\n" + latex_preservation_prompt
    
    # Stream generation với fallback mechanism
    ai_message_content = ""
    openai_failed = False
    
    # Thử OpenAI trước nếu được cấu hình
    if use_openai:
        try:
            logger.info("Attempting to use OpenAI service...")
            openai_service = OpenAIService(
                api_key=settings.openai_api_key,
                model_name=settings.openai_model_name
            )
            
            async for chunk in openai_service.generate_stream(
                system_message=system_message,
                user_message=enhanced_prompt
            ):
                ai_message_content += chunk
                if queue:
                    await queue.put(chunk)
                yield chunk
                
        except Exception as e:
            logger.error(f"OpenAI service failed: {e}")
            openai_failed = True
            
            # Kiểm tra nếu là lỗi quota (429) thì fallback sang Gemini
            if "429" in str(e) or "quota" in str(e).lower() or "insufficient_quota" in str(e):
                logger.warning("OpenAI quota exceeded, falling back to Gemini...")
            else:
                logger.warning(f"OpenAI error: {e}, falling back to Gemini...")
    
    # Sử dụng Gemini nếu OpenAI không được cấu hình hoặc failed
    if not use_openai or openai_failed:
        try:
            logger.info("Using Gemini service...")
            from ..services.llm.gemini_service import gemini_stream_handler
            
            await gemini_stream_handler(
                chat_id=chat_id,
                user_message_content=enhanced_prompt,
                system_message=system_message,
                file_ids=file_ids,
                db=db,
                queue=queue
            )
            # Gemini function đã xử lý streaming và lưu DB, không cần yield thêm
            return
            
        except Exception as e:
            logger.error(f"Gemini service also failed: {e}")
            # Fallback to error message
            error_msg = "Xin lỗi, có lỗi xảy ra khi xử lý yêu cầu của bạn. Vui lòng thử lại sau."
            ai_message_content = error_msg
            if queue:
                await queue.put(error_msg)
            yield error_msg
    
    # Lưu AI message vào database
    try:
        # Bổ sung các ký hiệu LaTeX bị thiếu nếu cần
        # Kiểm tra và đảm bảo các dấu $ được đóng mở đúng cặp
        ai_msg_db = chat_crud.create_chat_message(
            db=db,
            chat_id=int(chat_id),
            role="assistant",
            content=ai_message_content
        )
        logger.info(f"AI response saved to DB with ID: {ai_msg_db.id}")
    except Exception as e:
        logger.error(f"Failed to save AI message: {e}")
        logger.error(traceback.format_exc())

# Wrapper coroutine cho asyncio.create_task
async def generate_ai_response_stream(
    chat_id: str, 
    user_message_content: str,
    file_ids: List[str] = None,
    db: Session = None,
    queue: asyncio.Queue = None
) -> None:
    """
    Wrapper để gọi generate_ai_response_stream_impl từ asyncio.create_task
    
    Args:
        chat_id: ID của chat
        user_message_content: Nội dung tin nhắn
        file_ids: Danh sách file IDs
        db: Database session
        queue: Queue để gửi phản hồi
    """
    async_gen = generate_ai_response_stream_impl(
        chat_id=chat_id,
        user_message_content=user_message_content,
        file_ids=file_ids,
        db=db,
        queue=queue
    )
    
    try:
        # Process each yielded chunk
        async for chunk in async_gen:
            # Chunk already sent to queue in the generator
            pass
    except Exception as e:
        logger.error(f"Error in generate_ai_response_stream wrapper: {e}")
        
        # Kiểm tra nếu là lỗi OpenAI quota thì fallback sang Gemini
        if "429" in str(e) or "quota" in str(e).lower() or "insufficient_quota" in str(e):
            logger.warning("OpenAI quota exceeded in wrapper, attempting Gemini fallback...")
            try:
                from ..services.llm.gemini_service import gemini_stream_handler
                
                # Tạo system prompt cơ bản
                from ..rag.prompts.templates import LinearAlgebraTemplates
                system_message = LinearAlgebraTemplates.get_system_prompt(rag_enabled=False)
                
                await gemini_stream_handler(
                    chat_id=chat_id,
                    user_message_content=user_message_content,
                    system_message=system_message,
                    file_ids=file_ids,
                    db=db,
                    queue=queue
                )
                return
                
            except Exception as gemini_error:
                logger.error(f"Gemini fallback also failed: {gemini_error}")
                if queue:
                    await queue.put("Xin lỗi, có lỗi xảy ra khi xử lý yêu cầu của bạn. Vui lòng thử lại sau.")
                    await queue.put("[DONE]")
        else:
            if queue:
                await queue.put(f"Error: {str(e)}")
                await queue.put("[DONE]")

def generate_ai_response(chat_id: int, user_message_content: str, file_ids: List[str] = None) -> str:
    """
    Patched version of generate_ai_response sử dụng OpenAI
    
    Args:
        chat_id: ID của chat
        user_message_content: Nội dung tin nhắn người dùng
        file_ids: Danh sách IDs của các file đính kèm (Optional)
        
    Returns:
        Phản hồi AI
    """
    file_ids = file_ids or []
    settings = get_settings()
    
    # Initialize services với fallback mechanism
    openai_failed = False
    
    # Initialize RAG service if enabled
    system_message = ""
    enhanced_prompt = ""
    is_linear_algebra_question = True  # Giả định mọi câu đều liên quan đến ĐSTT
    
    try:
        if settings.rag_enabled and is_linear_algebra_question:
            logger.info(f"Áp dụng RAG cho câu hỏi ĐSTT")
            
            # Tạo một event loop mới để gọi async RAG service
            rag_service = RAGService()
            
            # Sử dụng phương pháp trực tiếp để lấy context
            new_loop = asyncio.new_event_loop()
            try:
                asyncio.set_event_loop(new_loop)
                documents, success = new_loop.run_until_complete(
                    rag_service.get_context(user_message_content, use_query_metadata=True)
                )
                
                if success and documents:
                    logger.info(f"Tìm thấy {len(documents)} tài liệu liên quan")
                    
                    # Sử dụng template để định dạng context
                    prompt_templates = LinearAlgebraTemplates()
                    
                    # Log chi tiết về documents tìm thấy với schema mới
                    for i, doc in enumerate(documents[:2]):  # Log 2 docs đầu tiên
                        if hasattr(doc, "metadata"):
                            metadata_str = ", ".join([f"{k}={v}" for k, v in doc.metadata.items() 
                                                    if k in ["question_number", "category", "subcategory", "year", "title"]])
                            logger.info(f"Doc {i+1} metadata: {metadata_str}")
                        
                        if hasattr(doc, "page_content"):
                            content_preview = doc.page_content[:100].replace("\n", " ")
                            logger.info(f"Doc {i+1} content: {content_preview}...")
                    
                    # Tạo enhanced prompt với context
                    system_message = prompt_templates.get_system_prompt(rag_enabled=True)
                    enhanced_prompt = prompt_templates.get_enhanced_prompt(
                        user_question=user_message_content,
                        documents=documents
                    )
                    
                    # Log prompt để debug
                    logger.info(f"Enhanced prompt với RAG context được tạo (độ dài: {len(enhanced_prompt)})")
                else:
                    logger.info("Không tìm thấy ngữ cảnh phù hợp, sử dụng OpenAI thông thường")
                    system_message = LinearAlgebraTemplates.get_system_prompt(rag_enabled=False)
                    enhanced_prompt = user_message_content
            finally:
                new_loop.close()
        else:
            logger.info("RAG không được bật, sử dụng OpenAI thông thường")
            system_message = LinearAlgebraTemplates.get_system_prompt(rag_enabled=False)
            enhanced_prompt = user_message_content
    except Exception as e:
        logger.error(f"Lỗi khi sử dụng RAG: {e}")
        system_message = LinearAlgebraTemplates.get_system_prompt(rag_enabled=False)
        enhanced_prompt = user_message_content
    
    # Lưu user message vào database
    db_generator = get_db()
    db = next(db_generator)
    
    try:
        user_msg_db = chat_crud.create_chat_message(
            db=db,
            chat_id=int(chat_id),
            role="user",
            content=user_message_content
        )
        logger.info(f"User message saved to DB with ID: {user_msg_db.id}")
        
        # Link files if provided
        if file_ids and len(file_ids) > 0:
            for file_id in file_ids:
                message_crud.link_file_to_message(
                    db=db,
                    message_id=user_msg_db.id,
                    file_id=file_id
                )
            logger.info(f"Linked {len(file_ids)} files to message")
    except Exception as e:
        logger.error(f"Failed to save user message or link files: {e}")
        logger.error(traceback.format_exc())
    
    # Thêm system prompt đặc biệt để đảm bảo nội dung LaTeX được bảo toàn
    latex_preservation_prompt = """
Khi trả lời, hãy LUÔN bảo toàn các ký hiệu toán học LaTeX chính xác như trong dữ liệu gốc.
Đảm bảo mọi biểu thức toán đều được bọc trong $...$ (cho inline) hoặc $$...$$ (cho block).
Tuyệt đối không thay đổi cú pháp LaTeX hay chuyển đổi nó sang văn bản thường.
Ví dụ: nếu dữ liệu có "\\begin{matrix}", hãy giữ nguyên không thay đổi.
"""
    
    # Thêm vào system_message
    system_message += "\n\n" + latex_preservation_prompt
    
    # Thử OpenAI trước, fallback sang Gemini nếu lỗi
    response = ""
    try:
        logger.info("Attempting to use OpenAI service...")
        openai_service = OpenAIService(
            api_key=settings.openai_api_key,
            model_name=settings.openai_model_name
        )
        
        response = openai_service.generate(
            system_message=system_message,
            user_message=enhanced_prompt
        )
        
    except Exception as e:
        logger.error(f"OpenAI service failed: {e}")
        
        # Kiểm tra nếu là lỗi quota (429) thì fallback sang Gemini
        if "429" in str(e) or "quota" in str(e).lower() or "insufficient_quota" in str(e):
            logger.warning("OpenAI quota exceeded, falling back to Gemini...")
        else:
            logger.warning(f"OpenAI error: {e}, falling back to Gemini...")
        
        # Fallback sang Gemini
        try:
            logger.info("Using Gemini service as fallback...")
            from google import genai
            
            # Khởi tạo Gemini client
            gemini_client = genai.Client(api_key=settings.gemini_api_key)
            
            # Tạo prompt cho Gemini
            full_prompt = f"{system_message}\n\nUser: {enhanced_prompt}"
            
            # Gọi Gemini API
            gemini_response = gemini_client.models.generate_content(
                model=settings.gemini_model_name,
                contents=[{"role": "user", "parts": [{"text": full_prompt}]}],
                config=genai.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=2048
                )
            )
            
            response = gemini_response.text
            
        except Exception as gemini_error:
            logger.error(f"Gemini service also failed: {gemini_error}")
            response = "Xin lỗi, có lỗi xảy ra khi xử lý yêu cầu của bạn. Vui lòng thử lại sau."
    
    # Lưu AI message vào database
    try:
        ai_msg_db = chat_crud.create_chat_message(
            db=db,
            chat_id=int(chat_id),
            role="assistant",
            content=response
        )
        logger.info(f"AI response saved to DB with ID: {ai_msg_db.id}")
    except Exception as e:
        logger.error(f"Failed to save AI message: {e}")
        logger.error(traceback.format_exc())
        
    return response 
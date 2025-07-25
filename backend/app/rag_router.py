import asyncio
import json
import logging
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from . import crud, schemas
from .adapters.streaming_adapter import streaming_adapter
from .config import get_settings
from .database import get_db
from .services.topic_classifier import topic_classifier
from .rag.rag_service import RAGService

# Configure logging
logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/chats/{chat_id}/openai-stream", response_class=StreamingResponse)
async def stream_openai_chat(
    chat_id: int,
    request: Request,
    user_message: str = Query(None),
    file_ids: Optional[List[str]] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Stream chat response using OpenAI and RAG (nếu phù hợp)
    
    Args:
        chat_id: ID của cuộc trò chuyện
        user_message: Nội dung tin nhắn của người dùng
        file_ids: Danh sách ID của các file đính kèm
        
    Returns:
        StreamingResponse: Phản hồi dạng stream
    """
    try:
        logger.info(f"Received OpenAI streaming request for chat_id: {chat_id}")
        logger.info(f"User message content: {user_message}")
        
        # Tạo một ID ngẫu nhiên cho generation này
        generation_id = f"{chat_id}_{hash(user_message + str(asyncio.get_event_loop().time()))}"
        logger.info(f"Generation ID: {generation_id}")
        
        # Tạo queue để chứa các đoạn phản hồi
        queue = asyncio.Queue()
        
        # Lưu tin nhắn người dùng vào DB (nếu có chat_id hợp lệ)
        user_msg_db = None
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                user_msg_db = crud.create_chat_message(
                    db=db,
                    chat_id=chat_id,
                    role="user",
                    content=user_message,
                    file_ids=file_ids
                )
                break  # Thoát khỏi vòng lặp nếu thành công
            except Exception as e:
                retry_count += 1
                logger.error(f"Failed to save user message (attempt {retry_count}/{max_retries}): {e}", exc_info=True)
                if retry_count < max_retries:
                    await asyncio.sleep(1)  # Chờ 1 giây trước khi thử lại
                    db.rollback()  # Rollback trạng thái trước khi thử lại
                # Nếu đã vượt quá số lần thử, tiếp tục xử lý mà không lưu tin nhắn user
        
        # Lấy lịch sử chat từ DB
        chat_history = []
        try:
            if user_msg_db:
                messages = crud.get_messages_for_chat(db, chat_id=chat_id)
                # Bỏ tin nhắn cuối cùng (tin nhắn user vừa tạo)
                messages = messages[:-1] if messages else []
            else:
                # Nếu không lưu được tin nhắn user, vẫn cố gắng lấy lịch sử
                messages = crud.get_messages_for_chat(db, chat_id=chat_id)
            
            # Chuyển đổi sang định dạng phù hợp
            for msg in messages:
                chat_history.append({
                    "role": msg.role,
                    "content": msg.content
                })
        except Exception as e:
            logger.error(f"Failed to get chat history: {e}", exc_info=True)
            # Tiếp tục với lịch sử trống nếu có lỗi
        
        # Tạo task để xử lý tin nhắn
        asyncio.create_task(
            streaming_adapter.process_with_openai_rag(user_message, chat_history, queue)
        )
        
        # Tạo hàm async generator để stream kết quả
        async def event_stream():
            logger.info(f"Starting generate_ai_response_stream for generation_id: {generation_id}")
            
            # Gửi generation_id trước
            yield f"data: {{'generation_id': '{generation_id}'}}\n\n"
            
            ai_response_content = ""
            
            # Đọc từng đoạn từ queue và gửi đi
            while True:
                chunk = await queue.get()
                
                if chunk == "[DONE]":
                    logger.info("Sending [DONE] marker")
                    yield "data: [DONE]\n\n"
                    break
                    
                try:
                    # Phân tích chunk thành JSON
                    chunk_data = json.loads(chunk)
                    
                    if "text" in chunk_data:
                        text_chunk = chunk_data["text"]
                        ai_response_content += text_chunk
                        logger.info(f"Sending chunk (length: {len(text_chunk)})")
                        yield f"data: {chunk}\n\n"
                    elif "error" in chunk_data:
                        logger.error(f"Error in stream: {chunk_data['error']}")
                        yield f"data: {chunk}\n\n"
                        
                except Exception as e:
                    logger.error(f"Error processing chunk: {str(e)}")
            
            # Lưu phản hồi AI vào database
            max_db_retries = 3
            retry_count = 0
            ai_msg_db = None
            
            while retry_count < max_db_retries:
                try:
                    ai_msg_db = crud.create_chat_message(
                        db=db,
                        chat_id=chat_id,
                        role="assistant",  # Chú ý: sử dụng "assistant" thay vì "ai"
                        content=ai_response_content
                    )
                    logger.info(f"AI response saved to DB with ID: {ai_msg_db.id}")
                    break  # Thoát khỏi vòng lặp nếu thành công
                except Exception as e:
                    retry_count += 1
                    logger.error(f"Failed to save AI response (attempt {retry_count}/{max_db_retries}): {e}", exc_info=True)
                    if retry_count < max_db_retries:
                        await asyncio.sleep(1)  # Chờ 1 giây trước khi thử lại
                        db.rollback()  # Rollback trạng thái trước khi thử lại
                    # Nếu đã vượt quá số lần thử, bỏ qua việc lưu phản hồi
                
            logger.info(f"Generation task for {generation_id} completed successfully")
            
        # Trả về StreamingResponse
        return StreamingResponse(
            event_stream(),
            media_type="text/event-stream"
        )
        
    except Exception as e:
        logger.error(f"Error in stream_openai_chat: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing your request: {str(e)}"
        )
        
@router.get("/classify-topic")
async def classify_topic(
    text: str = Query(..., description="Văn bản cần phân loại")
):
    """
    Phân loại chủ đề của văn bản
    
    Args:
        text: Văn bản cần phân loại
        
    Returns:
        Dict: Kết quả phân loại
    """
    try:
        is_linear_algebra, metadata = topic_classifier.classify(text)
        
        return {
            "is_linear_algebra": is_linear_algebra,
            "metadata": metadata
        }
    except Exception as e:
        logger.error(f"Error classifying topic: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while classifying the topic: {str(e)}"
        )

@router.get("/rag-search")
async def rag_search(
    query: str = Query(..., description="Câu truy vấn"),
    top_k: int = Query(3, description="Số lượng kết quả trả về")
):
    """
    Tìm kiếm với RAG
    
    Args:
        query: Câu truy vấn
        top_k: Số lượng kết quả trả về
        
    Returns:
        Dict: Kết quả tìm kiếm
    """
    try:
        # Khởi tạo RAGService
        rag_service = RAGService()
        
        # Thực hiện tìm kiếm
        documents, success = await rag_service.get_context(query, k=top_k)
        
        if not success:
            return {
                "success": False,
                "message": "Không tìm thấy kết quả phù hợp",
                "documents": []
            }
            
        # Chuyển đổi documents sang định dạng JSON
        results = []
        for doc in documents:
            results.append({
                "content": doc.page_content if hasattr(doc, "page_content") else "",
                "metadata": doc.metadata if hasattr(doc, "metadata") else {}
            })
            
        return {
            "success": True,
            "message": f"Tìm thấy {len(results)} kết quả",
            "documents": results
        }
        
    except Exception as e:
        logger.error(f"Error in RAG search: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during search: {str(e)}"
        ) 
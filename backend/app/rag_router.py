import asyncio
import json
import logging
import traceback
from typing import Dict, List, Optional, Any

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from . import crud, schemas
from .adapters.streaming_adapter import streaming_adapter
from .config import get_settings
from .database import get_db
from .services.topic_classifier import topic_classifier
from .rag.rag_service import RAGService
from .services.llm.openai_service import OpenAIService
from .rag.query_extractor_vn import parse_query
from .rag.prompts.templates import LinearAlgebraTemplates
from .crud import chat_crud

# Configure logging
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/rag", tags=["RAG"])

@router.post("/chats/{chat_id}/openai-stream")
async def openai_chat_stream(
    chat_id: int,
    user_message: str = Query(..., description="User message content"),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """
    Stream OpenAI chat response with RAG integration for a specific chat.
    """
    logger.info(f"User message content: {user_message}")
    
    settings = get_settings()
    
    # Tạo generation ID để tracking
    import uuid
    generation_id = f"{chat_id}_{uuid.uuid4().int}"
    logger.info(f"Generation ID: {generation_id}")
    
    # Tạo queue cho việc streaming
    queue = asyncio.Queue()
    
    # Parse query với VN extractor mới
    parsed_query = parse_query(user_message)
    
    # Log parsed query để debug
    logger.info(f"Parsed query: category={parsed_query.category}, subcategory={parsed_query.subcategory}, year={parsed_query.year}")
    if parsed_query.question_code:
        logger.info(f"Request for specific question: {parsed_query.question_code}")
    elif parsed_query.question_num:
        logger.info(f"Request for question section: {parsed_query.question_num}")
    
    # Khởi tạo RAG service
    rag_service = RAGService()
    
    # Function để xử lý streaming
    async def event_stream():
        try:
            logger.info(f"Starting generate_ai_response_stream for generation_id: {generation_id}")
            
            # Send generation ID event first
            yield f"data: {json.dumps({'generation_id': generation_id})}\n\n"
            
            # Lấy chat history để xử lý follow-up questions
            from . import crud
            chat_history = crud.get_messages_for_chat(db, chat_id=chat_id, limit=10)
            
            # Tìm kiếm context phù hợp từ RAG với chat history
            documents, success = await rag_service.get_context_with_history(
                user_message, 
                chat_history=chat_history,
                use_query_metadata=True
            )
            
            if success and documents:
                logger.info(f"Retrieved {len(documents)} documents for context")
                
                # Tạo prompt với context
                prompt_templates = LinearAlgebraTemplates()
                system_message = prompt_templates.get_system_prompt(rag_enabled=True)
                enhanced_prompt = prompt_templates.get_enhanced_prompt(
                    user_question=user_message,
                    documents=documents
                )
                
                # Log đầy đủ thông tin các documents để debug
                for i, doc in enumerate(documents[:2]):  # Log 2 documents đầu tiên
                    if hasattr(doc, "metadata"):
                        metadata_str = ", ".join([f"{k}={v}" for k, v in doc.metadata.items() 
                                                 if k in ["question_number", "problem_section", "year", "category", "subcategory", "title"]])
                        logger.info(f"Document {i+1} metadata: {metadata_str}")
                    
                    if hasattr(doc, "page_content"):
                        content_preview = doc.page_content[:150].replace("\n", " ")
                        logger.info(f"Document {i+1} content preview: {content_preview}...")
            else:
                logger.info("No relevant documents found")
                # Fallback to regular prompt
                system_message = LinearAlgebraTemplates.get_system_prompt(rag_enabled=False)
                enhanced_prompt = user_message
            
            # Thêm hướng dẫn bảo toàn LaTeX cho system prompt
            latex_preservation_prompt = """
CRITICAL INSTRUCTION: You must preserve ALL LaTeX syntax exactly as found in the data.
ALWAYS wrap math expressions in $...$ for inline math or $$...$$ for block math.
NEVER remove or simplify any LaTeX commands like \\begin{matrix} or \\frac{}.
IMPORTANT: If the user asks for a specific problem (e.g., "bài 2.1"), you MUST return the EXACT problem from the database without modifications.
"""
            system_message = system_message + "\n\n" + latex_preservation_prompt
            
            # OpenAI service để stream response
            openai_service = OpenAIService(
                api_key=settings.openai_api_key,
                model_name=settings.openai_model_name
            )
            
            # Save user message to DB
            user_msg = None
            try:
                # Retry mechanism cho việc save message
                max_retries = 3
                retry_count = 0
                while retry_count < max_retries:
                    try:
                        user_msg = chat_crud.create_chat_message(
                            db=db,
                            chat_id=chat_id,
                            role="user",
                            content=user_message
                        )
                        break
                    except Exception as e:
                        retry_count += 1
                        if retry_count >= max_retries:
                            logger.error(f"Failed to save user message after {max_retries} attempts: {e}")
                            raise
                        logger.warning(f"Retry {retry_count}: Failed to save user message: {e}")
                        await asyncio.sleep(0.5)  # Short delay before retry
            except Exception as e:
                logger.error(f"Error saving user message: {e}")
                yield f"data: Error saving user message: {str(e)}\n\n"
            
            # Stream response từ OpenAI
            ai_message_content = ""
            async for chunk in openai_service.generate_stream(
                system_message=system_message,
                user_message=enhanced_prompt
            ):
                # Chuyển đổi xuống dòng thành <br> để hiển thị trên web
                chunk_length = len(chunk) if chunk else 0
                logger.info(f"Sending chunk (length: {chunk_length})")
                
                # Add chunk to response
                ai_message_content += chunk
                
                # Yield the chunk for streaming
                yield f"data: {chunk}\n\n"
            
            # Send [DONE] marker
            logger.info("Sending [DONE] marker")
            yield "data: [DONE]\n\n"
            
            # Save AI response to DB
            try:
                # Retry mechanism cho việc save AI message
                max_retries = 3
                retry_count = 0
                while retry_count < max_retries:
                    try:
                        ai_msg = chat_crud.create_chat_message(
                            db=db,
                            chat_id=chat_id,
                            role="assistant",  # Phải là "assistant", không phải "ai"
                            content=ai_message_content
                        )
                        logger.info(f"AI response saved to DB with ID: {ai_msg.id}")
                        break
                    except Exception as e:
                        retry_count += 1
                        if retry_count >= max_retries:
                            logger.error(f"Failed to save AI message after {max_retries} attempts: {e}")
                            raise
                        logger.warning(f"Retry {retry_count}: Failed to save AI message: {e}")
                        await asyncio.sleep(0.5)  # Short delay before retry
            except Exception as e:
                logger.error(f"Error saving AI response: {e}")
            
            logger.info(f"Generation task for {generation_id} completed successfully")
            
        except Exception as e:
            logger.error(f"Error in streaming: {e}")
            logger.error(traceback.format_exc())
            yield f"data: Error: {str(e)}\n\n"
            yield "data: [DONE]\n\n"
    
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream"
    )

@router.get("/classify-topic")
async def classify_topic(
    text: str = Query(..., description="Text to classify"),
    db: Session = Depends(get_db)
):
    """
    Phân loại xem text có liên quan đến đại số tuyến tính không.
    """
    try:
        # Sử dụng VN parser để kiểm tra các từ khóa liên quan
        parsed = parse_query(text)
        metadata = {
            "category": parsed.category,
            "subcategory": parsed.subcategory,
            "year": parsed.year,
            "question_code": parsed.question_code,
            "question_num": parsed.question_num
        }
        
        # Kiểm tra nếu có category/subcategory đại số tuyến tính
        is_linear_algebra = False
        if parsed.category in ["baitap", "dethi"]:
            is_linear_algebra = True
        if parsed.subcategory in ["mt", "dt", "gtr", "hpt", "kgvt"]:
            is_linear_algebra = True
        
        # Kiểm tra nếu có từ "ma trận" hoặc "định thức" trong text
        if "ma trận" in text.lower() or "định thức" in text.lower():
            is_linear_algebra = True
            
        return {
            "is_linear_algebra": is_linear_algebra,
            "extracted_metadata": metadata
        }
    except Exception as e:
        logger.error(f"Error in classify_topic: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error classifying topic: {str(e)}"
        )

@router.get("/rag-search")
async def rag_search(
    query: str = Query(..., description="Search query"),
    top_k: int = Query(3, description="Number of results to return"),
    db: Session = Depends(get_db)
):
    """
    Tìm kiếm thông tin liên quan trong RAG.
    """
    try:
        rag_service = RAGService()
        documents, success = await rag_service.get_context(
            query, 
            k=top_k,
            use_query_metadata=True
        )
        
        if not success or not documents:
            return {"results": [], "message": "No relevant documents found"}
        
        results = []
        for doc in documents:
            doc_dict = {
                "content": doc.page_content if hasattr(doc, "page_content") else "",
                "metadata": doc.metadata if hasattr(doc, "metadata") else {}
            }
            results.append(doc_dict)
            
        return {"results": results, "count": len(results)}
    except Exception as e:
        logger.error(f"Error in rag_search: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching in RAG: {str(e)}"
        ) 
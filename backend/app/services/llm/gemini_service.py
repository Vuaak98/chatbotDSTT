"""
Gemini AI Service for streaming responses
"""
import asyncio
import logging
import json
from typing import List, Dict, Any, Optional, AsyncIterable
from google import genai
from google.genai import types
from sqlalchemy.orm import Session

from ...config import get_settings
from ...crud import chat_crud
from .base import LLMService

logger = logging.getLogger(__name__)

class GeminiService(LLMService):
    """Gemini AI service implementation"""
    
    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash-exp"):
        self.api_key = api_key
        self.model_name = model_name
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Gemini client"""
        try:
            self.client = genai.Client(api_key=self.api_key)
            logger.info(f"Gemini client initialized with model: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            self.client = None
    
    async def generate_stream(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> AsyncIterable[str]:
        """
        Generate streaming response from Gemini
        
        Args:
            messages: List of messages in format [{"role": "user", "content": "..."}]
            system_prompt: System prompt (optional)
            temperature: Temperature for AI
            max_tokens: Max tokens for response
            
        Yields:
            str: Response chunks
        """
        if not self.client:
            yield "Gemini service not available."
            return
        
        try:
            # Prepare contents for Gemini
            contents = []
            
            # Add system prompt if provided
            if system_prompt:
                contents.append(
                    types.Content(role='user', parts=[types.Part(text=system_prompt)])
                )
            
            # Add messages
            for msg in messages:
                role = 'user' if msg['role'] == 'user' else 'model'
                contents.append(
                    types.Content(role=role, parts=[types.Part(text=msg['content'])])
                )
            
            # Generate streaming response
            response_stream = self.client.models.generate_content_stream(
                model=self.model_name,
                contents=contents,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    top_p=0.95,
                    top_k=40,
                    max_output_tokens=max_tokens or 8192
                )
            )
            
            # Stream chunks
            for chunk in response_stream:
                if chunk.candidates and chunk.candidates[0].content.parts:
                    for part in chunk.candidates[0].content.parts:
                        if hasattr(part, 'text') and part.text:
                            yield part.text
                            
        except Exception as e:
            logger.error(f"Error in Gemini generate_stream: {e}")
            yield f"Lỗi khi tạo phản hồi: {str(e)}"
    
    async def generate(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate non-streaming response from Gemini
        
        Args:
            messages: List of messages in format [{"role": "user", "content": "..."}]
            system_prompt: System prompt (optional)
            temperature: Temperature for AI
            max_tokens: Max tokens for response
            
        Returns:
            str: Complete response
        """
        response_parts = []
        async for chunk in self.generate_stream(messages, system_prompt, temperature, max_tokens):
            response_parts.append(chunk)
        
        return ''.join(response_parts)


async def gemini_stream_handler(
    chat_id: str,
    user_message_content: str,
    system_message: str = "",
    file_ids: Optional[List[str]] = None,
    db: Session = None,
    queue: asyncio.Queue = None
) -> None:
    """
    Handle Gemini streaming for chat
    
    Args:
        chat_id: Chat ID
        user_message_content: User message
        system_message: System prompt
        file_ids: File IDs (optional)
        db: Database session
        queue: Queue for streaming
    """
    settings = get_settings()
    
    if not settings.gemini_api_key:
        error_msg = "Gemini API key not configured."
        logger.error(error_msg)
        if queue:
            await queue.put(error_msg)
        return
    
    # Initialize Gemini service
    gemini_service = GeminiService(
        api_key=settings.gemini_api_key,
        model_name=settings.gemini_model_name
    )
    
    # Default system message if not provided
    if not system_message:
        system_message = """Bạn là một trợ lý AI thông minh chuyên về toán học. 
        Hãy trả lời câu hỏi một cách chính xác và hữu ích.
        Sử dụng LaTeX cho các công thức toán học, bọc trong $...$ cho inline hoặc $$...$$ cho block."""
    
    ai_response_content = ""
    
    try:
        # Prepare messages for Gemini service
        messages = [{"role": "user", "content": user_message_content}]
        
        # Stream response from Gemini
        async for chunk in gemini_service.generate_stream(
            messages=messages,
            system_prompt=system_message,
            temperature=0.7
        ):
            ai_response_content += chunk
            if queue:
                await queue.put(chunk)
        
        # Save AI response to database
        if db:
            try:
                ai_msg_db = chat_crud.create_chat_message(
                    db=db,
                    chat_id=int(chat_id),
                    role="assistant",
                    content=ai_response_content
                )
                logger.info(f"Gemini response saved to DB with ID: {ai_msg_db.id}")
            except Exception as e:
                logger.error(f"Failed to save Gemini response: {e}")
                
    except Exception as e:
        error_msg = f"Lỗi Gemini service: {str(e)}"
        logger.error(error_msg)
        if queue:
            await queue.put(error_msg)
import os
import logging
from typing import List, Dict, Any, Optional, AsyncGenerator, Union
import json
from openai import AsyncOpenAI, OpenAI

from ...config import get_settings
from .base import LLMService

logger = logging.getLogger(__name__)

class OpenAIService(LLMService):
    """
    Service để giao tiếp với OpenAI API
    """
    
    def __init__(
        self, 
        api_key: Optional[str] = None, 
        model_name: Optional[str] = None
    ):
        """
        Khởi tạo OpenAI service
        
        Args:
            api_key: OpenAI API key
            model_name: Tên model OpenAI cần sử dụng
        """
        settings = get_settings()
        self.api_key = api_key or settings.openai_api_key
        self.model_name = model_name or settings.openai_model_name
        
        # Tạo async client cho OpenAI
        self.async_client = AsyncOpenAI(api_key=self.api_key)
        self.sync_client = OpenAI(api_key=self.api_key)
        
        # LaTeX config để đảm bảo công thức toán học được hiển thị đúng
        self.latex_config = {
            "preserve_latex": True,
            "response_format": {
                "type": "text"
            }
        }
        
        logger.info(f"OpenAI service initialized with model: {self.model_name}")
    
    async def generate_stream(
        self, 
        system_message: str, 
        user_message: str,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> AsyncGenerator[str, None]:
        """
        Generate stream từ OpenAI API
        
        Args:
            system_message: System prompt
            user_message: User message
            temperature: Mức độ sáng tạo (0.0 - 1.0)
            max_tokens: Số tokens tối đa
            
        Yields:
            Các chunks của response
        """
        try:
            # Tạo messages
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
            
            # Thêm hướng dẫn để bảo toàn LaTeX
            additional_system_message = {
                "role": "system", 
                "content": "LUÔN LUÔN bảo toàn tất cả các công thức toán học và ký hiệu LaTeX. Sử dụng $...$ cho inline và $$...$$ cho block công thức."
            }
            messages.insert(1, additional_system_message)
            
            logger.info(f"Generating streaming response with model: {self.model_name}")
            
            # Thêm tham số bổ sung để đảm bảo LaTeX được bảo toàn
            stream = await self.async_client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
                response_format={"type": "text"}
            )
            
            async for chunk in stream:
                if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    # Đảm bảo nội dung LaTeX không bị cắt giữa chừng
                    yield content
        except Exception as e:
            logger.error(f"Error in generate_stream: {e}")
            raise
    
    def generate(
        self, 
        system_message: str, 
        user_message: str,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> str:
        """
        Generate đồng bộ từ OpenAI API
        
        Args:
            system_message: System prompt
            user_message: User message
            temperature: Mức độ sáng tạo (0.0 - 1.0)
            max_tokens: Số tokens tối đa
            
        Returns:
            Response text
        """
        try:
            # Tạo messages
            messages = [
                {"role": "system", "content": system_message},
                {"role": "system", "content": "LUÔN LUÔN bảo toàn tất cả các công thức toán học và ký hiệu LaTeX. Sử dụng $...$ cho inline và $$...$$ cho block công thức."},
                {"role": "user", "content": user_message}
            ]
            
            logger.info(f"Generating synchronous response with model: {self.model_name}")
            
            # Thêm tham số bổ sung để đảm bảo LaTeX được bảo toàn
            response = self.sync_client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                response_format={"type": "text"}
            )
            
            if response.choices and len(response.choices) > 0:
                return response.choices[0].message.content
            else:
                return ""
        except Exception as e:
            logger.error(f"Error in generate: {e}")
            raise
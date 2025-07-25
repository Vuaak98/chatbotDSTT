import asyncio
from typing import AsyncIterator, Dict, List, Optional

import openai
from openai import AsyncOpenAI

from .base import LLMService


class OpenAIService(LLMService):
    """
    Triển khai LLMService sử dụng OpenAI API
    """
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """
        Khởi tạo OpenAI Service
        
        Args:
            api_key: API key cho OpenAI
            model: Tên model OpenAI (mặc định: gpt-3.5-turbo)
        """
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
    
    async def generate_stream(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> AsyncIterator[str]:
        """
        Tạo phản hồi streaming từ OpenAI.
        
        Args:
            messages: List các tin nhắn
            system_prompt: Prompt hệ thống
            temperature: Temperature cho AI
            max_tokens: Số lượng token tối đa
            
        Yields:
            Các phần nội dung từ phản hồi
        """
        # Thêm system message nếu có
        all_messages = []
        if system_prompt:
            all_messages.append({"role": "system", "content": system_prompt})
        all_messages.extend(messages)
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=all_messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            
            async for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            # Log lỗi và trả về thông báo lỗi
            print(f"Error in OpenAI streaming: {e}")
            yield f"Error: {str(e)}"
    
    async def generate(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Tạo phản hồi đầy đủ từ OpenAI.
        
        Args:
            messages: List các tin nhắn
            system_prompt: Prompt hệ thống
            temperature: Temperature cho AI
            max_tokens: Số lượng token tối đa
            
        Returns:
            Phản hồi từ OpenAI
        """
        # Tận dụng hàm generate_stream để có code DRY
        result = []
        async for chunk in self.generate_stream(
            messages, system_prompt, temperature, max_tokens
        ):
            result.append(chunk)
        
        return "".join(result)
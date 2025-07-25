
from abc import ABC, abstractmethod
from typing import AsyncIterator, Dict, List, Optional, Union

class LLMService(ABC):
    """
    Lớp trừu tượng cho các dịch vụ LLM.
    Định nghĩa interface chung cho các LLM khác nhau (OpenAI, Gemini, v.v.)
    """
    
    @abstractmethod
    async def generate_stream(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> AsyncIterator[str]:
        """
        Tạo phản hồi streaming từ LLM.
        
        Args:
            messages: List các tin nhắn theo định dạng [{"role": "user", "content": "..."}]
            system_prompt: Prompt hệ thống (tùy chọn)
            temperature: Giá trị temperature cho AI
            max_tokens: Số lượng token tối đa cho phản hồi
            
        Returns:
            AsyncIterator[str]: Stream các token phản hồi
        """
        pass
        
    @abstractmethod
    async def generate(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Tạo phản hồi đầy đủ (không streaming) từ LLM.
        
        Args:
            messages: List các tin nhắn theo định dạng [{"role": "user", "content": "..."}]
            system_prompt: Prompt hệ thống (tùy chọn)
            temperature: Giá trị temperature cho AI
            max_tokens: Số lượng token tối đa cho phản hồi
            
        Returns:
            str: Phản hồi đầy đủ từ LLM
        """
        pass

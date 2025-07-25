import logging
from typing import Dict, List, Optional, Tuple, Union

from sqlalchemy.orm import Session

from ..rag.rag_service import RAGService
from ..services.topic_classifier import topic_classifier
from ..config import get_settings

# Cấu hình logging
logger = logging.getLogger(__name__)

class RAGIntegrationService:
    """
    Service tích hợp RAG vào luồng xử lý tin nhắn.
    Đánh giá tin nhắn của người dùng và quyết định có áp dụng RAG hay không.
    """
    
    def __init__(self, rag_service: Optional[RAGService] = None):
        """
        Khởi tạo service tích hợp RAG
        
        Args:
            rag_service: RAGService instance (tạo mới nếu không có)
        """
        self.settings = get_settings()
        self.rag_service = rag_service or RAGService()
        
    async def process_message_for_rag(
        self, 
        user_message: str
    ) -> Tuple[str, Dict]:
        """
        Xử lý tin nhắn người dùng để áp dụng RAG nếu phù hợp
        
        Args:
            user_message: Tin nhắn của người dùng
            
        Returns:
            Tuple[str, Dict]: (enhanced_prompt, metadata)
            - enhanced_prompt: Prompt đã tăng cường với ngữ cảnh từ RAG (hoặc rỗng nếu không phù hợp)
            - metadata: Thông tin về quá trình xử lý RAG
        """
        # Nếu RAG bị tắt, trả về prompt rỗng và metadata
        if not self.settings.rag_enabled:
            return "", {"rag_enabled": False, "is_rag_query": False, "success": False}
            
        # 1. Phân loại topic
        is_linear_algebra, topic_metadata = topic_classifier.classify(user_message)
        
        if not is_linear_algebra:
            # Không phải câu hỏi đại số tuyến tính, trả về prompt rỗng
            logger.info("Không phải câu hỏi đại số tuyến tính, bỏ qua RAG.")
            return "", {
                "rag_enabled": True, 
                "is_rag_query": False,
                "success": False,
                "topic_metadata": topic_metadata
            }
            
        # 2. Lấy ngữ cảnh RAG
        logger.info(f"Câu hỏi đại số tuyến tính phát hiện, đang lấy ngữ cảnh RAG...")
        
        # Đối với Olympic, có thể thêm bộ lọc cho Olympic
        filter_condition = None
        if topic_metadata.get("is_olympic", False):
            filter_condition = {"category": "olympic"}
            
        # Lấy ngữ cảnh đã định dạng và thông tin thành công
        context, success = await self.rag_service.get_formatted_context(
            query=user_message,
            filter=filter_condition
        )
        
        # 3. Tạo enhanced prompt
        if success and context:
            logger.info(f"Đã tìm thấy {len(context)} ký tự ngữ cảnh phù hợp")
            
            # Tạo prompt đã tăng cường với ngữ cảnh
            enhanced_prompt = self._create_enhanced_prompt(user_message, context)
            
            return enhanced_prompt, {
                "rag_enabled": True,
                "is_rag_query": True,
                "success": True,
                "topic_metadata": topic_metadata,
                "context_length": len(context)
            }
        else:
            # Không tìm thấy ngữ cảnh phù hợp hoặc có lỗi
            logger.info("Không tìm thấy ngữ cảnh phù hợp, sử dụng câu hỏi thông thường.")
            return "", {
                "rag_enabled": True,
                "is_rag_query": True,
                "success": False,
                "topic_metadata": topic_metadata
            }
            
    def _create_enhanced_prompt(self, user_message: str, context: str) -> str:
        """
        Tạo prompt tăng cường với ngữ cảnh
        
        Args:
            user_message: Câu hỏi gốc của người dùng
            context: Ngữ cảnh từ RAG
            
        Returns:
            Prompt tăng cường
        """
        return f"""
Hãy trả lời câu hỏi sau dựa trên ngữ cảnh được cung cấp. Nếu ngữ cảnh không đủ thông tin, hãy trả lời theo kiến thức của bạn nhưng ưu tiên thông tin từ ngữ cảnh cung cấp.

{context}

Câu hỏi: {user_message}

Trả lời dựa trên ngữ cảnh trên. Nếu bạn sử dụng thông tin từ ngữ cảnh, hãy nêu rõ nguồn. Nếu bạn trả lời theo kiến thức của riêng bạn, hãy nói rõ điều đó. Hãy đảm bảo câu trả lời của bạn chính xác, súc tích và dễ hiểu với các ví dụ minh họa nếu cần.
"""

# Singleton instance
rag_integration = RAGIntegrationService() 
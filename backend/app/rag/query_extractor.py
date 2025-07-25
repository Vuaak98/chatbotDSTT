import re
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class QueryMetadataExtractor:
    """
    Trích xuất metadata và bộ lọc từ câu truy vấn người dùng
    """
    
    # Danh sách các chủ đề DSTT phổ biến (tags)
    MATH_TOPICS = [
        "ma trận", "định thức", "giá trị riêng", "vector riêng",
        "hệ phương trình", "không gian vector", "tổ hợp", 
        "đa thức", "không gian con", "ánh xạ tuyến tính",
        "cơ sở", "chiếu trực giao", "chéo hóa",
        "trực giao", "biến đổi tuyến tính"
    ]
    
    @staticmethod
    def extract_metadata(query: str) -> Dict[str, Any]:
        """
        Trích xuất metadata từ câu truy vấn
        
        Args:
            query: Câu truy vấn của người dùng
            
        Returns:
            Dict[str, Any]: Các bộ lọc tìm được (tags, year, question, etc.)
        """
        filter_params = {}
        query_lower = query.lower()
        
        # Tìm năm
        year_match = re.search(r'20\d{2}', query)
        if year_match:
            filter_params["year"] = int(year_match.group())
        
        # Tìm số bài (bài 1, bài 2.1, etc)
        bai_match = re.search(r'bài\s+(\d+\.?\d*)\s*(\([a-z]\))?', query_lower)
        if bai_match:
            question = bai_match.group(1)
            if bai_match.group(2):  # Có ý phụ (a), (b), etc.
                question += bai_match.group(2).strip('()').lower()
            filter_params["question"] = question
        
        # Tìm chủ đề toán học
        found_topics = []
        for topic in QueryMetadataExtractor.MATH_TOPICS:
            if topic in query_lower:
                found_topics.append(topic)
                
        if found_topics:
            filter_params["tags"] = found_topics
        
        # Tìm cấp độ (olympic, quốc gia, etc.)
        if "olympic" in query_lower:
            filter_params["cap"] = "olympic"
        elif "quốc gia" in query_lower:
            filter_params["cap"] = "quốc gia"
            
        # Tìm loại (đề thi, bài tập)
        if "đề thi" in query_lower:
            filter_params["type"] = "dethi"
        elif "bài tập" in query_lower:
            filter_params["type"] = "dangbai"
            
        return filter_params 
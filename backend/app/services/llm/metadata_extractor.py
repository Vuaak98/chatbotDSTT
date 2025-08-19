import sys
import os
import logging
import json
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field

# Thêm đường dẫn tới thư mục app
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(app_path)

# Import tuyệt đối
import config

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

logger = logging.getLogger(__name__)

class MathQueryMetadata(BaseModel):
    """Schema cho metadata được trích xuất từ câu hỏi toán học - Cấu trúc mới"""
    
    # === CẤU TRÚC MỚI ===
    category: Optional[str] = Field(
        None,
        description="Loại nội dung: 'dethi' (đề thi) hoặc 'baitap' (bài tập). Chỉ trả về nếu có trong câu hỏi."
    )
    
    subcategory: Optional[str] = Field(
        None,
        description="Phân loại con: 'bangA', 'bangB' (cho đề thi), 'gtr' (giải tích), 'hpt' (hệ phương trình), 'dstuyentinh' (đại số tuyến tính). Chỉ trả về nếu có trong câu hỏi."
    )
    
    problem_type: Optional[str] = Field(
        None,
        description="Loại bài toán: 'dethi', 'baitap', 'thuchanh'. Chỉ trả về nếu có trong câu hỏi."
    )
    
    difficulty_level: Optional[str] = Field(
        None,
        description="Mức độ khó: 'co_ban', 'trung_binh', 'kho', 'quoc_gia' (olympic). Chỉ trả về nếu có trong câu hỏi."
    )
    
    subject_area: Optional[str] = Field(
        None,
        description="Lĩnh vực toán học: 'dai_so_tuyen_tinh', 'giai_tich', 'hinh_hoc', 'xac_suat_thong_ke', 'dai_so'. Chỉ trả về nếu có trong câu hỏi."
    )
    
    # === CẤU TRÚC CŨ (GIỮ LẠI ĐỂ BACKWARD COMPATIBILITY) ===
    year: Optional[int] = Field(
        None, 
        description="Năm của đề thi, ví dụ: 2024. Chỉ trả về số nguyên nếu có trong câu hỏi."
    )
    
    exam: Optional[str] = Field(
        None,
        description="Loại đề thi, ví dụ: 'olympic', 'dethi', 'kyyeu'. Chỉ trả về nếu có trong câu hỏi."
    )
    
    question: Optional[str] = Field(
        None,
        description="Số hiệu câu hỏi, ví dụ: '1', '2.1', '3a', 'bài 4'. Chỉ trả về nếu có trong câu hỏi. Lưu ý: nếu câu hỏi chỉ có số không có chữ cái (như 'bài 1'), hãy chỉ trả về số ('1')."
    )
    
    level: Optional[str] = Field(
        None,
        description="Bảng của đề thi, ví dụ: 'a', 'b', 'c'. Chỉ trả về nếu có trong câu hỏi."
    )
    
    tags: Optional[List[str]] = Field(
        None,
        description="Các từ khóa toán học, ví dụ: ['ma trận', 'định thức', 'hệ phương trình']. Chỉ trả về nếu có trong câu hỏi."
    )
    
    requesting_solution: bool = Field(
        description="True nếu người dùng yêu cầu lời giải/hướng dẫn/cách làm, False nếu chỉ yêu cầu đề bài/tìm hiểu"
    )
    
    display_mode: bool = Field(
        default=False,
        description="True nếu người dùng chỉ muốn xem đề bài nguyên văn (cho tôi, hiển thị, xem đề), False nếu cần giải thích"
    )
    
    class Config:
        extra = "forbid"  # Không cho phép thêm trường khác

class MetadataExtractor:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.1,  # Thấp để ổn định
            api_key=self.api_key
        )
        self.parser = PydanticOutputParser(pydantic_object=MathQueryMetadata)
        
    async def extract_metadata(self, query: str, max_retries: int = 2) -> MathQueryMetadata:
        """
        Trích xuất metadata từ câu hỏi với retry logic
        """
        format_instructions = self.parser.get_format_instructions()
        prompt_template = ChatPromptTemplate.from_messages([
            ("system",
                """
Bạn là chuyên gia trích xuất metadata từ câu hỏi toán học với cấu trúc mới.
CHỈ trả về một object JSON hợp lệ theo schema dưới đây, KHÔNG giải thích, KHÔNG lặp lại schema, KHÔNG trả về mô tả schema, KHÔNG trả về bất kỳ thông tin nào ngoài object JSON.

Schema:
{format_instructions}

HƯỚNG DẪN TRÍCH XUẤT CẤU TRÚC MỚI:

1. CATEGORY (Loại nội dung):
   - "dethi": đề thi, olympic, thi đấu
   - "baitap": bài tập, thực hành, luyện tập

2. SUBCATEGORY (Phân loại con):
   - "bangA": bảng A, bang A (cho đề thi)
   - "bangB": bảng B, bang B (cho đề thi)
   - "gtr": giá trị riêng, vector riêng, eigenvalue, eigenvector (cho bài tập)
   - "hpt": hệ phương trình, phương trình tuyến tính (cho bài tập)
   - "kgvt": không gian vector, vector space (cho bài tập)
   - "mt": ma trận, matrix, phép toán ma trận (cho bài tập)
   - "tohop": tổ hợp, combinatorics (cho bài tập)
   - "dathuc": đa thức, polynomial (cho bài tập)
   - "dt": định thức, determinant (cho bài tập)

3. DIFFICULTY_LEVEL (Mức độ khó):
   - "co_ban": cơ bản, dễ, đơn giản
   - "trung_binh": trung bình, vừa
   - "kho": khó, nâng cao, phức tạp
   - "quoc_gia": olympic, quốc gia

4. SUBJECT_AREA (Lĩnh vực toán - CHỈ ĐẠI SỐ TUYẾN TÍNH):
   - "dai_so_tuyen_tinh": ma trận, định thức, hệ phương trình, vector, eigenvalue, eigenvector, không gian vector, biến đổi tuyến tính, hạng ma trận

5. PROBLEM_TYPE: thường giống category

LƯU Ý ĐẶC BIỆT:
- Ưu tiên sử dụng CẤU TRÚC MỚI (category, subcategory, etc.)
- Vẫn giữ cấu trúc cũ để backward compatibility
- Nếu có "bảng A" → category: "dethi", subcategory: "bangA"
- Nếu có "ma trận" → subject_area: "dai_so_tuyen_tinh"
- Nếu có "olympic" → difficulty_level: "quoc_gia"

REQUESTING_SOLUTION DETECTION:
- TRUE nếu có: "giải", "hướng dẫn", "cách làm", "lời giải", "solution", "solve", "how to", "làm thế nào", "giúp tôi làm", "chỉ cách", "hướng dẫn giải", "giải thích", "explain", "tại sao", "why", "phương pháp", "method", "cách tiếp cận", "approach", "hiểu", "understand", "học", "learn"
- FALSE nếu có: "cho tôi", "tìm", "có", "cần", "muốn xem", "đưa ra", "cung cấp", "hiển thị", "show me", "give me", "list", "liệt kê"
- Ưu tiên từ khóa yêu cầu giải thích hơn từ khóa yêu cầu đề bài
- Nếu có cả hai loại từ khóa, ưu tiên TRUE (sinh viên muốn học)

DISPLAY_MODE DETECTION:
- TRUE nếu có: "cho tôi", "hiển thị", "xem đề", "đưa ra đề", "show me", "give me", "cung cấp đề", "muốn xem đề", "đề bài", "bài số"
- FALSE nếu có: "giải thích", "hướng dẫn", "làm thế nào", "tại sao", "phương pháp"
- Display_mode = TRUE có nghĩa là chỉ hiển thị đề bài nguyên văn, không giải thích

Ví dụ:
User: Cho tôi bài 1 đề thi bảng A năm 2024 về ma trận
Output: {{"category": "dethi", "subcategory": "bangA", "difficulty_level": "quoc_gia", "subject_area": "dai_so_tuyen_tinh", "year": 2024, "question": "1", "level": "a", "tags": ["ma trận"], "requesting_solution": false, "display_mode": true}}

User: Giải bài tập về định thức
Output: {{"category": "baitap", "subcategory": "dt", "subject_area": "dai_so_tuyen_tinh", "tags": ["định thức"], "requesting_solution": true, "display_mode": false}}

User: Cho tôi bài tập về ma trận
Output: {{"category": "baitap", "subcategory": "mt", "subject_area": "dai_so_tuyen_tinh", "tags": ["ma trận"], "requesting_solution": false, "display_mode": true}}

User: Hướng dẫn làm bài tập về ma trận nghịch đảo
Output: {{"category": "baitap", "subcategory": "mt", "subject_area": "dai_so_tuyen_tinh", "tags": ["ma trận", "nghịch đảo"], "requesting_solution": true}}

User: Tôi cần bài tập về hệ phương trình tuyến tính
Output: {{"category": "baitap", "subcategory": "hpt", "subject_area": "dai_so_tuyen_tinh", "tags": ["hệ phương trình"], "requesting_solution": false}}

User: Làm thế nào để tính eigenvalue?
Output: {{"category": "baitap", "subcategory": "kgvt", "subject_area": "dai_so_tuyen_tinh", "tags": ["eigenvalue"], "requesting_solution": true}}

User: Đề olympic bảng B có bài nào về vector không?
Output: {{"category": "dethi", "subcategory": "bangB", "difficulty_level": "quoc_gia", "subject_area": "dai_so_tuyen_tinh", "exam": "olympic", "level": "b", "tags": ["vector"], "requesting_solution": false}}

User: Giải thích cách làm bài 1 đề thi bảng A
Output: {{"category": "dethi", "subcategory": "bangA", "difficulty_level": "quoc_gia", "subject_area": "dai_so_tuyen_tinh", "question": "1", "tags": ["giải thích"], "requesting_solution": true}}

User: Tôi không hiểu bài này, hướng dẫn giúp tôi
Output: {{"category": "baitap", "subject_area": "dai_so_tuyen_tinh", "tags": ["hướng dẫn"], "requesting_solution": true}}

User: Tại sao phải dùng phương pháp này để tính định thức?
Output: {{"category": "baitap", "subcategory": "dt", "subject_area": "dai_so_tuyen_tinh", "tags": ["định thức", "phương pháp"], "requesting_solution": true}}
"""
            ),
            ("user", "Câu hỏi: {query}")
        ])
        
        for attempt in range(max_retries + 1):
            try:
                # Tạo chain với structured output
                chain = prompt_template | self.llm | self.parser
                
                # Thực thi
                result = await chain.ainvoke({
                    "query": query,
                    "format_instructions": self.parser.get_format_instructions()
                })
                
                logger.info(f"Metadata extracted successfully: {result}")
                
                # Xử lý hậu kỳ để chuẩn hóa trường question
                if result.question:
                    # Loại bỏ các tiền tố như "bài", "câu", v.v.
                    question = result.question.lower()
                    question = question.replace("bài", "").replace("câu", "").replace("toán", "").strip()
                    # Chỉ giữ lại số và chữ cái (nếu có)
                    result.question = question
                    logger.info(f"Normalized question: {result.question}")
                
                return result
                
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                
                if attempt < max_retries:
                    # Thêm context lỗi cho lần thử tiếp theo
                    query = f"{query}\n\nLỗi trước đó: {str(e)}. Hãy cố gắng trích xuất chính xác hơn."
                else:
                    # Fallback: trả về metadata mặc định
                    logger.error(f"All attempts failed for query: {query}")
                    return MathQueryMetadata(
                        requesting_solution="giải" in query.lower() or "lời giải" in query.lower()
                    )

# Test function
async def test_extractor():
    extractor = MetadataExtractor()
    
    test_queries = [
        "Cho tôi bài 1 đề thi bảng A năm 2024 về ma trận",
        "Giải bài tập khó về định thức trong đại số tuyến tính", 
        "Đề olympic bảng B có bài nào về hệ phương trình không?",
        "Hướng dẫn giải bài tập cơ bản về đạo hàm",
        "Bài 2 trong đề thi năm 2024",
        "Tôi cần bài tập về hình học không gian",
        "Cho tôi đề bài về xác suất và thống kê"
    ]
    
    for query in test_queries:
        result = await extractor.extract_metadata(query)
        print(f"Query: {query}")
        print(f"Result: {result}")
        print(f"New structure - Category: {result.category}, Subcategory: {result.subcategory}")
        print(f"Subject: {result.subject_area}, Difficulty: {result.difficulty_level}")
        print("---")

# Chạy test nếu file được chạy trực tiếp
if __name__ == "__main__":
    import asyncio
    asyncio.run(test_extractor()) 
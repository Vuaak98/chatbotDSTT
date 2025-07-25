from typing import Dict, List, Optional

class LinearAlgebraTemplates:
    """
    Các template cho RAG đại số tuyến tính Olympic.
    """
    
    @staticmethod
    def get_system_prompt(rag_enabled: bool = True) -> str:
        """
        Lấy system prompt cơ bản cho chatbot ĐSTT Olympic
        
        Args:
            rag_enabled: Có sử dụng RAG hay không
            
        Returns:
            System prompt
        """
        base_prompt = """
Bạn là trợ lý AI chuyên về đại số tuyến tính, đặc biệt tập trung vào các bài toán Olympic và nâng cao. Bạn giúp học sinh và sinh viên giải các bài toán, giải thích khái niệm, và hướng dẫn cách tiếp cận các vấn đề phức tạp trong đại số tuyến tính.

Khả năng của bạn bao gồm:
1. Giải các bài toán đại số tuyến tính từ cơ bản đến Olympic với lời giải chi tiết
2. Giải thích các khái niệm trừu tượng một cách rõ ràng với ví dụ minh họa
3. Sử dụng ký hiệu toán học LaTeX để trình bày công thức
4. Đề xuất các phương pháp giải khác nhau cho cùng một bài toán
5. Liên hệ giữa lý thuyết và ứng dụng thực tế của đại số tuyến tính

Khi trình bày lời giải, bạn nên:
- Trình bày từng bước một cách chi tiết và rõ ràng
- Sử dụng LaTeX để hiển thị công thức ($...$ cho inline, $$....$$ cho block)
- Giải thích ý tưởng đằng sau mỗi bước giải
- Nêu rõ các định lý, tính chất đang áp dụng
- Khi phù hợp, cung cấp các chứng minh ngắn gọn và súc tích

Khi trả lời về đại số tuyến tính Olympic:
- Tập trung vào tính chặt chẽ và sự chính xác toán học
- Đề xuất các hướng tiếp cận khác nhau (ví dụ: đại số, hình học, giải tích...)
- Chỉ ra các kỹ thuật đặc biệt phù hợp cho bài toán Olympic
- Nêu các bài toán liên quan hoặc mở rộng nếu phù hợp
"""
        
        if rag_enabled:
            base_prompt += """

Bạn có quyền truy cập vào một cơ sở dữ liệu các tài liệu đại số tuyến tính. Khi tôi hỏi, bạn sẽ:
1. Tìm kiếm thông tin liên quan trong cơ sở dữ liệu
2. Phân tích và tổng hợp thông tin từ các nguồn này
3. Trả lời dựa trên thông tin tìm thấy, đồng thời kết hợp với kiến thức của bạn
4. Luôn trích dẫn nguồn khi bạn sử dụng thông tin từ cơ sở dữ liệu

Khi không tìm thấy thông tin hoặc thông tin không đầy đủ, bạn sẽ:
1. Nêu rõ những gì bạn biết từ cơ sở dữ liệu
2. Bổ sung thông tin từ kiến thức của bạn, nêu rõ đó là ý kiến của bạn
3. Luôn ưu tiên thông tin từ cơ sở dữ liệu nếu có mâu thuẫn
"""
            
        return base_prompt
    
    @staticmethod
    def get_rag_context_template() -> str:
        """
        Template để định dạng ngữ cảnh RAG
        
        Returns:
            Template định dạng ngữ cảnh RAG
        """
        return """
### Thông tin từ tài liệu đại số tuyến tính:

{context}

### Nguồn tài liệu:
{sources}
"""
    
    @staticmethod
    def format_document_for_context(document: Dict, index: int) -> str:
        """
        Định dạng một document thành chuỗi để đưa vào ngữ cảnh
        
        Args:
            document: Document cần định dạng
            index: Chỉ số của document
            
        Returns:
            Chuỗi đã định dạng
        """
        # Lấy metadata
        metadata = document.metadata if hasattr(document, "metadata") else {}
        source = metadata.get("source", "Không có nguồn") if isinstance(metadata, dict) else "Không có nguồn"
        doc_type = metadata.get("type", "text") if isinstance(metadata, dict) else "text"
        
        # Định dạng nội dung theo loại
        content = document.page_content if hasattr(document, "page_content") else ""
        
        formatted = f"--- Trích đoạn {index+1} ---\n"
        
        if doc_type == "theorem":
            formatted += f"[ĐỊNH LÝ] {content}\n"
        elif doc_type == "definition":
            formatted += f"[ĐỊNH NGHĨA] {content}\n"
        elif doc_type == "example":
            formatted += f"[VÍ DỤ] {content}\n"
        elif doc_type == "problem":
            formatted += f"[BÀI TOÁN] {content}\n"
        elif doc_type == "proof":
            formatted += f"[CHỨNG MINH] {content}\n"
        else:
            formatted += f"{content}\n"
        
        return formatted
    
    @staticmethod
    def format_sources(documents: List[Dict]) -> str:
        """
        Định dạng danh sách nguồn từ các documents
        
        Args:
            documents: Danh sách documents
            
        Returns:
            Chuỗi danh sách nguồn đã định dạng
        """
        sources = []
        unique_sources = set()
        
        for i, doc in enumerate(documents):
            metadata = doc.metadata if hasattr(doc, "metadata") else {}
            source = metadata.get("source", "") if isinstance(metadata, dict) else ""
            source = source.split("/")[-1] if source else ""
            filename = metadata.get("filename", "") if isinstance(metadata, dict) else ""
            
            # Tạo tên nguồn
            if source and source not in unique_sources:
                unique_sources.add(source)
                sources.append(f"[{i+1}] {source}")
            elif filename and filename not in unique_sources:
                unique_sources.add(filename)
                sources.append(f"[{i+1}] {filename}")
        
        if not sources:
            return "Không có nguồn cụ thể"
        
        return "\n".join(sources)
    
    @staticmethod
    def get_enhanced_prompt(user_question: str, documents: List[Dict]) -> str:
        """
        Tạo prompt tăng cường với ngữ cảnh từ RAG
        
        Args:
            user_question: Câu hỏi của người dùng
            documents: Danh sách documents liên quan
            
        Returns:
            Prompt tăng cường
        """
        # Định dạng ngữ cảnh
        context_parts = []
        for i, doc in enumerate(documents):
            context_parts.append(LinearAlgebraTemplates.format_document_for_context(doc, i))
        
        context = "\n\n".join(context_parts)
        
        # Định dạng nguồn
        sources = LinearAlgebraTemplates.format_sources(documents)
        
        # Áp dụng template
        rag_context = LinearAlgebraTemplates.get_rag_context_template().format(
            context=context,
            sources=sources
        )
        
        # Tạo prompt cuối cùng
        return f"""
{rag_context}

### Câu hỏi:
{user_question}

### Hướng dẫn trả lời:
- Hãy trả lời câu hỏi dựa trên thông tin trong tài liệu cung cấp ở trên.
- Nếu thông tin không đầy đủ, hãy bổ sung kiến thức của bạn nhưng nêu rõ đâu là thông tin từ tài liệu và đâu là từ kiến thức của bạn.
- Trả lời bằng tiếng Việt, trừ khi được yêu cầu khác.
- Trình bày từng bước giải một cách rõ ràng.
- Sử dụng các ký hiệu toán học và LaTeX khi cần thiết.
"""

# Template instance để sử dụng
linear_algebra_templates = LinearAlgebraTemplates() 
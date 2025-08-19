"""
Math Problem Templates cho format context và prompts
"""

import logging
from typing import List, Dict, Any, Optional
from langchain_core.documents import Document

logger = logging.getLogger(__name__)

class MathProblemTemplates:
    """Templates cho format math problems và context"""
    
    @staticmethod
    def format_problem_context(documents: List[Document], problem_only: bool = False) -> str:
        """
        Format context từ documents với cấu trúc mới
        
        Args:
            documents: Danh sách documents
            problem_only: Chỉ hiển thị đề bài, không hiển thị lời giải
            
        Returns:
            str: Context đã format
        """
        if not documents:
            return "Không tìm thấy tài liệu phù hợp."
        
        context_parts = []
        
        for i, doc in enumerate(documents[:3]):  # Giới hạn 3 documents
            metadata = doc.metadata if hasattr(doc, 'metadata') else {}
            
            # === HEADER INFORMATION ===
            header_info = MathProblemTemplates._format_document_header(metadata, i + 1)
            
            # === PROBLEM CONTENT ===
            problem_content = MathProblemTemplates._extract_problem_content(doc, metadata)
            
            # === SOLUTION CONTENT (nếu không phải problem_only) ===
            solution_content = ""
            if not problem_only:
                solution_content = MathProblemTemplates._extract_solution_content(doc, metadata)
            
            # === COMBINE DOCUMENT ===
            doc_text = f"=== {header_info} ===\n\n"
            
            if problem_content:
                doc_text += f"📝 **Đề bài:**\n{problem_content}\n\n"
            
            if solution_content:
                doc_text += f"💡 **Lời giải:**\n{solution_content}\n\n"
            
            # Thêm metadata bổ sung
            additional_info = MathProblemTemplates._format_additional_metadata(metadata)
            if additional_info:
                doc_text += f"ℹ️ **Thông tin bổ sung:** {additional_info}\n\n"
            
            context_parts.append(doc_text)
        
        return "\n".join(context_parts)
    
    @staticmethod
    def _format_document_header(metadata: Dict[str, Any], doc_number: int) -> str:
        """Format header cho document"""
        
        # Ưu tiên cấu trúc mới
        if metadata.get('category_display_name'):
            title = metadata['category_display_name']
        elif metadata.get('category') and metadata.get('subcategory'):
            category_map = {
                'dethi': 'Đề thi',
                'baitap': 'Bài tập'
            }
            subcategory_map = {
                'bangA': 'Bảng A',
                'bangB': 'Bảng B',
                'gtr': 'Giải tích',
                'hpt': 'Hệ phương trình',
                'dstuyentinh': 'Đại số tuyến tính'
            }
            
            category_name = category_map.get(metadata['category'], metadata['category'])
            subcategory_name = subcategory_map.get(metadata['subcategory'], metadata['subcategory'])
            title = f"{category_name} {subcategory_name}"
        else:
            title = metadata.get('title', f'Tài liệu {doc_number}')
        
        # Thêm thông tin năm và câu hỏi nếu có
        if metadata.get('year'):
            title += f" - Năm {metadata['year']}"
        
        if metadata.get('question'):
            title += f" - Bài {metadata['question']}"
        
        return title
    
    @staticmethod
    def _extract_problem_content(doc: Document, metadata: Dict[str, Any]) -> str:
        """Extract problem content từ document với hỗ trợ cấu trúc mới"""
        
        content = ""
        
        # Cấu trúc mới: problem_statement + problem_parts
        if metadata.get('problem_statement'):
            content = metadata['problem_statement']
            
            # Thêm problem_parts nếu có
            if metadata.get('problem_parts'):
                parts = metadata['problem_parts']
                if isinstance(parts, dict):
                    content += "\n\n"
                    for part_key, part_content in parts.items():
                        content += f"**{part_key})** {part_content}\n"
        
        # Cấu trúc cũ: page_content
        elif doc.page_content:
            content = doc.page_content
            
            # Nếu có suggested_solution, loại bỏ phần đó
            if metadata.get('suggested_solution'):
                # Tìm và cắt bỏ phần solution
                solution_keywords = ['lời giải', 'giải:', 'solution:', 'đáp án:', 'hướng dẫn giải']
                content_lower = content.lower()
                
                for keyword in solution_keywords:
                    if keyword in content_lower:
                        split_index = content_lower.find(keyword)
                        content = content[:split_index].strip()
                        break
        
        # Fallback: nếu vẫn chưa có content, thử lấy từ metadata.content
        if not content and metadata.get('content'):
            content = metadata['content']
        
        return content.strip()
    
    @staticmethod
    def _extract_solution_content(doc: Document, metadata: Dict[str, Any]) -> str:
        """Extract solution content từ document"""
        
        solution = ""
        
        # Cấu trúc mới: solution object
        if metadata.get('solution'):
            solution_data = metadata['solution']
            if isinstance(solution_data, dict):
                # Full solution
                if solution_data.get('full_solution'):
                    solution = solution_data['full_solution']
                
                # Solution parts
                if solution_data.get('solution_parts'):
                    parts = solution_data['solution_parts']
                    if isinstance(parts, dict):
                        solution += "\n\n**Chi tiết từng phần:**\n"
                        for part_key, part_solution in parts.items():
                            solution += f"**{part_key})** {part_solution}\n"
                
                # Solution method
                if solution_data.get('solution_method'):
                    method_map = {
                        'algebraic': 'Phương pháp đại số',
                        'geometric': 'Phương pháp hình học',
                        'analytical': 'Phương pháp giải tích'
                    }
                    method_name = method_map.get(solution_data['solution_method'], solution_data['solution_method'])
                    solution += f"\n\n**Phương pháp:** {method_name}"
            else:
                solution = str(solution_data)
        
        # Cấu trúc cũ: suggested_solution
        elif metadata.get('suggested_solution'):
            solution = metadata['suggested_solution']
        
        # Fallback: tìm trong page_content
        elif doc.page_content:
            content = doc.page_content
            solution_keywords = ['lời giải', 'giải:', 'solution:', 'đáp án:', 'hướng dẫn giải']
            content_lower = content.lower()
            
            for keyword in solution_keywords:
                if keyword in content_lower:
                    split_index = content_lower.find(keyword)
                    solution = content[split_index:].strip()
                    break
        
        return solution.strip()
    
    @staticmethod
    def _format_additional_metadata(metadata: Dict[str, Any]) -> str:
        """Format additional metadata information"""
        
        info_parts = []
        
        # Difficulty level
        if metadata.get('difficulty_level'):
            difficulty_map = {
                'co_ban': 'Cơ bản',
                'trung_binh': 'Trung bình',
                'kho': 'Khó',
                'quoc_gia': 'Olympic/Quốc gia'
            }
            difficulty_name = difficulty_map.get(metadata['difficulty_level'], metadata['difficulty_level'])
            info_parts.append(f"Độ khó: {difficulty_name}")
        
        # Subject area
        if metadata.get('subject_area'):
            subject_map = {
                'dai_so_tuyen_tinh': 'Đại số tuyến tính',
                'giai_tich': 'Giải tích',
                'hinh_hoc': 'Hình học',
                'xac_suat_thong_ke': 'Xác suất & Thống kê',
                'dai_so': 'Đại số'
            }
            subject_name = subject_map.get(metadata['subject_area'], metadata['subject_area'])
            info_parts.append(f"Lĩnh vực: {subject_name}")
        
        # Educational info
        if metadata.get('educational_info'):
            edu_info = metadata['educational_info']
            if isinstance(edu_info, dict):
                if edu_info.get('concepts'):
                    concepts = edu_info['concepts']
                    if isinstance(concepts, list):
                        info_parts.append(f"Khái niệm: {', '.join(concepts)}")
        
        # Tags (fallback)
        if not info_parts and metadata.get('tags'):
            tags = metadata['tags']
            if isinstance(tags, list):
                info_parts.append(f"Từ khóa: {', '.join(tags)}")
        
        return " | ".join(info_parts)
    
    @staticmethod
    def format_search_summary(query: str, documents: List[Document], metadata: Any) -> str:
        """
        Format tóm tắt kết quả search
        
        Args:
            query: Query gốc
            documents: Documents tìm được
            metadata: Metadata đã extract
            
        Returns:
            str: Tóm tắt kết quả
        """
        summary = f"🔍 **Tìm kiếm cho:** {query}\n\n"
        
        if not documents:
            summary += "❌ Không tìm thấy tài liệu phù hợp.\n"
            summary += "💡 Gợi ý: Thử tìm kiếm với từ khóa khác hoặc mở rộng phạm vi tìm kiếm."
            return summary
        
        # Thông tin metadata đã extract
        if hasattr(metadata, 'category') and metadata.category:
            summary += f"📂 **Loại tài liệu:** {metadata.category}\n"
        
        if hasattr(metadata, 'subject_area') and metadata.subject_area:
            subject_map = {
                'dai_so_tuyen_tinh': 'Đại số tuyến tính',
                'giai_tich': 'Giải tích',
                'hinh_hoc': 'Hình học',
                'xac_suat_thong_ke': 'Xác suất & Thống kê'
            }
            subject_name = subject_map.get(metadata.subject_area, metadata.subject_area)
            summary += f"🎯 **Lĩnh vực:** {subject_name}\n"
        
        if hasattr(metadata, 'difficulty_level') and metadata.difficulty_level:
            difficulty_map = {
                'co_ban': 'Cơ bản',
                'trung_binh': 'Trung bình',
                'kho': 'Khó',
                'quoc_gia': 'Olympic/Quốc gia'
            }
            difficulty_name = difficulty_map.get(metadata.difficulty_level, metadata.difficulty_level)
            summary += f"⭐ **Độ khó:** {difficulty_name}\n"
        
        summary += f"\n✅ **Tìm thấy {len(documents)} tài liệu phù hợp:**\n\n"
        
        return summary
    
    @staticmethod
    def format_no_results_message(query: str, metadata: Any) -> str:
        """
        Format message khi không tìm thấy kết quả
        
        Args:
            query: Query gốc
            metadata: Metadata đã extract
            
        Returns:
            str: Message không tìm thấy kết quả
        """
        message = f"❌ **Không tìm thấy tài liệu cho:** {query}\n\n"
        
        message += "💡 **Gợi ý:**\n"
        message += "• Thử sử dụng từ khóa khác\n"
        message += "• Mở rộng phạm vi tìm kiếm (bỏ bớt điều kiện lọc)\n"
        message += "• Kiểm tra chính tả\n"
        
        # Gợi ý dựa trên metadata
        if hasattr(metadata, 'subject_area') and metadata.subject_area:
            message += f"• Thử tìm kiếm chung về {metadata.subject_area}\n"
        
        if hasattr(metadata, 'category') and metadata.category:
            if metadata.category == 'dethi':
                message += "• Thử tìm 'bài tập' thay vì 'đề thi'\n"
            elif metadata.category == 'baitap':
                message += "• Thử tìm 'đề thi' thay vì 'bài tập'\n"
        
        return message
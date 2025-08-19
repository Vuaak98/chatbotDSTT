#!/usr/bin/env python3
"""
Smart LaTeX Translator - Dịch LaTeX thông minh dựa trên patterns phân tích
"""

import re
import time
from typing import Dict, List, Optional
from openai import OpenAI

class SmartLatexTranslator:
    """Dịch LaTeX thông minh với cache và pattern recognition"""
    
    def __init__(self, openai_client: OpenAI):
        self.client = openai_client
        self.cache = {}  # Cache để tránh dịch lại
        self.error_cache = {}  # Cache cho các lỗi để tránh retry vô ích
        self.translation_stats = {
            "total_calls": 0,
            "cache_hits": 0,
            "cot_matrix": 0,
            "cot_equation": 0,
            "cot_general": 0,
            "errors": 0
        }
        
        # Mapping cho các biến đơn giản
        self.simple_mappings = {
            'A': 'ma trận A',
            'B': 'ma trận B', 
            'P(x)': 'đa thức P của x',
            'n': 'n',
            'a': 'a',
            'x': 'x',
            'y': 'y',
            'z': 'z',
            't': 't',
            '\\lambda': 'lambda',
            '\\alpha': 'alpha',
            '\\beta': 'beta',
            '\\gamma': 'gamma',
            '\\det': 'định thức',
            '\\rank': 'hạng',
            '\\dim': 'số chiều',
            '\\mathbb{R}': 'tập số thực',
            '\\mathbb{C}': 'tập số phức',
            '\\mathbb{Z}': 'tập số nguyên',
            '\\in': 'thuộc',
            '\\subset': 'con của',
            '\\cup': 'hợp',
            '\\cap': 'giao',
            '\\neq': 'khác',
            '\\geq': 'lớn hơn hoặc bằng',
            '\\leq': 'nhỏ hơn hoặc bằng',
            '\\rightarrow': 'suy ra',
            '\\Rightarrow': 'kéo theo',
            '\\iff': 'khi và chỉ khi',
            '\\forall': 'với mọi',
            '\\exists': 'tồn tại',
            '\\sum': 'tổng',
            '\\prod': 'tích',
            '\\int': 'tích phân',
            '\\lim': 'giới hạn',
            '\\infty': 'vô cùng',
            '\\partial': 'đạo hàm riêng',
            '\\nabla': 'nabla',
            '\\times': 'nhân',
            '\\cdot': 'nhân',
            '\\div': 'chia',
            '\\pm': 'cộng trừ',
            '\\mp': 'trừ cộng'
        }
        
        # Patterns không nên dịch (giữ nguyên)
        self.keep_patterns = [
            r'^\d+$',  # Chỉ số
            r'^[a-zA-Z]$',  # Biến đơn
            r'^[a-zA-Z]_\d+$',  # Biến có chỉ số
            r'^\w+\s*=\s*\d+$',  # Gán giá trị đơn giản
        ]
    
    def should_keep_original(self, latex_text: str) -> bool:
        """Kiểm tra có nên giữ nguyên LaTeX không"""
        
        latex_text = latex_text.strip()
        
        # Kiểm tra patterns đơn giản
        for pattern in self.keep_patterns:
            if re.match(pattern, latex_text):
                return True
        
        # Quá ngắn
        if len(latex_text) < 3:
            return True
            
        # Chỉ chứa số và ký tự đơn giản
        if re.match(r'^[\w\s=\-+.,]+$', latex_text):
            return True
            
        return False
    
    def translate_simple_variable(self, latex_text: str) -> str:
        """Dịch biến đơn giản bằng mapping"""
        
        latex_text = latex_text.strip()
        
        # Kiểm tra mapping trực tiếp
        if latex_text in self.simple_mappings:
            return self.simple_mappings[latex_text]
        
        # Xử lý biến có chỉ số: a_1 -> a chỉ số 1
        if re.match(r'^[a-zA-Z]_\d+$', latex_text):
            var, idx = latex_text.split('_')
            return f"{var} chỉ số {idx}"
        
        # Xử lý biến có mũ: x^2 -> x bình phương
        if re.match(r'^[a-zA-Z]\^2$', latex_text):
            var = latex_text[0]
            return f"{var} bình phương"
        
        if re.match(r'^[a-zA-Z]\^3$', latex_text):
            var = latex_text[0]
            return f"{var} lập phương"
        
        # Xử lý phân số đơn giản: \frac{a}{b} -> a chia b
        frac_match = re.match(r'\\frac\{([^}]+)\}\{([^}]+)\}', latex_text)
        if frac_match:
            num, den = frac_match.groups()
            return f"{num} chia {den}"
        
        # Xử lý căn bậc hai: \sqrt{x} -> căn bậc hai của x
        sqrt_match = re.match(r'\\sqrt\{([^}]+)\}', latex_text)
        if sqrt_match:
            content = sqrt_match.group(1)
            return f"căn bậc hai của {content}"
        
        return latex_text
    
    def is_matrix_pattern(self, latex_text: str) -> bool:
        """Kiểm tra có phải pattern ma trận không"""
        return any(keyword in latex_text for keyword in [
            '\\begin{array}', '\\begin{matrix}', '\\begin{pmatrix}',
            '\\left(\\begin{array}', '\\left[\\begin{array}'
        ])
    
    def is_equation_system(self, latex_text: str) -> bool:
        """Kiểm tra có phải hệ phương trình không"""
        return any(keyword in latex_text for keyword in [
            '\\begin{aligned}', '\\begin{cases}', '\\left\\{',
            '\\begin{equation}', '\\begin{eqnarray}'
        ])
    
    def translate_with_ai(self, latex_text: str, context: str = "") -> str:
        """Dịch bằng AI với Chain-of-Thought prompting"""
        
        self.translation_stats["total_calls"] += 1
        
        # Kiểm tra cache
        cache_key = f"{latex_text}_{context}"
        if cache_key in self.cache:
            self.translation_stats["cache_hits"] += 1
            return self.cache[cache_key]
        
        # Kiểm tra error cache để tránh retry lỗi đã biết
        if cache_key in self.error_cache:
            return latex_text
        
        # Xác định loại content và prompt tương ứng
        if self.is_matrix_pattern(latex_text):
            self.translation_stats["cot_matrix"] += 1
            return self._translate_matrix_cot(latex_text, context)
        elif self.is_equation_system(latex_text):
            self.translation_stats["cot_equation"] += 1
            return self._translate_equation_system_cot(latex_text, context)
        else:
            self.translation_stats["cot_general"] += 1
            return self._translate_general_expression_cot(latex_text, context)
    
    def _translate_matrix_cot(self, latex_text: str, context: str) -> str:
        """Chain-of-Thought prompting cho ma trận"""
        
        # Rút gọn LaTeX nếu quá dài
        if len(latex_text) > 500:
            latex_preview = latex_text[:300] + "... [đã rút gọn]"
        else:
            latex_preview = latex_text

        prompt = f"""
Bạn là một nhà toán học chuyên gia. Dịch ma trận LaTeX sau thành tiếng Việt tự nhiên. Hãy suy nghĩ từng bước:

Đầu vào LaTeX:
{latex_preview}

Hãy suy nghĩ từng bước:
1. **Xác định cấu trúc:** Phân tích môi trường LaTeX (pmatrix, array, matrix...) và dấu phân cách.
2. **Xác định kích thước:** Đếm số hàng (phân tách bởi \\\\) và số cột (phân tách bởi &).
3. **Liệt kê các phần tử:** Mô tả nội dung từng hàng một cách có hệ thống.
4. **Tổng hợp mô tả:** Kết hợp thành mô tả ngắn gọn, dễ hiểu.

Mô tả cuối cùng (chỉ trả về phần này):"""
        
        return self._call_openai_api(prompt, latex_text, context)
    
    def _translate_equation_system_cot(self, latex_text: str, context: str) -> str:
        """Chain-of-Thought prompting cho hệ phương trình"""
        
        if len(latex_text) > 500:
            latex_preview = latex_text[:300] + "... [đã rút gọn]"
        else:
            latex_preview = latex_text

        prompt = f"""
Bạn là một nhà toán học chuyên gia. Dịch hệ phương trình LaTeX sau thành tiếng Việt tự nhiên. Hãy suy nghĩ từng bước:

Đầu vào LaTeX:
{latex_preview}

Hãy suy nghĩ từng bước:
1. **Xác định cấu trúc:** Phân tích môi trường LaTeX (aligned, cases, equation...).
2. **Đếm số phương trình:** Xác định số lượng phương trình trong hệ.
3. **Phân tích từng phương trình:** Mô tả nội dung và mối quan hệ giữa các biến.
4. **Tổng hợp mô tả:** Kết hợp thành mô tả ngắn gọn về hệ phương trình.

Mô tả cuối cùng (chỉ trả về phần này):"""
        
        return self._call_openai_api(prompt, latex_text, context)
    
    def _translate_general_expression_cot(self, latex_text: str, context: str) -> str:
        """Chain-of-Thought prompting cho biểu thức toán học tổng quát"""
        
        if len(latex_text) > 500:
            latex_preview = latex_text[:300] + "... [đã rút gọn]"
        else:
            latex_preview = latex_text

        prompt = f"""
Bạn là một nhà toán học chuyên gia. Dịch biểu thức toán học LaTeX sau thành tiếng Việt tự nhiên. Hãy suy nghĩ từng bước:

Đầu vào LaTeX:
{latex_preview}

Hãy suy nghĩ từng bước:
1. **Xác định thành phần chính:** Phân tích các ký hiệu, hàm số, toán tử chính.
2. **Xác định cấu trúc:** Phân tích thứ tự ưu tiên và nhóm các phần tử.
3. **Mô tả từng phần:** Giải thích ý nghĩa của từng thành phần quan trọng.
4. **Tổng hợp mô tả:** Kết hợp thành mô tả ngắn gọn, dễ hiểu.

Mô tả cuối cùng (chỉ trả về phần này):"""
        
        return self._call_openai_api(prompt, latex_text, context)
    
    def _call_openai_api(self, prompt: str, latex_text: str, context: str) -> str:
        """Gọi OpenAI API với error handling và caching"""
        
        cache_key = f"{latex_text}_{context}"
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,  # Tăng cho CoT
                temperature=0.1
            )
            
            translated = response.choices[0].message.content.strip()
            
            # Lưu cache
            self.cache[cache_key] = translated
            
            # Rate limiting
            time.sleep(0.2)
            
            return translated
            
        except Exception as e:
            print(f"❌ Lỗi dịch AI: {e}")
            self.translation_stats["errors"] += 1
            
            # Lưu vào error cache để tránh retry
            self.error_cache[cache_key] = str(e)
            
            time.sleep(1)
            return latex_text
    
    def get_translation_stats(self) -> dict:
        """Trả về thống kê translation để đánh giá hiệu suất"""
        stats = self.translation_stats.copy()
        if stats["total_calls"] > 0:
            stats["cache_hit_rate"] = stats["cache_hits"] / stats["total_calls"]
            stats["error_rate"] = stats["errors"] / stats["total_calls"]
        return stats
    
    def clear_caches(self):
        """Xóa cache để tiết kiệm memory"""
        self.cache.clear()
        self.error_cache.clear()
        print("🧹 Đã xóa translation caches")
    
    def translate(self, text: str, context: str = "") -> str:
        """Function chính để dịch text có chứa LaTeX"""
        
        if not text or not text.strip():
            return text
        
        # Không có LaTeX
        if not any(symbol in text for symbol in ['$', '\\', '{', '}']):
            return text
        
        result = text
        
        # 1. Xử lý display math $$...$$
        def replace_display_math(match):
            latex_content = match.group(1).strip()
            
            if self.should_keep_original(latex_content):
                return f"$${latex_content}$$"
            
            if len(latex_content) > 200:  # Quá phức tạp
                if self.is_matrix_pattern(latex_content):
                    return "ma trận phức tạp"
                elif self.is_equation_system(latex_content):
                    return "hệ phương trình phức tạp"
                else:
                    return "biểu thức toán học phức tạp"
            
            translated = self.translate_with_ai(latex_content, context)
            return translated
        
        result = re.sub(r'\$\$([^$]+)\$\$', replace_display_math, result, flags=re.DOTALL)
        
        # 2. Xử lý inline math $...$
        def replace_inline_math(match):
            latex_content = match.group(1).strip()
            
            if self.should_keep_original(latex_content):
                return latex_content
            
            # Thử dịch đơn giản trước
            simple_translation = self.translate_simple_variable(latex_content)
            if simple_translation != latex_content:
                return simple_translation
            
            # Nếu phức tạp, dùng AI
            if len(latex_content) > 50:
                translated = self.translate_with_ai(latex_content, context)
                return translated
            else:
                return latex_content
        
        result = re.sub(r'\$([^$]+)\$', replace_inline_math, result)
        
        return result

# Test function
def test_translator():
    """Test translator với các cases thực tế"""
    
    from openai import OpenAI
    import os
    from dotenv import load_dotenv
    
    load_dotenv('data/.env')
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    translator = SmartLatexTranslator(client)
    
    test_cases = [
        # Test Chain-of-Thought cho ma trận
        {
            "input": "$$A=\\left(\\begin{array}{cc}1 & 2 \\\\ 3 & 4\\end{array}\\right)$$",
            "type": "Matrix CoT",
            "context": "Đại số tuyến tính"
        },
        # Test Chain-of-Thought cho hệ phương trình
        {
            "input": "$$\\begin{cases} x + y = 5 \\\\ 2x - y = 1 \\end{cases}$$",
            "type": "Equation System CoT", 
            "context": "Hệ phương trình"
        },
        # Test biểu thức tổng quát
        {
            "input": "Tính $\\int_0^\\pi \\sin(x) dx$",
            "type": "General Expression CoT",
            "context": "Giải tích"
        },
        # Test simple mapping (không dùng AI)
        {
            "input": "Ma trận $A$ có định thức $\\det(A) = 5$",
            "type": "Simple Mapping",
            "context": ""
        },
        # Test ma trận phức tạp
        {
            "input": "$$A=\\left(\\begin{array}{cccc}1 & a+1 & a+2 & 0 \\\\ a+3 & 1 & 0 & a+2 \\\\ a+2 & 0 & 1 & a+1 \\\\ 0 & a+2 & a+3 & 1\\end{array}\\right)$$",
            "type": "Complex Matrix CoT",
            "context": "Olympic toán học"
        }
    ]
    
    print("TEST SMART LATEX TRANSLATOR WITH CHAIN-OF-THOUGHT:")
    print("=" * 60)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}. [{test['type']}]")
        print(f"   Input: {test['input']}")
        print(f"   Context: {test['context']}")
        
        start_time = time.time()
        result = translator.translate(test['input'], test['context'])
        end_time = time.time()
        
        print(f"   Output: {result}")
        print(f"   Time: {end_time - start_time:.2f}s")
        print("-" * 50)
    
    # Hiển thị thống kê
    print("\nTRANSLATION STATISTICS:")
    stats = translator.get_translation_stats()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"   {key}: {value:.2%}")
        else:
            print(f"   {key}: {value}")

if __name__ == "__main__":
    test_translator()

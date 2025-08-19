#!/usr/bin/env python3
"""
Xử lý kỷ yếu đại số tuyến tính: Chuyển đổi MD sang JSON
- Nguồn: Kỷ yếu đại số tuyến tính các năm (PDF → Mathpix → MD)
- Cấu trúc: 2 loại đề thi (bangA, bangB) + 7 dạng bài tập
- Output: JSON tối ưu cho RAG system
"""

import os
import re
import json
import logging
import datetime
import itertools
import unicodedata
import uuid

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("final_md_to_json_processor.log", mode='w', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# ========================
# CATEGORY MAPPING - Hệ thống phân loại 2 cấp hoàn chỉnh
# ========================

CATEGORY_MAPPING = {
    # Đề thi Olympic
    "dethi_bangA": {
        "category": "dethi",
        "subcategory": "bangA",
        "display_name": "Đề thi Olympic Bảng A",
        "description": "Các đề thi Olympic Toán học sinh viên bảng A - dành cho sinh viên năm 1, 2",
        "difficulty_level": "quoc_gia",
        "keywords": ["đề thi", "thi", "olympic", "thi đấu", "bảng A", "bang A", "bảng a"]
    },
    "dethi_bangB": {
        "category": "dethi", 
        "subcategory": "bangB",
        "display_name": "Đề thi Olympic Bảng B",
        "description": "Các đề thi Olympic Toán học sinh viên bảng B - dành cho sinh viên năm 3, 4",
        "difficulty_level": "quoc_gia",
        "keywords": ["đề thi", "thi", "olympic", "thi đấu", "bảng B", "bang B", "bảng b"]
    },
    
    # 7 dạng bài tập
    "GTR": {
        "category": "baitap",
        "subcategory": "gtr", 
        "display_name": "Giá trị riêng - Vector riêng",
        "description": "Bài tập về giá trị riêng và vector riêng của ma trận",
        "difficulty_level": "olympic",
        "keywords": ["bài tập", "luyện tập", "dạng bài", "giá trị riêng", "vector riêng", "eigenvalue", "eigenvector"]
    },
    "HPT": {
        "category": "baitap",
        "subcategory": "hpt",
        "display_name": "Hệ phương trình tuyến tính", 
        "description": "Bài tập về hệ phương trình tuyến tính và phương pháp giải",
        "difficulty_level": "olympic",
        "keywords": ["bài tập", "luyện tập", "dạng bài", "hệ phương trình", "phương trình tuyến tính", "system"]
    },
    "KGVT": {
        "category": "baitap",
        "subcategory": "kgvt",
        "display_name": "Không gian vector",
        "description": "Bài tập về không gian vector và ánh xạ tuyến tính",
        "difficulty_level": "olympic", 
        "keywords": ["bài tập", "luyện tập", "dạng bài", "không gian vector", "ánh xạ tuyến tính", "vector space"]
    },
    "MT": {
        "category": "baitap",
        "subcategory": "mt",
        "display_name": "Ma trận",
        "description": "Bài tập về ma trận và các phép toán ma trận",
        "difficulty_level": "olympic",
        "keywords": ["bài tập", "luyện tập", "dạng bài", "ma trận", "matrix", "phép toán ma trận"]
    },
    "ToHop": {
        "category": "baitap", 
        "subcategory": "tohop",
        "display_name": "Tổ hợp tuyến tính",
        "description": "Bài tập về tổ hợp tuyến tính và độc lập tuyến tính",
        "difficulty_level": "olympic",
        "keywords": ["bài tập", "luyện tập", "dạng bài", "tổ hợp tuyến tính", "độc lập tuyến tính", "linear combination"]
    },
    "DaThuc": {
        "category": "baitap",
        "subcategory": "dathuc", 
        "display_name": "Đa thức",
        "description": "Bài tập về đa thức và không gian đa thức",
        "difficulty_level": "olympic",
        "keywords": ["bài tập", "luyện tập", "dạng bài", "đa thức", "polynomial", "không gian đa thức"]
    },
    "DT": {
        "category": "baitap",
        "subcategory": "dt",
        "display_name": "Định thức", 
        "description": "Bài tập về định thức và tính chất định thức",
        "difficulty_level": "olympic",
        "keywords": ["bài tập", "luyện tập", "dạng bài", "định thức", "determinant", "det"]
    }
}

# Cấu hình
IMAGE_BASE_URL = "https://cdn.mathpix.com/"
ALL_CREATED_IDS = set()

# ========================
# UTILITY FUNCTIONS
# ========================

def get_category_info(filename):
    """Lấy thông tin category từ tên file"""
    filename_lower = filename.lower()
    
    logging.info(f"🔍 Phân tích file: {filename}")
    
    # Kiểm tra đề thi
    if "dethi" in filename_lower:
        if "banga" in filename_lower:
            logging.info(f"   → Phân loại: Đề thi Bảng A")
            return CATEGORY_MAPPING["dethi_bangA"]
        elif "bangb" in filename_lower:
            logging.info(f"   → Phân loại: Đề thi Bảng B")
            return CATEGORY_MAPPING["dethi_bangB"]
        else:
            logging.warning(f"   → Đề thi không rõ bảng, mặc định Bảng A")
            return CATEGORY_MAPPING["dethi_bangA"]
    
    # Kiểm tra bài tập theo 7 dạng
    for topic_code in ["GTR", "HPT", "KGVT", "MT", "ToHop", "DaThuc", "DT"]:
        if topic_code.lower() in filename_lower:
            logging.info(f"   → Phân loại: Bài tập {CATEGORY_MAPPING[topic_code]['display_name']}")
            return CATEGORY_MAPPING[topic_code]
    
    # Default fallback
    logging.warning(f"   → Không nhận diện được, dùng mặc định")
    return {
        "category": "baitap",
        "subcategory": "general",
        "display_name": "Bài tập tổng hợp",
        "description": "Bài tập tổng hợp các chủ đề",
        "difficulty_level": "olympic",
        "keywords": ["bài tập", "luyện tập", "dạng bài"]
    }

def replace_images_with_placeholders(text):
    """Thay thế hình ảnh bằng placeholder và trả về danh sách URLs"""
    image_urls = re.findall(r'!\[.*?\]\((.*?)\)', text)
    if not image_urls:
        return text, []

    counter = itertools.count(1)
    
    def replacer(match):
        return f"[IMAGE_{next(counter)}]"

    modified_text = re.sub(r'!\[.*?\]\((.*?)\)', replacer, text)
    return modified_text, image_urls

def normalize_image_url(url):
    """Chuẩn hóa đường dẫn ảnh"""
    if url.startswith('/') or url.startswith('.\\') or url.startswith('./'):
        filename = os.path.basename(url)
        return f"{IMAGE_BASE_URL}{filename}"
    
    if url.startswith('http://') or url.startswith('https://'):
        return url
    
    return f"{IMAGE_BASE_URL}{url}"

def get_format_type(filename):
    """Nhận diện loại file: 'exam' cho đề thi, 'topic' cho dạng bài tập"""
    return "exam" if "dethi" in filename.lower() else "topic"

# ========================
# PARSING FUNCTIONS - Kết hợp từ cả 2 file gốc
# ========================

def split_bai(text, format_type=None):
    """
    Tách các bài lớn trong file markdown
    Kết hợp logic từ cả 2 file gốc để xử lý mọi trường hợp
    """
    # Chuẩn hóa dòng
    text = re.sub(r'\r\n|\r', '\n', text)
    text = re.sub(r'(?<!\n)(Bài\s+\d+\.)', r'\n\1', text)
    
    # Tự động xác định format_type nếu không được cung cấp
    if format_type is None:
        if re.search(r'\nBài\s+\d+\.\d+', text):
            format_type = "topic"
        else:
            format_type = "exam"
    
    if format_type == "exam":
        # Đề thi: Bài 1., Bài 2., ...
        pattern = r'\n(Bài\s+\d+\.)([\s\S]*?)(?=\nBài\s+\d+\.|\Z)'
    else:
        # Bài tập: Bài 5.1, Bài 5.2, ...
        pattern = r'\n(Bài\s+\d+\.\d+)([\s\S]*?)(?=\nBài\s+\d+\.\d+|\Z)'
    
    matches = re.findall(pattern, text)
    result = {}
    
    for m in matches:
        # m[0]: tiêu đề bài, m[1]: nội dung
        match_num = re.match(r'Bài\s*(\d+(?:\.\d+)?).*', m[0])
        key = match_num.group(1) if match_num else str(len(result)+1)
        # Ghép lại tiêu đề + nội dung
        result[key] = (m[0] + '\n' + m[1]).strip()
    
    return result

def split_problem_parts(text):
    """
    Tách các ý nhỏ (a), (b), (c) trong một bài
    Trả về problem_statement và problem_parts riêng biệt
    """
    text = re.sub(r'\r\n|\r|\n', '\n', text)
    
    # Tìm ý đầu tiên để tách problem_statement
    first_part_match = re.search(r'(?:^|[\n\.])\s*\(([a-hj-zA-HJ-Z])\)\s*[:\.]?\s*', text)
    
    if not first_part_match:
        # Không có ý con, toàn bộ là problem_statement
        return text.strip(), {}
    
    # Tách problem_statement (phần trước ý đầu tiên)
    problem_statement = text[:first_part_match.start()].strip()
    
    # Tách các ý con
    pattern = r'(?:^|[\n\.])\s*\(([a-hj-zA-HJ-Z])\)\s*[:\.]?\s*'
    matches = list(re.finditer(pattern, text, flags=re.DOTALL))
    
    problem_parts = {}
    for idx, m in enumerate(matches):
        key = m.group(1).lower()
        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        content = text[start:end].strip()
        
        # Loại bỏ dấu : hoặc . đầu dòng nếu còn sót
        while content and content[0] in ":. ":
            content = content[1:].strip()
        
        problem_parts[key] = content
    
    return problem_statement, problem_parts

def split_solution_parts(text):
    """
    Tách lời giải thành các phần tương ứng với các ý a, b, c
    """
    text = re.sub(r'\r\n|\r|\n', '\n', text)
    
    # Tìm pattern cho lời giải từng ý
    pattern = r'(?:^|[\n\.])\s*\(([a-hj-zA-HJ-Z])\)\s*[:\.]?\s*'
    matches = list(re.finditer(pattern, text, flags=re.DOTALL))
    
    if not matches:
        # Không có ý con, toàn bộ là lời giải chung
        return text.strip(), {}
    
    # Lời giải chung (phần trước ý đầu tiên)
    full_solution = text[:matches[0].start()].strip()
    
    # Tách lời giải từng ý
    solution_parts = {}
    for idx, m in enumerate(matches):
        key = m.group(1).lower()
        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        content = text[start:end].strip()
        
        # Loại bỏ dấu : hoặc . đầu dòng nếu còn sót
        while content and content[0] in ":. ":
            content = content[1:].strip()
        
        solution_parts[key] = content
    
    return full_solution, solution_parts

def extract_school_info(text):
    """Trích xuất thông tin trường đại học từ text"""
    school_pattern = r'\(([^)]*(?:ĐH|Đại học|University)[^)]*)\)'
    matches = re.findall(school_pattern, text, re.IGNORECASE)
    return matches[0] if matches else ""

def extract_question_number(text, format_type=None):
    """Trích xuất số câu hỏi từ text"""
    if format_type == "exam":
        match = re.search(r'Bài\s+(\d+)', text)
        return match.group(1) if match else "1"
    else:
        match = re.search(r'Bài\s+([\d\.]+)', text)
        return match.group(1) if match else "1"

# Đã loại bỏ các function tự sinh thông tin không chính xác:
# - auto_tags(): Tạo tags không đáng tin cậy
# - extract_concepts(): Mapping cứng không phản ánh nội dung thực

# ========================
# MAIN PROCESSING FUNCTION
# ========================

def create_problem_object_new_structure(bt_content, lg_content, metadata, category_info):
    """
    Tạo object bài toán với cấu trúc JSON mới - tách biệt đề bài và lời giải
    """
    # Xử lý hình ảnh
    bt_clean, bt_images = replace_images_with_placeholders(bt_content)
    lg_clean, lg_images = replace_images_with_placeholders(lg_content)
    
    # Chuẩn hóa URLs hình ảnh
    all_images = []
    for i, url in enumerate(bt_images + lg_images):
        all_images.append({
            "id": f"IMAGE_{i+1}",
            "url": normalize_image_url(url),
            "description": f"Hình ảnh {i+1}",
            "position": "in_content" if i < len(bt_images) else "in_solution"
        })
    
    # Tách đề bài thành statement và parts
    problem_statement, problem_parts = split_problem_parts(bt_clean)
    
    # Tách lời giải thành full solution và parts
    full_solution, solution_parts = split_solution_parts(lg_clean)
    
    # Loại bỏ tất cả thông tin tự sinh không chính xác
    # concepts = extract_concepts(bt_content + " " + lg_content, category_info)
    # tags = auto_tags(bt_content + " " + lg_content, category_info)
    
    # Tạo object theo cấu trúc mới
    problem_object = {
        "id": metadata["id"],
        "category": category_info["category"],
        "subcategory": category_info["subcategory"],
        
        # Metadata cho kỷ yếu đại số tuyến tính
        "metadata": {
            "year": metadata["year"],
            "source_file": metadata["source"],
            "subject": "dai_so_tuyen_tinh",
            "document_type": "ky_yeu",
            "category_name": category_info["display_name"],
            "difficulty": category_info["difficulty_level"],
            "created_at": datetime.datetime.now().isoformat()
        },
        
        # Nội dung bài toán (tách biệt)
        "problem_statement": problem_statement,
        "problem_parts": problem_parts,
        "images": all_images,
        
        # Lời giải (tách biệt)
        "solution": {
            "full_solution": full_solution,
            "solution_parts": solution_parts
        },
        
        # Loại bỏ educational_info tự sinh không chính xác
        
        # Thông tin bổ sung
        "title": metadata["title"],
        "question_number": metadata["question"],
        "source_path": metadata.get("source_md", "")
    }
    
    return problem_object

def process_one_pair_final(bt_path, lg_path, year, category_info, output_json_path, id_prefix="2024"):
    """
    Xử lý một cặp file BT + LG thành JSON với cấu trúc mới hoàn chỉnh
    """
    logging.info(f"📄 Xử lý cặp: {os.path.basename(bt_path)} + {os.path.basename(lg_path)}")
    
    try:
        # Đọc file BT và LG
        with open(bt_path, 'r', encoding='utf-8') as f:
            bt_content = f.read()
        
        with open(lg_path, 'r', encoding='utf-8') as f:
            lg_content = f.read()
        
        # Xác định format type
        format_type = get_format_type(os.path.basename(bt_path))
        
        # Tách các bài
        bt_problems = split_bai(bt_content, format_type)
        lg_solutions = split_bai(lg_content, format_type)
        
        logging.info(f"   📝 Tìm thấy {len(bt_problems)} bài tập, {len(lg_solutions)} lời giải")
        
        # Ghép bài tập với lời giải
        problems = []
        for ma_bai in bt_problems:
            bt_problem = bt_problems.get(ma_bai, "")
            lg_solution = lg_solutions.get(ma_bai, "")
            
            if not bt_problem.strip():
                continue
            
            # Trích xuất metadata
            school_info = extract_school_info(bt_problem)
            question_num = extract_question_number(bt_problem, format_type)
            
            # Tạo ID unique
            base_name = os.path.splitext(os.path.basename(bt_path))[0].lower()
            problem_id = f"{year}-{id_prefix}-{base_name}-{ma_bai.replace('.', '')}"
            
            # Kiểm tra trùng lặp ID
            if problem_id in ALL_CREATED_IDS:
                counter = 1
                while f"{problem_id}-{counter}" in ALL_CREATED_IDS:
                    counter += 1
                problem_id = f"{problem_id}-{counter}"
            
            ALL_CREATED_IDS.add(problem_id)
            
            # Tạo title
            if format_type == "exam":
                title = f"Đề thi Olympic {year} - Bài {ma_bai} ({category_info['subcategory'].upper()})"
            else:
                title = f"Bài {ma_bai}: {category_info['display_name']}"
            
            # Metadata
            metadata = {
                "id": problem_id,
                "title": title,
                "year": year,
                "exam": "Olympic" if format_type == "exam" else "Tổng hợp",
                "question": ma_bai,
                "source_school": f"{school_info} {year}" if school_info else "",
                "source": os.path.basename(bt_path),
                "source_md": bt_path
            }
            
            # Tạo object bài toán với cấu trúc mới
            problem_obj = create_problem_object_new_structure(
                bt_content=bt_problem,
                lg_content=lg_solution,
                metadata=metadata,
                category_info=category_info
            )
            
            problems.append(problem_obj)
        
        # Lưu JSON
        os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(problems, f, ensure_ascii=False, indent=2)
        
        logging.info(f"✅ Đã lưu {len(problems)} bài vào {output_json_path}")
        return len(problems)
        
    except Exception as e:
        logging.error(f"❌ Lỗi xử lý {bt_path}: {str(e)}")
        return 0

def auto_process_all_final(root_dir="data/raw", output_root="data/processed/final"):
    """
    Tự động xử lý tất cả file MD với cấu trúc JSON mới hoàn chỉnh
    """
    logging.info("🚀 Bắt đầu xử lý tất cả file MD với cấu trúc JSON mới...")
    total_files_processed = 0
    total_problems_created = 0
    
    # Xóa tập hợp ID toàn cục trước khi bắt đầu
    ALL_CREATED_IDS.clear()
    
    # Xử lý thư mục 2024, 2023, 2018 (có thể mở rộng cho các năm khác)
    for year_folder in ["2024", "2023", "2018"]:
        year_path = os.path.join(root_dir, year_folder)
        if not os.path.exists(year_path):
            continue
            
        bt_dir = os.path.join(year_path, "BT")
        lg_dir = os.path.join(year_path, "LG")
        
        if not (os.path.isdir(bt_dir) and os.path.isdir(lg_dir)):
            logging.warning(f"⚠️ Bỏ qua {year_folder}: không tìm thấy cấu trúc BT/LG")
            continue
            
        logging.info(f"📂 Đang xử lý năm {year_folder}...")
        bt_files = [f for f in os.listdir(bt_dir) if f.endswith(".md")]
        lg_files = [f for f in os.listdir(lg_dir) if f.endswith(".md")]
        
        # Tạo cấu trúc thư mục output theo category
        output_year_dir = os.path.join(output_root, year_folder)
        os.makedirs(output_year_dir, exist_ok=True)
        
        for bt_file in bt_files:
            # Lấy thông tin category
            category_info = get_category_info(bt_file)
            
            # Tìm file lời giải tương ứng với logic linh hoạt cho mọi năm
            base_name = bt_file.replace("BT_", "").replace(".md", "")
            lg_file = None
            
            # Tìm file LG tương ứng với pattern khác nhau theo năm
            for lf in lg_files:
                # Pattern năm 2024: LG_BT_DaThuc_2024.md
                # Pattern năm 2018: LG_DaThuc_2018.md
                # Pattern đề thi: LG_dethi_bangA_2024.md (giống nhau)
                
                if f"LG_BT_{base_name}" in lf:  # Pattern 2024 cho bài tập
                    lg_file = lf
                    break
                elif f"LG_{base_name}" in lf:  # Pattern 2018 hoặc đề thi
                    lg_file = lf
                    break
            
            if not lg_file:
                logging.warning(f"⚠️ Không tìm thấy lời giải cho {bt_file}")
                continue
                
            bt_path = os.path.join(bt_dir, bt_file)
            lg_path = os.path.join(lg_dir, lg_file)
            
            # Tạo đường dẫn output theo category
            category_dir = os.path.join(output_year_dir, category_info["category"], category_info["subcategory"])
            os.makedirs(category_dir, exist_ok=True)
            
            output_filename = f"{base_name}.json"
            output_json_path = os.path.join(category_dir, output_filename)
            
            # Xử lý cặp file
            problems_count = process_one_pair_final(
                bt_path=bt_path,
                lg_path=lg_path,
                year=int(year_folder),
                category_info=category_info,
                output_json_path=output_json_path,
                id_prefix=year_folder
            )
            
            if problems_count > 0:
                total_files_processed += 1
                total_problems_created += problems_count
    
    # Tạo summary report
    create_processing_summary(output_root, total_files_processed, total_problems_created)
    
    logging.info(f"✅ Hoàn tất xử lý:")
    logging.info(f"   📁 {total_files_processed} cặp file đã xử lý")
    logging.info(f"   📝 {total_problems_created} bài toán đã tạo")
    logging.info(f"   💾 Dữ liệu lưu trong: {output_root}")
    
    return total_files_processed, total_problems_created

def create_processing_summary(output_root, total_files, total_problems):
    """Tạo báo cáo tổng kết quá trình xử lý"""
    summary = {
        "processing_info": {
            "timestamp": datetime.datetime.now().isoformat(),
            "total_files_processed": total_files,
            "total_problems_created": total_problems,
            "output_directory": output_root
        },
        "data_structure": {
            "schema_version": "2.0",
            "features": [
                "Separated problem statement and solution",
                "Hierarchical categorization (category + subcategory)",
                "Rich metadata for filtering",
                "Educational information",
                "Image handling with placeholders",
                "Backward compatibility"
            ]
        },
        "categories": {
            "dethi": {
                "subcategories": ["bangA", "bangB"],
                "description": "Olympic exam problems"
            },
            "baitap": {
                "subcategories": ["gtr", "hpt", "kgvt", "mt", "tohop", "dathuc", "dt"],
                "description": "Exercise problems by topic"
            }
        }
    }
    
    summary_path = os.path.join(output_root, "processing_summary.json")
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    logging.info(f"📊 Đã tạo báo cáo tổng kết: {summary_path}")

if __name__ == "__main__":
    # Chạy xử lý tự động với cấu trúc mới
    total_files, total_problems = auto_process_all_final()
    
    logging.info("🎉 Hoàn thành xử lý với cấu trúc JSON mới!")
    logging.info("📋 Cấu trúc dữ liệu:")
    logging.info("   ✓ Tách biệt đề bài và lời giải")
    logging.info("   ✓ Phân loại 2 cấp (category + subcategory)")
    logging.info("   ✓ Metadata đầy đủ cho chatbot")
    logging.info("   ✓ Thông tin giáo dục bổ sung")
    logging.info("   ✓ Backward compatibility")
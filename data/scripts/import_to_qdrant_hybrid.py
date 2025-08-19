#!/usr/bin/env python3
"""
Import dữ liệu vào Qdrant Cloud với chiến lược HYBRID
- Filter chính xác + Semantic search
- Metadata đầy đủ cho filtering
- Embedding text tối ưu (giữ nguyên LaTeX + context)
"""

import os
import json
import logging
import time
import re
import hashlib
from tqdm import tqdm
from dotenv import load_dotenv
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.http import models
import glob

# Load environment variables from backend/.env
load_dotenv("backend/.env")

# Cấu hình từ environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "math_collection")

# Khởi tạo clients
client = OpenAI(api_key=OPENAI_API_KEY)
qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

# Cấu hình
EMBEDDING_MODEL = "text-embedding-3-small"
VECTOR_SIZE = 1536

# Import Smart Translator
import sys
sys.path.append('data/scripts')
from smart_latex_translator import SmartLatexTranslator

# Khởi tạo translator
smart_translator = SmartLatexTranslator(client)

def create_numeric_id(string_id):
    """Tạo numeric ID từ string ID để tương thích với Qdrant Cloud"""
    # Sử dụng hash để tạo ID số nguyên duy nhất
    hash_object = hashlib.md5(string_id.encode())
    # Lấy 8 bytes đầu và convert thành int
    numeric_id = int.from_bytes(hash_object.digest()[:8], byteorder='big')
    # Đảm bảo là số dương
    return abs(numeric_id)

def translate_latex_to_natural(latex_text, context=""):
    """Dịch LaTeX thành văn bản tự nhiên bằng Smart Translator"""
    
    if not latex_text or not latex_text.strip():
        return latex_text
    
    try:
        # Sử dụng Smart Translator
        translated = smart_translator.translate(latex_text, context)
        return translated
        
    except Exception as e:
        print(f"❌ Lỗi dịch LaTeX: {e}")
        return latex_text

def create_enhanced_embedding_text(item):
    """Tạo text cho embedding - Tập trung vào đề bài với LaTeX translation"""
    
    parts = []
    
    # === METADATA CONTEXT ===
    parts.append(f"Chủ đề: {item['metadata']['category_name']}")
    parts.append(f"Năm: {item['metadata']['year']}")
    parts.append(f"Loại: {item['category']} {item['subcategory']}")
    
    # === NỘI DUNG ĐỀ BÀI (DỊCH LaTeX) - TRỌNG TÂM ===
    context = f"{item['metadata']['category_name']} - {item['category']}"
    problem_natural = translate_latex_to_natural(item['problem_statement'], context)
    parts.append(f"Đề bài: {problem_natural}")
    
    # Thêm problem parts (dịch)
    for part_key, part_content in item["problem_parts"].items():
        part_natural = translate_latex_to_natural(part_content, context)
        parts.append(f"({part_key}) {part_natural}")
    
    # === TITLE ===
    parts.append(item['title'])
    
    # === THÊM CONTEXT TỪ LỜI GIẢI (NHẸ) ===
    # Chỉ thêm 1 dòng tóm tắt để cải thiện context
    if item.get('solution', {}).get('full_solution'):
        solution_preview = item['solution']['full_solution'][:100] + "..."
        solution_natural = translate_latex_to_natural(solution_preview, context)
        parts.append(f"Phương pháp: {solution_natural}")
    
    return "\n".join(parts)

def get_embedding(text):
    """Tạo semantic embedding từ OpenAI"""
    try:
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"❌ Lỗi tạo embedding: {e}")
        return None

def create_keyword_vector(text):
    """Tạo keyword vector (sparse) cho hybrid search - Simple TF-IDF approach"""
    
    # Simple keyword extraction cho Vietnamese math terms
    import re
    from collections import Counter
    
    # Normalize text
    text_lower = text.lower()
    
    # Extract important math keywords
    math_keywords = [
        'ma trận', 'matrix', 'định thức', 'det', 'hạng', 'rank',
        'phương trình', 'equation', 'hệ', 'system', 'nghiệm', 'solution',
        'giá trị riêng', 'eigenvalue', 'vector riêng', 'eigenvector',
        'không gian', 'space', 'tuyến tính', 'linear', 'độc lập', 'independent',
        'tích phân', 'integral', 'đạo hàm', 'derivative', 'giới hạn', 'limit',
        'tổ hợp', 'combination', 'đa thức', 'polynomial'
    ]
    
    # Simple keyword scoring
    keyword_scores = {}
    for i, keyword in enumerate(math_keywords):
        count = text_lower.count(keyword)
        if count > 0:
            keyword_scores[i] = float(count)
    
    # Convert to sparse vector format (simple approach)
    # Note: Trong production, nên dùng SPLADE hoặc BM25
    return keyword_scores if keyword_scores else None

def create_collection():
    """Tạo collection với MULTI-VECTOR schema theo khuyến nghị Gemini"""
    
    collection_name = QDRANT_COLLECTION_NAME  # Sử dụng tên từ .env
    
    try:
        # Kiểm tra collection cũ (KHÔNG xóa tự động để tránh mất dữ liệu)
        try:
            existing = qdrant_client.get_collection(collection_name)
            print(f"⚠️ Collection {collection_name} đã tồn tại. Sẽ thêm dữ liệu vào collection hiện có.")
        except:
            print(f"📝 Tạo collection mới: {collection_name}")
        
        # Tạo collection với MULTI-VECTOR configuration (chỉ khi chưa tồn tại)
        try:
            qdrant_client.get_collection(collection_name)
            print(f"✅ Collection {collection_name} đã tồn tại, bỏ qua tạo mới")
        except:
            qdrant_client.create_collection(
                collection_name=collection_name,
                vectors_config={
                    # Vector dày cho semantic search
                    "semantic_vector": models.VectorParams(
                        size=VECTOR_SIZE,  # 1536 for text-embedding-3-small
                        distance=models.Distance.COSINE
                    ),
                    # Vector thưa cho keyword matching (sẽ implement sau)
                    # "keyword_vector": models.SparseVectorParams()
                }
            )
            print(f"✅ Đã tạo collection mới: {collection_name}")
        
        # Tạo RICH PAYLOAD INDEXES theo Gemini Table 2.1.1 + problem_section
        payload_indexes = [
            # Core identifiers
            ("doc_id", models.PayloadSchemaType.KEYWORD),
            ("source_file", models.PayloadSchemaType.KEYWORD),
            
            # Filtering fields
            ("category", models.PayloadSchemaType.KEYWORD),
            ("subcategory", models.PayloadSchemaType.KEYWORD),
            ("metadata.year", models.PayloadSchemaType.INTEGER),
            ("metadata.difficulty", models.PayloadSchemaType.KEYWORD),
            ("metadata.subject", models.PayloadSchemaType.KEYWORD),
            
            # Question filtering (NEW)
            ("question_number", models.PayloadSchemaType.KEYWORD),
            ("problem_section", models.PayloadSchemaType.KEYWORD),
            
            # Full-text search fields
            ("latex_string", models.PayloadSchemaType.TEXT),
            ("natural_language_desc", models.PayloadSchemaType.TEXT),
        ]
        
        for field_name, field_type in payload_indexes:
            try:
                qdrant_client.create_payload_index(
                    collection_name=collection_name,
                    field_name=field_name,
                    field_schema=field_type
                )
                print(f"   ✅ Created index: {field_name} ({field_type})")
            except Exception as e:
                print(f"   ⚠️ Index {field_name}: {e}")
        
        print(f"✅ Đã tạo collection: {collection_name}")
        print("✅ Đã tạo indexes cho filtering")
        
    except Exception as e:
        print(f"❌ Lỗi tạo collection {collection_name}: {e}")
        return False
    
    return True

def extract_problem_section(question_number: str, category: str) -> str:
    """Extract problem section from question_number based on category."""
    if not question_number:
        return ""
    
    if category == "dethi":
        # For dethi: section = question_number (e.g., "1" -> "1")
        return question_number.strip()
    elif category == "baitap":
        # For baitap: section = part before dot (e.g., "1.2" -> "1")
        if "." in question_number:
            return question_number.split(".")[0].strip()
        else:
            return question_number.strip()
    else:
        return question_number.strip()


def upload_item_to_qdrant(item):
    """Upload item với MULTI-VECTOR schema và RICH PAYLOAD + problem_section"""
    
    try:
        # === TẠO SEMANTIC VECTOR ===
        embedding_text = create_enhanced_embedding_text(item)
        semantic_vector = get_embedding(embedding_text)
        
        if semantic_vector is None:
            return False
        
        # === DỊCH TOÀN BỘ NỘI DUNG ===
        context = f"{item['metadata']['category_name']} - {item['category']}"
        
        # Dịch đề bài
        problem_natural = translate_latex_to_natural(item['problem_statement'], context)
        
        # Dịch problem parts
        problem_parts_natural = {}
        for part_key, part_content in item["problem_parts"].items():
            problem_parts_natural[part_key] = translate_latex_to_natural(part_content, context)
        
        # Dịch lời giải
        solution_natural = {}
        if item.get('solution', {}).get('full_solution'):
            solution_natural['full_solution'] = translate_latex_to_natural(
                item['solution']['full_solution'], context
            )
        
        # Dịch solution parts
        solution_parts_natural = {}
        for part_key, part_content in item.get('solution', {}).get('solution_parts', {}).items():
            solution_parts_natural[part_key] = translate_latex_to_natural(part_content, context)
        
        if solution_parts_natural:
            solution_natural['solution_parts'] = solution_parts_natural
        
        # === THÊM PROBLEM_SECTION ===
        question_number = item.get("question_number", "")
        category = item.get("category", "")
        problem_section = extract_problem_section(question_number, category)
        
        # === TẠO RICH PAYLOAD theo Gemini Table 2.1.1 + problem_section ===
        payload = {
            # Core identifiers (theo Gemini schema)
            "doc_id": item["id"],
            "source_file": item["metadata"]["source_file"],
            
            # Filtering fields
            "category": item["category"],
            "subcategory": item["subcategory"],
            "metadata": item["metadata"],  # Giữ nguyên để backward compatibility
            
            # LaTeX content (cho full-text search)
            "latex_string": item["problem_statement"],
            "natural_language_desc": problem_natural,
            
            # Complete content (giữ nguyên structure cũ)
            "title": item["title"],
            "question_number": item["question_number"],
            "source_path": item["source_path"],
            "problem_statement": item["problem_statement"],
            "problem_parts": item["problem_parts"],
            "solution": item["solution"],
            
            # Enhanced natural language content
            "problem_statement_natural": problem_natural,
            "problem_parts_natural": problem_parts_natural,
            "solution_natural": solution_natural,
            
            # NEW: Problem section for advanced filtering
            "problem_section": problem_section,
            
            # Search optimization
            "content_type": "hybrid_v3",  # Updated version
            "embedding_text": embedding_text  # Để debug và analysis
        }
        
        # === TẠO NUMERIC ID cho Qdrant Cloud ===
        numeric_id = create_numeric_id(item["id"])
        
        # === UPLOAD VÀO QDRANT với MULTI-VECTOR ===
        qdrant_client.upsert(
            collection_name=QDRANT_COLLECTION_NAME,  # Sử dụng collection name từ .env
            points=[{
                "id": numeric_id,  # Sử dụng numeric ID
                "vector": {
                    "semantic_vector": semantic_vector
                    # "keyword_vector": keyword_vector  # Sẽ implement sau
                },
                "payload": payload
            }]
        )
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi upload item {item['id']}: {e}")
        return False

def load_and_upload_data():
    """Load và upload tất cả dữ liệu JSON"""
    
    # Tìm tất cả file JSON
    json_pattern = "data/processed/final/**/*.json"
    json_files = glob.glob(json_pattern, recursive=True)
    
    # Loại bỏ file summary
    json_files = [f for f in json_files if "processing_summary.json" not in f]
    
    print(f"📁 Tìm thấy {len(json_files)} file JSON")
    
    total_items = 0
    success_count = 0
    
    for json_file in tqdm(json_files, desc="Xử lý files"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"\n📄 Xử lý file: {json_file}")
            print(f"   📊 Số items: {len(data)}")
            
            for item in tqdm(data, desc="Upload items", leave=False):
                total_items += 1
                if upload_item_to_qdrant(item):
                    success_count += 1
                else:
                    print(f"❌ Lỗi upload: {item['id']}")
                
                # Delay nhỏ để tránh rate limit
                time.sleep(0.1)
                
        except Exception as e:
            print(f"❌ Lỗi xử lý file {json_file}: {e}")
    
    print(f"\n🎉 HOÀN THÀNH!")
    print(f"📊 Tổng items: {total_items}")
    print(f"✅ Upload thành công: {success_count}")
    print(f"❌ Lỗi: {total_items - success_count}")
    
    return success_count

def test_search_functionality():
    """Test chức năng tìm kiếm với filter"""
    
    print("\n🧪 TEST SEARCH FUNCTIONALITY")
    
    test_queries = [
        {
            "query": "đề thi bảng A năm 2024",
            "expected_filters": {
                "category": "dethi",
                "subcategory": "bangA", 
                "year": 2024
            }
        },
        {
            "query": "bài tập ma trận năm 2018",
            "expected_filters": {
                "category": "baitap",
                "subcategory": "mt",
                "year": 2018
            }
        }
    ]
    
    for test in test_queries:
        print(f"\n🔍 Query: {test['query']}")
        
        # Tạo filter conditions
        must_conditions = []
        for key, value in test['expected_filters'].items():
            if key == "year":
                must_conditions.append({
                    "key": "metadata.year",
                    "match": {"value": value}
                })
            else:
                must_conditions.append({
                    "key": key,
                    "match": {"value": value}
                })
        
        query_filter = {"must": must_conditions} if must_conditions else None
        
        try:
            # Tìm kiếm với filter trên MULTI-VECTOR collection
            query_vector = get_embedding(test['query'])
            results = qdrant_client.search(
                collection_name=QDRANT_COLLECTION_NAME,
                query_vector=("semantic_vector", query_vector),  # Chỉ định vector name
                query_filter=query_filter,
                limit=5,
                with_vectors=False  # Không cần trả về vectors để tiết kiệm bandwidth
            )
            
            print(f"   📊 Kết quả: {len(results)} items")
            for i, result in enumerate(results[:3]):
                payload = result.payload
                print(f"   {i+1}. {payload['title']} (Score: {result.score:.3f})")
                print(f"      Category: {payload['category']}/{payload['subcategory']}")
                print(f"      Year: {payload['metadata']['year']}")
                
        except Exception as e:
            print(f"   ❌ Lỗi search: {e}")

def load_and_upload_data():
    """Load và upload tất cả dữ liệu JSON"""
    
    # Tìm tất cả file JSON
    json_files = glob.glob("data/processed/final/**/*.json", recursive=True)
    json_files = [f for f in json_files if "processing_summary.json" not in f]
    
    print(f"📁 Tìm thấy {len(json_files)} files")
    
    total_success = 0
    total_items = 0
    
    for json_file in json_files:
        print(f"\n📄 Xử lý: {json_file}")
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                items = json.load(f)
            
            print(f"   📊 {len(items)} items")
            total_items += len(items)
            
            # Upload từng item
            for item in items:
                if upload_item_to_qdrant(item):
                    total_success += 1
                    print(f"   ✅ {total_success}/{total_items} uploaded", end='\r')
                else:
                    print(f"   ❌ Lỗi upload item {item.get('id', 'unknown')}")
                
                # Rate limiting để tránh quá tải
                time.sleep(0.1)
                
        except Exception as e:
            print(f"❌ Lỗi xử lý file {json_file}: {e}")
    
    print(f"\n📊 Tổng kết: {total_success}/{total_items} items uploaded thành công")
    return total_success

def main():
    """Hàm main"""
    
    print("🚀 BẮT ĐẦU IMPORT DỮ LIỆU VÀO QDRANT CLOUD")
    print("=" * 50)
    
    # Kiểm tra cấu hình
    if not all([OPENAI_API_KEY, QDRANT_URL, QDRANT_API_KEY]):
        print("❌ Thiếu cấu hình environment variables!")
        return
    
    print(f"🔗 QDRANT_URL: {QDRANT_URL}")
    print(f"📦 COLLECTION: {QDRANT_COLLECTION_NAME}")
    
    # Tạo collection
    if not create_collection():
        return
    
    # Upload dữ liệu
    success_count = load_and_upload_data()
    
    if success_count > 0:
        # Test search
        test_search_functionality()
        
        print(f"\n🎉 THÀNH CÔNG! Đã upload {success_count} items vào Qdrant Cloud")
    else:
        print("\n❌ THẤT BẠI! Không upload được item nào")

if __name__ == "__main__":
    main()

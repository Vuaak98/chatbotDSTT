"""
Vietnamese query parser for RAG filters.
- Extracts: category (baitap/dethi), subcategory (mt/dt/gtr/hpt/kgvt/tohop), year (int)
- Normalizes query (Unicode NFC, lowercase, trim)
- No external deps; safe to import.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict
import re
import unicodedata


CATEGORY_KEYWORDS = {
    "baitap": ["bài tập", "baitap", "bt"],
    "dethi": ["đề thi", "dethi", "đề", "de thi"],
}

SUBCATEGORY_KEYWORDS = {
    "mt": ["ma trận", "ma-trận", "matrix", "mt"],
    "dt": ["định thức", "dinh thuc", "det", "dt"],
    "gtr": ["giá trị riêng", "gia tri rieng", "eigenvalue", "gtr"],
    "hpt": ["hệ phương trình", "he phuong trinh", "system", "hpt"],
    "kgvt": ["không gian vector", "khong gian vector", "vector space", "kgvt"],
    "tohop": ["tổ hợp", "to hop", "combination", "tohop"],
    # Exam boards for dethi
    "bangA": ["bảng a", "bang a", "banga", "board a"],
    "bangB": ["bảng b", "bang b", "bangb", "board b"],
}

YEAR_PATTERN = re.compile(r"\b(201[0-9]|202[0-9])\b")
QUESTION_CODE_PATTERN = re.compile(r"\bbài\s+(\d+\.\d+)\b", re.IGNORECASE)
QUESTION_NUM_PATTERN = re.compile(r"\bbài\s+(\d+)\b", re.IGNORECASE)


@dataclass
class ParsedQuery:
    normalized_query: str
    category: Optional[str] = None
    subcategory: Optional[str] = None
    year: Optional[int] = None
    question_code: Optional[str] = None  # "1.2", "3.1", etc.
    question_num: Optional[str] = None   # "1", "2", "3" (for section filtering)


def normalize_text(s: str) -> str:
    s = unicodedata.normalize("NFC", s)
    s = s.strip().lower()
    return s


def extract_year(text: str) -> Optional[int]:
    m = YEAR_PATTERN.search(text)
    if m:
        try:
            return int(m.group(1))
        except Exception:
            return None
    return None


def extract_question_info(text: str) -> tuple[Optional[str], Optional[str]]:
    """Extract question_code (e.g., '1.2') and question_num (e.g., '1') from text.
    Returns (question_code, question_num).
    """
    # First try to match "Bài N.M" (more specific)
    code_match = QUESTION_CODE_PATTERN.search(text)
    if code_match:
        question_code = code_match.group(1)
        question_num = question_code.split('.')[0]  # Extract section number
        return question_code, question_num
    
    # Then try to match "Bài N" (less specific)
    num_match = QUESTION_NUM_PATTERN.search(text)
    if num_match:
        question_num = num_match.group(1)
        return None, question_num  # No specific code, just section
    
    return None, None


def match_keyword(text: str, mapping: Dict[str, list[str]]) -> Optional[str]:
    for key, variants in mapping.items():
        for v in variants:
            if v in text:
                return key
    return None


def parse_query(query: str) -> ParsedQuery:
    nq = normalize_text(query or "")
    year = extract_year(nq)
    category = match_keyword(nq, CATEGORY_KEYWORDS)
    subcat = match_keyword(nq, SUBCATEGORY_KEYWORDS)
    question_code, question_num = extract_question_info(nq)

    # If exam board detected, force category to dethi and normalize subcategory
    if subcat in ("bangA", "bangB"):
        category = "dethi"
        # Keep subcategory as-is (bangA/bangB)

    return ParsedQuery(
        normalized_query=nq, 
        category=category, 
        subcategory=subcat, 
        year=year,
        question_code=question_code,
        question_num=question_num
    )


# Helper to build Qdrant filter dict compatible with client.query_points
# Uses payload keys from your import: category, subcategory, metadata.year

def build_qdrant_filter(category: Optional[str], subcategory: Optional[str], year: Optional[int]):
    must = []
    if category:
        must.append({"key": "category", "match": {"value": category}})
    if subcategory:
        must.append({"key": "subcategory", "match": {"value": subcategory}})
    if year is not None:
        must.append({"key": "metadata.year", "match": {"value": year}})
    return {"must": must} if must else None


#!/usr/bin/env python3
"""
Full Pipeline Test - Mô phỏng chính xác luồng backend + frontend
Bao gồm: RAG Service + Prompt Templates + OpenAI Integration

Sử dụng để test xem response có giống với web interface không.
"""

import asyncio
import logging
import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import các module cần thiết với absolute import
from app.rag.rag_service import RAGService
from app.rag.prompts.templates import LinearAlgebraTemplates
from app.rag.query_extractor_vn import parse_query
from app.services.llm.openai_service import OpenAIService
from app.config import get_settings

class FullPipelineTest:
    """Test toàn diện mô phỏng luồng thực tế"""
    
    def __init__(self):
        """Khởi tạo các service giống như trong production"""
        self.settings = get_settings()
        self.rag_service = RAGService()
        self.templates = LinearAlgebraTemplates()
        
        # Khởi tạo OpenAI service nếu có API key
        if self.settings.openai_api_key:
            self.openai_service = OpenAIService(
                api_key=self.settings.openai_api_key,
                model_name=self.settings.openai_model_name
            )
        else:
            logger.warning("No OpenAI API key - will only test RAG pipeline")
            self.openai_service = None
    
    async def test_query(self, query: str, include_llm: bool = False) -> dict:
        """
        Test một query hoàn chỉnh qua toàn bộ pipeline
        
        Args:
            query: Câu hỏi test
            include_llm: Có gọi LLM thực tế không (tốn tiền)
            
        Returns:
            Dict chứa kết quả từng bước
        """
        result = {
            "query": query,
            "vn_parser": None,
            "rag_documents": None,
            "rag_success": False,
            "system_prompt": None,
            "enhanced_prompt": None,
            "llm_response": None,
            "errors": []
        }
        
        try:
            # Bước 1: Parse query với VN parser
            logger.info(f"🔍 TESTING QUERY: '{query}'")
            parsed = parse_query(query)
            result["vn_parser"] = {
                "category": parsed.category,
                "subcategory": parsed.subcategory,
                "year": parsed.year,
                "question_code": parsed.question_code,
                "question_num": parsed.question_num
            }
            logger.info(f"📝 VN Parser: {result['vn_parser']}")
            
            # Bước 2: RAG retrieval
            logger.info("🔍 Starting RAG retrieval...")
            documents, success = await self.rag_service.get_context(
                query, 
                k=3,
                use_query_metadata=True
            )
            
            result["rag_success"] = success
            if success and documents:
                result["rag_documents"] = []
                for i, doc in enumerate(documents):
                    doc_info = {
                        "index": i + 1,
                        "metadata": getattr(doc, "metadata", {}),
                        "content_preview": getattr(doc, "page_content", "")[:200] + "..."
                    }
                    result["rag_documents"].append(doc_info)
                    
                logger.info(f"✅ RAG Success: {len(documents)} documents found")
                for i, doc in enumerate(documents[:2]):
                    if hasattr(doc, "metadata"):
                        meta_str = ", ".join([f"{k}={v}" for k, v in doc.metadata.items() 
                                            if k in ["title", "category", "subcategory", "question_number", "year"]])
                        logger.info(f"  📄 Doc {i+1}: {meta_str}")
                
                # Bước 3: Tạo prompts giống như production
                logger.info("📝 Creating prompts...")
                system_prompt = self.templates.get_system_prompt(rag_enabled=True)
                enhanced_prompt = self.templates.get_enhanced_prompt(
                    user_question=query,
                    documents=documents
                )
                
                result["system_prompt"] = f"System prompt length: {len(system_prompt)} chars"
                result["enhanced_prompt"] = f"Enhanced prompt length: {len(enhanced_prompt)} chars"
                
                # Log một phần prompt để debug
                logger.info(f"📝 System prompt: {len(system_prompt)} chars")
                logger.info(f"📝 Enhanced prompt: {len(enhanced_prompt)} chars")
                
                # Bước 4: LLM call (optional)
                if include_llm and self.openai_service:
                    logger.info("🤖 Calling OpenAI...")
                    try:
                        response = self.openai_service.generate(
                            system_message=system_prompt,
                            user_message=enhanced_prompt
                        )
                        result["llm_response"] = response[:500] + "..." if len(response) > 500 else response
                        logger.info(f"🤖 LLM Response: {len(response)} chars")
                    except Exception as e:
                        error_msg = f"LLM Error: {str(e)}"
                        result["errors"].append(error_msg)
                        logger.error(error_msg)
                        
            else:
                logger.warning("❌ RAG Failed: No documents found")
                result["errors"].append("RAG retrieval failed")
                
                # Fallback prompt
                system_prompt = self.templates.get_system_prompt(rag_enabled=False)
                result["system_prompt"] = f"Fallback system prompt: {len(system_prompt)} chars"
                result["enhanced_prompt"] = f"Original query: {query}"
                
        except Exception as e:
            error_msg = f"Pipeline Error: {str(e)}"
            result["errors"].append(error_msg)
            logger.error(error_msg, exc_info=True)
            
        return result
    
    def print_result(self, result: dict):
        """In kết quả test một cách đẹp mắt"""
        print("\n" + "="*80)
        print(f"🔍 QUERY: {result['query']}")
        print("="*80)
        
        # VN Parser
        if result["vn_parser"]:
            print("📝 VN PARSER:")
            for key, value in result["vn_parser"].items():
                if value:
                    print(f"  {key}: {value}")
        
        # RAG Results
        print(f"\n🔍 RAG: {'✅ SUCCESS' if result['rag_success'] else '❌ FAILED'}")
        if result["rag_documents"]:
            print(f"  Found {len(result['rag_documents'])} documents:")
            for doc in result["rag_documents"][:2]:  # Show first 2
                meta = doc["metadata"]
                title = meta.get("title", "No title")
                category = meta.get("category", "")
                subcategory = meta.get("subcategory", "")
                question_num = meta.get("question_number", "")
                year = meta.get("year", "")
                print(f"    📄 {title} | {category}/{subcategory} | #{question_num} | {year}")
        
        # Prompts
        if result["system_prompt"]:
            print(f"\n📝 PROMPTS:")
            print(f"  System: {result['system_prompt']}")
            print(f"  Enhanced: {result['enhanced_prompt']}")
        
        # LLM Response
        if result["llm_response"]:
            print(f"\n🤖 LLM RESPONSE:")
            print(f"  {result['llm_response']}")
        
        # Errors
        if result["errors"]:
            print(f"\n❌ ERRORS:")
            for error in result["errors"]:
                print(f"  {error}")
        
        print("\n" + "="*80)

async def main():
    """Test các query quan trọng"""
    tester = FullPipelineTest()
    
    # Test cases giống như trên web interface
    test_queries = [
        "đề thi bảng B 2024",
        "bài 1.1 ma trận 2018", 
        "đề thi bảng A 2024",
        "bài 1 ma trận 2018",
        "ma trận nghịch đảo",
        "định thức ma trận"
    ]
    
    print("🚀 FULL PIPELINE TEST - Mô phỏng Backend + Frontend")
    print("="*80)
    
    for query in test_queries:
        result = await tester.test_query(query, include_llm=False)  # Set True để test LLM
        tester.print_result(result)
        
        # Pause between tests
        await asyncio.sleep(1)
    
    print("\n✅ Test completed!")
    print("\n💡 Để test với LLM thực tế, set include_llm=True trong test_query()")

if __name__ == "__main__":
    asyncio.run(main())

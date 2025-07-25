import argparse
import asyncio
import logging
import os
import sys
from pathlib import Path
from typing import List, Optional

# Thêm parent directory vào Python path
parent_dir = str(Path(__file__).parent.parent.absolute())
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from app.rag.config.config import rag_settings
from app.rag.qdrant_connector import QdrantConnector
from data_ingestion.pipelines.text_loader import TextLoader

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(os.path.dirname(__file__), "ingestion.log"))
    ]
)
logger = logging.getLogger(__name__)


async def ingest_directory(
    directory: str,
    recursive: bool = True,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    use_semantic_chunking: bool = True,
    collection_name: Optional[str] = None,
    clear_collection: bool = False
) -> None:
    """
    Nhập dữ liệu từ thư mục vào Qdrant
    
    Args:
        directory: Đường dẫn đến thư mục chứa dữ liệu
        recursive: Có đọc các thư mục con hay không
        chunk_size: Kích thước chunk cho việc chia nhỏ văn bản
        chunk_overlap: Độ chồng lấp giữa các chunks
        use_semantic_chunking: Sử dụng semantic chunking thay vì chunking thông thường
        collection_name: Tên collection (mặc định lấy từ cấu hình)
        clear_collection: Xóa collection cũ nếu đã tồn tại
    """
    try:
        # Khởi tạo QdrantConnector
        if collection_name:
            qdrant = QdrantConnector(collection_name=collection_name)
        else:
            qdrant = QdrantConnector()
            collection_name = rag_settings.qdrant_collection_name
            
        # Xóa collection nếu được yêu cầu
        if clear_collection:
            logger.info(f"Xóa collection {collection_name} nếu tồn tại")
            try:
                qdrant.client.delete_collection(collection_name=collection_name)
                logger.info(f"Đã xóa collection {collection_name}")
                
                # Tạo lại connector sau khi xóa collection
                qdrant = QdrantConnector(collection_name=collection_name)
            except Exception as e:
                logger.warning(f"Không thể xóa collection: {e}")
                
        # Khởi tạo TextLoader
        loader = TextLoader(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        
        # Đọc tất cả documents từ thư mục
        logger.info(f"Đang đọc dữ liệu từ thư mục {directory}")
        raw_documents = TextLoader.load_directory(
            directory_path=directory,
            recursive=recursive,
            collection=collection_name,
            category="linear_algebra"
        )
        
        logger.info(f"Đã đọc {len(raw_documents)} documents")
        
        # Xử lý documents
        if use_semantic_chunking:
            # Sử dụng semantic chunking cho từng document
            documents = []
            for doc in raw_documents:
                chunks = TextLoader.semantic_chunking(
                    text=doc.page_content,
                    metadata=doc.metadata
                )
                documents.extend(chunks)
            logger.info(f"Đã tạo {len(documents)} chunks với semantic chunking")
        else:
            # Sử dụng chunking thông thường
            documents = loader.split_documents(raw_documents)
            logger.info(f"Đã tạo {len(documents)} chunks với regular chunking")
            
        # Lưu vào Qdrant
        if documents:
            logger.info(f"Đang lưu {len(documents)} documents vào Qdrant collection {collection_name}")
            try:
                ids = await qdrant.add_documents(documents)
                logger.info(f"Đã lưu thành công {len(ids)} documents vào Qdrant")
            except Exception as e:
                logger.error(f"Lỗi khi lưu documents vào Qdrant: {e}")
        else:
            logger.warning("Không có documents nào để lưu")
            
    except Exception as e:
        logger.exception(f"Lỗi trong quá trình nhập dữ liệu: {e}")


async def test_search(query: str, collection_name: Optional[str] = None, top_k: int = 3) -> None:
    """
    Test tìm kiếm trong Qdrant
    
    Args:
        query: Câu truy vấn
        collection_name: Tên collection (mặc định lấy từ cấu hình)
        top_k: Số lượng kết quả trả về
    """
    try:
        # Khởi tạo QdrantConnector
        if collection_name:
            qdrant = QdrantConnector(collection_name=collection_name)
        else:
            qdrant = QdrantConnector()
            collection_name = rag_settings.qdrant_collection_name
            
        logger.info(f"Test tìm kiếm với query: '{query}'")
        results = await qdrant.similarity_search(query=query, k=top_k)
        
        logger.info(f"Kết quả ({len(results)} documents):")
        for i, doc in enumerate(results):
            logger.info(f"Kết quả #{i+1}:")
            logger.info(f"- Source: {doc.metadata.get('source', 'Unknown')}")
            logger.info(f"- Type: {doc.metadata.get('type', 'Unknown')}")
            logger.info(f"- Content: {doc.page_content[:200]}...")
            logger.info("---")
            
    except Exception as e:
        logger.exception(f"Lỗi trong quá trình test tìm kiếm: {e}")


def parse_args():
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser(description="Data Ingestion Tool")
    
    # Command
    parser.add_argument(
        "--command",
        type=str,
        choices=["ingest", "test_search"],
        default="ingest",
        help="Command to execute (default: ingest)"
    )
    
    # Ingestion arguments
    parser.add_argument(
        "--directory",
        type=str,
        default=rag_settings.data_dir,
        help=f"Directory containing data files (default: {rag_settings.data_dir})"
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        default=True,
        help="Process subdirectories recursively (default: True)"
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=1000,
        help="Chunk size for text splitting (default: 1000)"
    )
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=200,
        help="Chunk overlap for text splitting (default: 200)"
    )
    parser.add_argument(
        "--semantic-chunking",
        action="store_true",
        default=True,
        help="Use semantic chunking instead of regular chunking (default: True)"
    )
    parser.add_argument(
        "--collection-name",
        type=str,
        default=None,
        help=f"Qdrant collection name (default: {rag_settings.qdrant_collection_name})"
    )
    parser.add_argument(
        "--clear-collection",
        action="store_true",
        default=False,
        help="Clear existing collection before ingestion (default: False)"
    )
    
    # Test search arguments
    parser.add_argument(
        "--query",
        type=str,
        default="Ma trận vuông bậc 3 có những tính chất nào?",
        help="Query for testing search"
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=3,
        help="Number of results to return (default: 3)"
    )
    
    return parser.parse_args()


async def main():
    """
    Main function
    """
    args = parse_args()
    
    if args.command == "ingest":
        logger.info("Bắt đầu quá trình nhập dữ liệu")
        await ingest_directory(
            directory=args.directory,
            recursive=args.recursive,
            chunk_size=args.chunk_size,
            chunk_overlap=args.chunk_overlap,
            use_semantic_chunking=args.semantic_chunking,
            collection_name=args.collection_name,
            clear_collection=args.clear_collection
        )
        logger.info("Hoàn thành quá trình nhập dữ liệu")
        
    elif args.command == "test_search":
        logger.info("Bắt đầu test tìm kiếm")
        await test_search(
            query=args.query,
            collection_name=args.collection_name,
            top_k=args.top_k
        )
        logger.info("Hoàn thành test tìm kiếm")


if __name__ == "__main__":
    asyncio.run(main()) 
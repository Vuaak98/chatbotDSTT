import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Union

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextLoader:
    """
    Lớp để đọc và xử lý văn bản cho RAG
    """
    
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        separators: Optional[List[str]] = None
    ):
        """
        Khởi tạo TextLoader
        
        Args:
            chunk_size: Kích thước chunk cho việc chia nhỏ văn bản
            chunk_overlap: Độ chồng lấp giữa các chunks
            separators: Danh sách các separators cho việc chia nhỏ văn bản
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Sử dụng các separators mặc định nếu không có
        if separators is None:
            separators = ["\n\n", "\n", ". ", " ", ""]
        self.separators = separators
        
        # Khởi tạo text splitter
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=self.separators,
        )
    
    def load_document_from_file(self, file_path: Union[str, Path], **metadata) -> List[Document]:
        """
        Đọc văn bản từ file và tạo Document object
        
        Args:
            file_path: Đường dẫn đến file
            **metadata: Metadata tùy chọn cho document
            
        Returns:
            Document object
        """
        file_path = Path(file_path)
        
        # Kiểm tra file tồn tại
        if not file_path.exists():
            raise FileNotFoundError(f"File {file_path} không tồn tại")
        
        # Thêm metadata cơ bản
        base_metadata = {
            "source": str(file_path),
            "filename": file_path.name,
            "filetype": file_path.suffix.lower(),
        }
        
        # Gộp với metadata tùy chọn
        doc_metadata = {**base_metadata, **metadata}
        
        # Đọc nội dung file
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            # Thử lại với encoding khác nếu utf-8 không hoạt động
            with open(file_path, "r", encoding="latin-1") as f:
                content = f.read()
        
        # Tạo Document
        document = Document(
            page_content=content,
            metadata=doc_metadata,
        )
        
        return [document]
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Chia nhỏ documents thành chunks
        
        Args:
            documents: Danh sách Document objects
            
        Returns:
            Danh sách Document objects đã được chia nhỏ
        """
        # Chia nhỏ từng document
        all_splits = []
        for doc in documents:
            splits = self.splitter.split_documents([doc])
            
            # Đảm bảo metadata được giữ nguyên
            for split in splits:
                if "chunk_id" not in split.metadata:
                    split.metadata["chunk_id"] = f"{doc.metadata.get('filename', 'unknown')}_chunk_{len(all_splits) + len(splits)}"
            
            all_splits.extend(splits)
        
        return all_splits
    
    @staticmethod
    def semantic_chunking(text: str, metadata: Dict = None) -> List[Document]:
        """
        Chia văn bản theo ngữ nghĩa (Semantic Chunking) - phù hợp với đại số tuyến tính
        
        Args:
            text: Văn bản cần chia
            metadata: Metadata cơ bản cho documents
            
        Returns:
            Danh sách Document objects
        """
        metadata = metadata or {}
        documents = []
        
        # Các pattern phổ biến trong tài liệu toán học
        patterns = [
            # Định lý, định nghĩa
            r"(Định lý|Theorem|Định nghĩa|Definition)[:\s]+([^.]*\.(?:[^.]*\.[^.]*\.)*)",
            # Ví dụ
            r"(Ví dụ|Example)[:\s]+([^.]*\.(?:[^.]*\.[^.]*\.)*)",
            # Bài tập
            r"(Bài tập|Bài toán|Exercise|Problem)[:\s]+([^.]*\.(?:[^.]*\.[^.]*\.)*)",
            # Chứng minh
            r"(Chứng minh|Proof)[:\s]+([^.]*\.(?:[^.]*\.[^.]*\.)*)",
        ]
        
        # Vị trí cuối cùng đã xử lý
        last_end = 0
        
        for pattern in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE | re.DOTALL):
                start, end = match.span()
                if start >= last_end:  # Tránh chồng lấp
                    # Thêm phần trước đó nếu có
                    if start > last_end:
                        prev_chunk = text[last_end:start].strip()
                        if prev_chunk:
                            chunk_metadata = metadata.copy()
                            chunk_metadata["type"] = "text"
                            documents.append(Document(page_content=prev_chunk, metadata=chunk_metadata))
                    
                    # Thêm phần match với loại phù hợp
                    chunk = match.group(0).strip()
                    if chunk:
                        chunk_metadata = metadata.copy()
                        chunk_type = match.group(1).lower()
                        
                        if "định lý" in chunk_type or "theorem" in chunk_type:
                            chunk_metadata["type"] = "theorem"
                        elif "định nghĩa" in chunk_type or "definition" in chunk_type:
                            chunk_metadata["type"] = "definition"
                        elif "ví dụ" in chunk_type or "example" in chunk_type:
                            chunk_metadata["type"] = "example"
                        elif "bài tập" in chunk_type or "bài toán" in chunk_type or "exercise" in chunk_type or "problem" in chunk_type:
                            chunk_metadata["type"] = "problem"
                        elif "chứng minh" in chunk_type or "proof" in chunk_type:
                            chunk_metadata["type"] = "proof"
                        else:
                            chunk_metadata["type"] = "unknown"
                            
                        documents.append(Document(page_content=chunk, metadata=chunk_metadata))
                    
                    last_end = end
        
        # Thêm phần còn lại
        if last_end < len(text):
            remaining = text[last_end:].strip()
            if remaining:
                chunk_metadata = metadata.copy()
                chunk_metadata["type"] = "text"
                documents.append(Document(page_content=remaining, metadata=chunk_metadata))
        
        return documents
    
    @classmethod
    def load_directory(cls, directory_path: Union[str, Path], recursive: bool = True, **metadata) -> List[Document]:
        """
        Đọc tất cả files trong một thư mục
        
        Args:
            directory_path: Đường dẫn đến thư mục
            recursive: Có đọc các thư mục con hay không
            **metadata: Metadata tùy chọn cho documents
            
        Returns:
            Danh sách Document objects
        """
        directory_path = Path(directory_path)
        
        if not directory_path.exists() or not directory_path.is_dir():
            raise ValueError(f"{directory_path} không phải là thư mục hợp lệ")
        
        documents = []
        loader = cls()
        
        # Hàm đệ quy để duyệt thư mục
        def process_directory(dir_path: Path, base_metadata: Dict):
            nonlocal documents
            
            for item in dir_path.iterdir():
                # Bỏ qua các file ẩn
                if item.name.startswith('.'):
                    continue
                    
                if item.is_file() and item.suffix.lower() in ['.txt', '.md']:
                    # Đọc file
                    try:
                        item_metadata = base_metadata.copy()
                        item_metadata["directory"] = str(item.parent.relative_to(directory_path))
                        docs = loader.load_document_from_file(item, **item_metadata)
                        documents.extend(docs)
                    except Exception as e:
                        print(f"Lỗi khi đọc file {item}: {e}")
                        
                elif item.is_dir() and recursive:
                    # Đọc thư mục con nếu recursive=True
                    dir_metadata = base_metadata.copy()
                    dir_metadata["parent_dir"] = str(item.parent.relative_to(directory_path))
                    process_directory(item, dir_metadata)
        
        # Bắt đầu duyệt từ thư mục gốc
        process_directory(directory_path, metadata)
        
        return documents 
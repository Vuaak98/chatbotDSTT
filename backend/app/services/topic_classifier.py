import logging
import re
from typing import Dict, Tuple

logger = logging.getLogger(__name__)

# Từ khóa liên quan đến đại số tuyến tính (Tiếng Việt)
LINEAR_ALGEBRA_KEYWORDS_VI = [
    # Chủ đề chính
    r"đại số tuyến tính", r"đstt", r"đại số tt",
    
    # Không gian vector
    r"không gian vect[oơ]", r"vector", r"vect[oơ] cơ sở", r"vect[oơ] đơn vị",
    r"không gian con", r"độc lập tuyến tính", r"phụ thuộc tuyến tính",
    r"tọa độ", r"hạng",
    
    # Ma trận
    r"ma trận", r"định thức", r"đường chéo[hóa]*", r"tam giác[hóa]*", r"nghịch đảo", 
    r"chéo hóa", r"đồng dạng", r"tương tự", r"trực giao", r"trực chuẩn",
    r"khả nghịch", r"đối xứng",
    
    # Ánh xạ tuyến tính
    r"ánh xạ tuyến tính", r"phép biến đổi tuyến tính", r"toán tử tuyến tính",
    r"nhân", r"phép chiếu", r"kernel", r"hạt nhân", r"ảnh",
    
    # Trị riêng & vector riêng
    r"trị riêng", r"giá trị riêng", r"vect[oơ] riêng", r"không gian riêng", r"đa thức đặc trưng",
    r"phương trình đặc trưng",
    
    # Dạng toàn phương
    r"dạng toàn phương", r"dạng chính tắc", r"dạng chuẩn tắc", r"chỉ số quán tính",
    
    # Olympic
    r"olympic", r"thi học sinh giỏi", r"hsg", r"đội tuyển",
    
    # Từ khóa kỹ thuật
    r"hạng của ma trận", r"dấu của hoán vị", r"phần tử bội", r"phép khử gauss", 
    r"gauss-jordan", r"ma trận bậc thang", r"bậc thang rút gọn",
    r"ma trận đơn vị", r"ma trận không", r"ma trận chuyển vị", r"chuyển vị",
    r"tích vô hướng", r"không gian euclid", r"ma trận trực giao", r"trực giao",
    r"trực giao hóa gram-schmidt", r"trực giao hóa", r"chuẩn hóa",
]

# Từ khóa liên quan đến đại số tuyến tính (Tiếng Anh)
LINEAR_ALGEBRA_KEYWORDS_EN = [
    # Chủ đề chính
    r"linear algebra",
    
    # Không gian vector
    r"vector space", r"basis", r"span", r"linear independence", r"linear dependence",
    r"coordinates", r"rank", r"dimension", r"subspace", r"null space",
    
    # Ma trận
    r"matrix", r"matrices", r"determinant", r"diagonal", r"triangular",
    r"inverse", r"diagonalization", r"similar", r"orthogonal", r"orthonormal",
    r"invertible", r"symmetric",
    
    # Ánh xạ tuyến tính
    r"linear map", r"linear transformation", r"linear operator",
    r"multiplication", r"projection", r"kernel", r"image", r"range",
    
    # Trị riêng & vector riêng
    r"eigenvalue", r"eigenvector", r"eigenspace", r"characteristic polynomial",
    r"characteristic equation",
    
    # Dạng toàn phương
    r"quadratic form", r"canonical form", r"inertia index",
    
    # Từ khóa kỹ thuật
    r"matrix rank", r"permutation sign", r"multiplicity", r"gaussian elimination", 
    r"gauss-jordan", r"row echelon form", r"reduced row echelon form",
    r"identity matrix", r"zero matrix", r"transpose", r"inner product",
    r"euclidean space", r"orthogonal matrix", r"gram-schmidt orthogonalization", r"normalization",
]

# Kết hợp các từ khóa
LINEAR_ALGEBRA_KEYWORDS = LINEAR_ALGEBRA_KEYWORDS_VI + LINEAR_ALGEBRA_KEYWORDS_EN

# Các dạng bài cụ thể trong Olympic đại số tuyến tính
OLYMPIC_PATTERNS = [
    # Dạng bài phổ biến trong Olympic và HSG
    r"tìm ma trận \w+ sao cho",
    r"chứng minh .*ma trận",
    r"hạng của ma trận",
    r"tính định thức",
    r"giá trị (của|lớn nhất|nhỏ nhất).*định thức",
    r"ma trận.*khả nghịch",
    r"trị riêng",
    r"vect[oơ] riêng",
    r"chéo hóa",
    r"đường chéo hóa",
    r"trực giao hóa",
    r"cơ sở trực giao",
    r"không gian sinh bởi",
    r"không gian con.*bởi",
    r"dạng toàn phương.*chính tắc",
    r"dạng toàn phương.*chỉ số quán tính",
]


class TopicClassifier:
    """
    Phân loại chủ đề của câu hỏi
    """
    
    def __init__(self):
        """
        Khởi tạo classifier
        """
        # Compile regex patterns cho hiệu năng
        self.la_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in LINEAR_ALGEBRA_KEYWORDS]
        self.olympic_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in OLYMPIC_PATTERNS]
        
    def classify(self, text: str) -> Tuple[bool, Dict]:
        """
        Phân loại câu hỏi vào các chủ đề
        
        Args:
            text: Nội dung câu hỏi
            
        Returns:
            Tuple[bool, Dict]: (is_linear_algebra, metadata)
            - is_linear_algebra: True nếu là câu hỏi về đại số tuyến tính
            - metadata: Metadata về chủ đề, dạng bài, độ khó, v.v.
        """
        # Chuẩn hóa text
        normalized_text = text.lower()
        
        # Kiểm tra xem có phải đại số tuyến tính không
        is_linear_algebra = any(pattern.search(normalized_text) for pattern in self.la_patterns)
        
        # Kiểm tra dạng bài Olympic
        olympic_patterns_found = [
            pattern.pattern for pattern in self.olympic_patterns 
            if pattern.search(normalized_text)
        ]
        is_olympic = len(olympic_patterns_found) > 0
        
        # Nếu tìm thấy dạng bài Olympic, ưu tiên nhận biết là đại số tuyến tính
        if is_olympic:
            is_linear_algebra = True
            
        # Tạo metadata
        metadata = {
            "is_linear_algebra": is_linear_algebra,
            "is_olympic": is_olympic,
            "olympic_patterns": olympic_patterns_found if is_olympic else [],
            "confidence": "high" if is_olympic else ("medium" if is_linear_algebra else "low")
        }
        
        return is_linear_algebra, metadata
        

# Singleton instance
topic_classifier = TopicClassifier() 
"""
AI Math Chatbot Application Package
"""
import warnings
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Filter out specific Pydantic warnings
warnings.filterwarnings(
    "ignore", 
    message=".*<built-in function any> is not a Python type.*",
    category=UserWarning
)

# The orm_mode warning is already fixed with from_attributes=True in schemas.py 

# Early import of services và adapters để monkey patch
try:
    from . import services
    # Import adapters/services_adapter để nó thực hiện monkey patch
    from .adapters import services_adapter
    logger.info("ServicesAdapter được nạp thành công và đã thực hiện monkey patch services.generate_ai_response")
except ImportError as e:
    logger.warning(f"Lỗi khi nạp ServicesAdapter: {e}")
except Exception as e:
    logger.warning(f"Lỗi không xác định khi nạp ServicesAdapter: {e}") 
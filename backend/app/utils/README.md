# Utility Functions

This directory contains utility functions used throughout the AI Math Chatbot backend.

## Sanitization Utilities

The `sanitizer.py` module provides functions for sanitizing user input to prevent injection attacks and other security vulnerabilities.

### Functions

#### `sanitize_text(text: str) -> str`

Sanitizes text input to prevent injection attacks.

- HTML escapes the text to prevent XSS
- Normalizes newlines
- Removes control characters

#### `sanitize_filename(filename: str) -> str`

Sanitizes a filename to prevent path traversal attacks.

- Removes path components (/, \, :, etc.)
- Removes leading/trailing dots and spaces
- Ensures the filename is not empty after sanitization

#### `sanitize_dict(data: Dict[str, Any]) -> Dict[str, Any]`

Recursively sanitizes all string values in a dictionary.

#### `sanitize_list(data: List[Any]) -> List[Any]`

Recursively sanitizes all string values in a list.

#### `validate_mime_type(content_type: str, allowed_types: List[str]) -> bool`

Validates that a MIME type is in the list of allowed types.

- Normalizes the content type (lowercase, removes parameters)
- Checks if the normalized content type is in the allowed types

## Usage

These utility functions are used throughout the application to sanitize user input before processing or storing it. For example:

```python
from ..utils import sanitize_text, sanitize_filename

# Sanitize user input
sanitized_message = sanitize_text(message)

# Sanitize filename
sanitized_filename = sanitize_filename(file.filename)
```
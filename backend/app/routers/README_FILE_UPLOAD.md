# File Upload API Documentation

## Overview

The File Upload API endpoint allows the AI Math Chatbot to accept and process file uploads from users. Supported files include images, PDFs, text files, and Word documents, which can be used as part of a chat or question to the AI assistant. **You can upload up to 5 files at once per request.**

## Endpoint

```
POST /upload-file
```

## Request Format

The request should be a `multipart/form-data` request with one or more files attached (up to 5 files per request).

### Parameters

- `file`: The file to upload (required; multiple files supported by sending up to 5 `file` fields)

### Supported File Types

- **PDF:** `application/pdf`
- **Images:**
  - `image/jpeg`
  - `image/png`
  - `image/webp`
  - `image/heic`
  - `image/heif`
- **Text:** `text/plain`
- **Word:** `application/vnd.openxmlformats-officedocument.wordprocessingml.document` (.docx)

### Size Limits

- **Inline processing:** Files < ~20MB are processed in-memory and sent directly to Gemini
- **Large files:** Files up to 2GB are uploaded via Gemini Files API (48-hour TTL)
- **Server-side limit:** The maximum file size is 2GB, but can be configured with the `MAX_FILE_SIZE` environment variable
- **File count limit:** Maximum 5 files per request

## Response Format

### Success Response (200 OK)

```json
[
  {
    "file_id": "unique_file_id_1",
    "filename": "uploaded_filename1.pdf",
    "mime_type": "application/pdf",
    "size": 123456,
    "status": "uploaded"
  },
  {
    "file_id": "unique_file_id_2",
    "filename": "uploaded_filename2.png",
    "mime_type": "image/png",
    "size": 654321,
    "status": "uploaded"
  }
  // ... up to 5 files
]
```

### Error Responses

- **415 Unsupported Media Type:** The file type is not supported
- **413 Request Entity Too Large:** The file exceeds the maximum allowed size
- **400 Bad Request:** No file provided, invalid request, or more than 5 files uploaded
- **500 Internal Server Error:** Server-side processing error

## Example Usage

### cURL

```bash
curl -X POST \
  -F "file=@example1.pdf" \
  -F "file=@example2.png" \
  http://localhost:8000/upload-file
```

### JavaScript (Frontend)

```javascript
async function uploadFiles(files) {
  const formData = new FormData();
  Array.from(files).slice(0, 5).forEach(file => formData.append('file', file));

  try {
    const response = await fetch('http://localhost:8000/upload-file', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error uploading files:', error);
    throw error;
  }
}
```

## Configuration

The file upload functionality can be configured using environment variables:

```
UPLOAD_DIR=/path/to/upload/directory
MAX_FILE_SIZE=2097152000  # 2GB in bytes
ALLOWED_FILE_TYPES=application/pdf,image/jpeg,image/png,image/webp,image/heic,image/heif,text/plain,application/vnd.openxmlformats-officedocument.wordprocessingml.document
```

## Security & Validation

- **MIME type validation:** Only allowed file types are accepted
- **Filename sanitization:** Prevents path traversal and unsafe filenames
- **Size validation:** Files exceeding the configured size limit are rejected
- **File count validation:** Requests with more than 5 files are rejected
- **Temporary storage:** Files are stored temporarily and deleted after processing or expiration
- **No persistent storage:** Files are not stored long-term beyond Gemini's 48-hour TTL

## Notes

- Uploaded files are processed and, if necessary, sent to the Gemini API for further analysis
- For best results, ensure files are clear, legible, and within the supported size and type limits
- The response includes a unique file ID for tracking and referencing the upload in subsequent chat messages 
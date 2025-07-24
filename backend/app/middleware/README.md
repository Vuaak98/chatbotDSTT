# Error Handling & Security Middleware

This directory contains middleware components for error handling, rate limiting, and other security features for the AI Math Chatbot backend. These components are designed for modularity, maintainability, and robust protection of the API.

## 🛡️ Components

### Error Handler Middleware

The `ErrorHandlerMiddleware` provides centralized error handling for the application. It catches exceptions raised during request processing, logs them appropriately, and returns standardized error responses to clients.

Key features:
- Handles different types of exceptions (validation errors, HTTP exceptions, Gemini API errors, unexpected errors)
- Provides user-friendly error messages
- Logs detailed error information for debugging
- Prevents exposure of sensitive information in error responses

### Rate Limiter

The `RateLimiter` middleware prevents abuse of the API by limiting the number of requests that can be made within a time window. It tracks requests by IP address and endpoint, and returns a 429 Too Many Requests response when limits are exceeded.

Key features:
- Configurable rate limits per endpoint
- IP-based tracking
- Support for X-Forwarded-For header for clients behind proxies

### Exception Handlers

The `exception_handlers.py` module provides FastAPI exception handlers for specific types of exceptions:
- `request_validation_exception_handler`: Handles validation errors from request data
- `http_exception_handler`: Handles HTTP exceptions
- `gemini_api_exception_handler`: Handles Gemini API errors

## 🚀 Usage

These middleware components are registered in the main FastAPI application instance in `main.py`. The middleware is executed in reverse order (last added, first executed), so the order of registration is important.

```python
# Add middleware
# Note: Middleware is executed in reverse order (last added, first executed)

# Add rate limiting middleware
app.add_middleware(RateLimiter)

# Add error handling middleware
app.add_middleware(ErrorHandlerMiddleware)
```

The exception handlers are registered using FastAPI's `add_exception_handler` method:

```python
# Register exception handlers
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(google.genai.errors.APIError, gemini_api_exception_handler)
```

## 📚 More Information

- See the [backend README](../../README.md) for overall architecture, security, and best practices.
- Middleware and exception handling are key to robust, production-grade API design.

## 🔮 Future Considerations

- **JWT Authentication Middleware:** Add support for user authentication and authorization
- **CORS Middleware:** Fine-grained control over cross-origin requests
- **Advanced Logging:** Structured, externalized, or distributed logging
- **Request/Response Compression:** Improve performance for large payloads
- **Custom Metrics Middleware:** Track API usage, latency, and error rates
- **IP Blacklisting/Whitelisting:** Additional security controls
- **Tracing/Correlation IDs:** For distributed tracing and debugging

---

**Showcase your backend engineering skills:** This middleware layer demonstrates best practices in error handling, security, and modular API design for modern Python web applications.
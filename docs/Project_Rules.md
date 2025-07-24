# AI Math Chatbot - Project Rules

This document outlines the specific rules, standards, and procedures for developing the AI Math Chatbot project. It complements the `global_rules.md` file by providing project-specific details. All development should adhere to these rules when working within Cursor AI IDE or Windsurf IDE.

**References:**

*   `AI-MATH-CHATBOT-PRD.md`: Product Requirements Document
*   `AI_ Math_Chatbot_Development_Roadmap.md`: Development Roadmap
*   `gemini_api_doc.md`: Gemini API Documentation
*   `global_rules.md`: Global Development and Configuration Rules

## 1. Project Setup & Infrastructure

*   **Initialization:**
    *   Backend: Python 3.9+ with FastAPI.
    *   Frontend: React with TypeScript, initialized using Vite or Create React App.
*   **Directory Structure:** Maintain a clear separation between `frontend` and `backend` directories at the project root. Shared configuration or scripts can reside at the root level.
*   **Dependencies:**
    *   Use `requirements.txt` (backend) and `package.json` (frontend) for dependency management.
    *   Required Backend Libraries: `google-genai`, `fastapi`, `uvicorn`, `python-docx`, `pydantic`, `sqlite3` (standard library), `httpx` (for fetching files from URLs), appropriate Whisper client library (e.g., `openai`), `python-dotenv`.
    *   Required Frontend Libraries: `react`, `react-dom`, `typescript`, `tailwindcss`, `zustand`, `katex`, `react-speech-recognition`, `heroicons` (or `feather-icons`), potentially a markdown renderer (`react-markdown`) and syntax highlighter (`react-syntax-highlighter`).
    *   Keep dependencies up-to-date, addressing security vulnerabilities promptly.
*   **Environment Variables:**
    *   Define all sensitive keys (Gemini API Key, Whisper API Key) and configuration settings (e.g., backend port, database file path) in a `.env` file at the project root.
    *   Use `python-dotenv` (backend) or standard environment variable handling (frontend build process) to load these variables.
    *   **Never commit `.env` files to version control.** A `.env.example` file *must* be provided listing required variables.
*   **Containerization:**
    *   Develop `Dockerfile` for both frontend (multi-stage build for serving static files via a lightweight server like Nginx) and backend (Python environment).
    *   Use `docker-compose.yml` to orchestrate local development and testing environments for both services. See Section 6 of the Roadmap.

## 2. Development Standards

### 2.1 Backend (Python/FastAPI)

*   **Style Guide:** Adhere to PEP 8. Use linters (e.g., Flake8, Ruff) and formatters (e.g., Black) configured in the IDE.
*   **Typing:** Use Python type hints extensively (`typing` module). FastAPI relies heavily on type hints for validation and documentation.
*   **API Design:** Follow RESTful principles for endpoint design as outlined in Section 3.1 of the Roadmap. Use clear and consistent naming conventions.
*   **Async:** Leverage FastAPI's `async`/`await` for I/O-bound operations (API calls, database interactions, file reads).
*   **Error Handling:** Implement robust error handling using FastAPI's exception handlers. Return meaningful HTTP status codes and error messages (refer to Section 3.6 Roadmap, Section 4 PRD). Log errors server-side.
*   **Database:** Use SQLAlchemy Core or ORM for interactions with the SQLite database. Manage sessions appropriately (e.g., using FastAPI dependencies). Schema defined in Section 3.3 of the Roadmap.
*   **Modularity:** Organize code into logical modules (e.g., `routers`, `services`, `models`, `crud`, `utils`).

### 2.2 Frontend (React/TypeScript)

*   **Style Guide:** Follow standard React/TypeScript best practices. Use linters (e.g., ESLint) and formatters (e.g., Prettier) configured in the IDE.
*   **Typing:** Utilize TypeScript for strong typing across components, state, and props. Avoid `any` where possible.
*   **Component Structure:** Break down the UI into reusable functional components. Follow conventions for naming (`PascalCase`) and file organization (e.g., `src/components`, `src/hooks`, `src/store`, `src/services`).
*   **State Management:** Use Zustand for global state management (chat history, active chat, theme, etc.) as specified in the PRD. Use `useState` / `useReducer` for local component state.
*   **Styling:** Use Tailwind CSS utility classes for styling. Maintain consistency with the design described in Section 2 of the PRD (minimalist, light/dark themes).
*   **API Communication:**
    *   Use the native `fetch` API for standard requests to the backend.
    *   Implement Server-Sent Events (SSE) handling using `fetch` and `ReadableStream` for streaming AI responses from `/chat/stream`.
    *   Centralize API call logic (e.g., in a `src/services` directory).
*   **Accessibility (A11y):** Implement specific A11y features outlined in Section 5 of the PRD and `global_rules.md`. Use semantic HTML and ARIA attributes diligently.

### 2.3 API Integration (Gemini & Whisper)

*   **Gemini (`google-genai` SDK):**
    *   Instantiate the client using the API key from environment variables.
    *   Target Model: `gemini-2.5-flash-preview-04-17` (see Roadmap Section 4, PRD Section 6).
    *   Implement `generate_content_stream` or `chat.send_message_stream` for streaming responses (Roadmap Section 4).
    *   Implement multi-turn chat history management using `client.chats` (Roadmap Section 4).
    *   Set System Instructions via `GenerateContentConfig` (Roadmap Section 4).
    *   Handle multimodal input:
        *   Inline (`types.Part.from_bytes`): For files < ~20MB total request size (PDF, Images). See Roadmap Section 3.4 & 4, PRD Section 6, `gemini_api_doc.md`.
        *   Files API (`client.files.upload`): For files > ~20MB (up to 2GB). Pass the resulting `File` object. Acknowledge the 48-hour TTL. See Roadmap Section 3.4 & 4, PRD Section 6, `gemini_api_doc.md`.
    *   Handle text extraction from `.txt` and `.docx` (using `python-docx`) *before* sending to Gemini (Roadmap Section 3.4).
    *   Structure `contents` correctly using `types.Content` and `types.Part` (Roadmap Section 4, `gemini_api_doc.md`).
    *   Implement robust error handling for `google.genai.errors.APIError` (Roadmap Section 4).
*   **Whisper (Speech-to-Text):**
    *   Integrate with the specified Whisper API endpoint (OpenAI or Hugging Face).
    *   Manage Whisper API key securely via environment variables.
    *   Handle audio data transfer from frontend to backend (`/stt` endpoint).
    *   Implement error handling for transcription failures (Roadmap Section 3.5, PRD Section 4).

## 3. File Handling

*   **Supported Types (Client & Server Validation):**
    *   PDF: `application/pdf`
    *   Images: `image/jpeg`, `image/png`, `image/webp`, `image/heic`, `image/heif`
    *   Text: `text/plain`
    *   Word: `application/vnd.openxmlformats-officedocument.wordprocessingml.document` (.docx)
    *   See PRD Section 1 & 3.
*   **Size Limits (Client & Server Validation):**
    *   Client-side check (approximate) based on ~19MB inline limit suggestion from PRD/Gemini Docs.
    *   Server-side check: Route to inline processing (`types.Part.from_bytes`) or Gemini Files API (`client.files.upload`) based on size relative to the 20MB request limit and 2GB file limit. See Roadmap Sections 3.4 & 4, PRD Section 6, `gemini_api_doc.md`.
*   **Processing:**
    *   Backend extracts text from `.txt` and `.docx` before passing to Gemini.
    *   PDF and Images are passed directly to Gemini (either inline or via Files API).
*   **Frontend Display:** Show staged files as chips inside the input bar with remove ('x') functionality (PRD Section 1 & 3).
*   **Backend Storage:** No long-term persistent storage for uploaded files is planned beyond the 48-hour TTL of the Gemini Files API. Uploaded files for inline processing are handled in memory or temporary storage during the request lifecycle.

## 4. Testing

*   **Unit Tests:**
    *   Backend: Use `pytest`. Test individual functions/classes for database operations, file processing logic, API payload construction, utility functions. Mock external dependencies (Gemini API, Whisper API, DB calls).
    *   Frontend: Use `jest` and `react-testing-library`. Test individual components (rendering, state changes, event handlers), utility functions, and state logic (Zustand stores).
*   **Integration Tests:**
    *   Backend: Test API endpoints using `pytest` and `httpx` (or FastAPI's `TestClient`). Test interactions between components (e.g., router -> service -> crud). Test interaction with a test database. Mock external APIs (Gemini, Whisper).
    *   Frontend-Backend: Test the flow of data between frontend and backend API endpoints (e.g., sending a message, receiving a stream, uploading a file, STT).
*   **End-to-End (E2E) Tests:**
    *   Use tools like Playwright or Cypress.
    *   Simulate key user flows described in the PRD: basic text chat, file upload interaction, voice input interaction, chat history management (new, load, rename, delete).
    *   Cover streaming response display and interruption.
*   **Coverage:** Aim for reasonable test coverage, focusing on critical paths and business logic.
*   **CI/CD:** Integrate tests into a Continuous Integration pipeline (if applicable) to run automatically on commits/PRs.

## 5. Deployment

*   **Method:** Primarily via Docker Compose for local setup and potentially simple deployments.
*   **Artifacts:** Ensure Dockerfiles and `docker-compose.yml` are functional and optimized (e.g., multi-stage builds, minimal base images).
*   **Configuration:** Deployment configuration (ports, volumes, environment variables) should be clearly defined in `docker-compose.yml` or platform-specific configuration files.
*   **Documentation:** Provide clear, step-by-step instructions in the main `README.md` for building and running the application using Docker Compose.
*   **Platform:** While none specified, ensure the Dockerized setup is platform-agnostic enough for deployment on common cloud platforms (e.g., Cloud Run, AWS ECS, Azure Container Apps) with minimal changes.

## 6. Project Milestones

Development should progress according to the milestones defined in the `AI_ Math_Chatbot_Development_Roadmap.md`:

*   **Milestone 1:** Basic Text Chat (Core UI, Backend API, Gemini Text, Streaming, DB History)
*   **Milestone 2:** File Uploads (File UI, Backend Processing, Gemini Multimodal/Files API)
*   **Milestone 3:** Voice Input (Mic UI, Backend STT, Transcription Display)
*   **Milestone 4:** Chat History Management (Sidebar UI, CRUD Operations)
*   **Milestone 5:** Refinement (Error Handling, A11y, Responsiveness, Dockerization Finalization)

Track progress against these milestones using project management tools or issue tracking.

---
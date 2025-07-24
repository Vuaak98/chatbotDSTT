# Global Development & Configuration Rules

This document outlines global rules, standards, and best practices applicable to projects developed using Cursor AI IDE and Windsurf IDE. It serves as a baseline for quality, consistency, and maintainability across different projects, including the AI Math Chatbot. Project-specific rules can override or extend these guidelines as documented in their respective `project_rules.md`.

## 1. Accessibility (A11y) & User Experience (UX)

*   **Compliance:** Strive for **WCAG 2.1 AA** compliance in all web-based UIs.
*   **Semantic HTML:** Use HTML elements according to their semantic meaning (`<nav>`, `<main>`, `<aside>`, `<button>`, `<article>`, etc.). Avoid using `<div>` or `<span>` for interactive elements; use `<button>` or `<a>` instead.
*   **Keyboard Navigation:** All interactive elements *must* be navigable and operable using the keyboard alone. Ensure a logical tab order. Use `outline` styles for focus indicators (do not disable without providing a clear alternative).
*   **Screen Reader Support:**
    *   Use ARIA attributes (`aria-label`, `aria-labelledby`, `aria-describedby`, `aria-live`, `aria-hidden`, roles) appropriately to enhance screen reader understanding, especially for dynamic content updates and custom controls.
    *   Ensure images have descriptive `alt` text or are marked as decorative (`alt=""`).
    *   Ensure form elements have associated labels.
*   **Color Contrast:** Maintain sufficient color contrast ratios for text and UI elements as per WCAG AA guidelines (4.5:1 for normal text, 3:1 for large text and graphical elements). Test in both light and dark themes if applicable.
*   **Resizable Text:** Ensure the UI reflows correctly and remains usable when text size is increased up to 200% via browser zoom settings. Avoid fixed heights that clip text.
*   **Responsive Design:** Design UIs to be responsive across various screen sizes (mobile, tablet, desktop). Use mobile-first or desktop-first approaches consistently within a project. Utilize CSS media queries or responsive frameworks (like Tailwind CSS breakpoints).
*   **User Feedback:** Provide clear visual feedback for user actions (e.g., button clicks, loading states, success/error notifications, progress indicators). Use established patterns like spinners, skeletons, toasts, and inline messages.
*   **Consistency:** Maintain consistency in UI elements, terminology, layout, navigation, and interaction patterns throughout the application.

## 2. Error Handling & Logging

*   **User-Facing Errors:**
    *   Display errors in a user-friendly manner. Avoid exposing technical details or stack traces directly to the user.
    *   Provide clear, actionable error messages whenever possible (e.g., "Invalid email format" instead of "Error code 5.2.1").
    *   Display errors contextually (e.g., near the input field for validation errors) or globally (e.g., toasts/banners for API or server errors).
*   **Backend Error Handling:**
    *   Implement centralized error handling (e.g., FastAPI middleware or exception handlers).
    *   Catch specific exceptions rather than generic `Exception`.
    *   Map internal errors to appropriate HTTP status codes (4xx for client errors, 5xx for server errors).
*   **Logging:**
    *   Implement structured logging on the backend (e.g., using Python's `logging` module).
    *   Log relevant information for debugging: timestamps, severity levels (INFO, WARNING, ERROR, CRITICAL), request IDs, user context (if applicable), error messages, and stack traces for critical errors.
    *   Avoid logging sensitive user data (passwords, API keys, PII).
    *   Consider logging key events or application flow milestones at INFO level for monitoring.

## 3. Security

*   **API Key Management:**
    *   **Never hardcode API keys** or other secrets in source code.
    *   Use environment variables (`.env` files locally, secure secrets management in deployment) to store sensitive credentials.
    *   Ensure `.env` files are listed in `.gitignore`. Provide a `.env.example` template.
*   **Input Sanitization & Validation:**
    *   Validate and sanitize *all* input from users or external systems on the **backend**. This includes text input, file uploads, API parameters, etc.
    *   Protect against common vulnerabilities like Cross-Site Scripting (XSS), SQL Injection (use ORMs or parameterized queries), and Prompt Injection (carefully handle user input passed to LLMs).
*   **Dependency Security:** Regularly scan project dependencies for known vulnerabilities using tools like `npm audit`, `pip-audit`, or IDE integrations. Update vulnerable dependencies promptly.
*   **Rate Limiting:** Implement basic rate limiting on public-facing or resource-intensive API endpoints to prevent abuse.
*   **File Uploads:**
    *   Validate file types and sizes rigorously on the backend (do not rely solely on client-side validation or `Content-Type` headers).
    *   If storing/processing uploads, consider security scanning for malware.
*   **Authentication & Authorization (If Applicable):** If authentication is added, use standard, secure methods (e.g., OAuth 2.0, JWT with appropriate algorithms and expiry). Implement proper authorization checks for accessing resources. (Note: AI Math Chatbot PRD specifies *no authentication*).
*   **HTTPS:** Ensure all communication is over HTTPS in production environments.

## 4. Performance & Optimization

*   **API Usage:**
    *   Be mindful of API call costs and quotas (e.g., Gemini, Whisper).
    *   Use streaming responses (`generate_content_stream`) where appropriate to improve perceived performance.
    *   Consider `count_tokens` for estimating costs or validating input sizes.
    *   Explore context caching (`client.caches.create`) for Gemini if large contexts are frequently reused, understanding the cost implications and TTL (See `gemini_api_doc.md`).
*   **Database Queries:** Optimize database queries. Use indexing appropriately. Avoid N+1 query problems. Select only necessary data.
*   **Frontend Performance:**
    *   Optimize bundle sizes (code splitting, tree shaking).
    *   Lazy load components or routes where appropriate.
    *   Optimize images (proper formats, compression, responsive sizes).
    *   Minimize unnecessary re-renders (use `React.memo`, `useCallback`, `useMemo` judiciously).
*   **Backend Performance:** Profile and optimize slow backend endpoints or processing steps. Use asynchronous operations for I/O-bound tasks.

## 5. Collaboration & Version Control

*   **Version Control System:** **Git** is mandatory for all projects.
*   **Repository:** Use a central Git repository (e.g., GitHub, GitLab, Bitbucket).
*   **Branching Strategy:**
    *   Use a consistent branching strategy (e.g., a simplified Gitflow: `main` for production-ready code, `develop` for integration, feature branches `feature/your-feature-name`).
    *   Create feature branches off `develop`.
    *   **Never commit directly to `main` or `develop`.**
*   **Commits:**
    *   Write clear, concise commit messages following conventional commit standards (e.g., `feat: add file upload button`, `fix: resolve streaming display issue`).
    *   Commit small, logical units of work frequently.
*   **Code Reviews:**
    *   All code changes *must* be reviewed via Pull Requests (PRs) before merging into `develop` (and subsequently `main`).
    *   Require at least one approval (or project-specific number) for PRs.
    *   Reviewers should check for correctness, adherence to standards (project & global), potential bugs, security issues, and clarity.
*   **Code Formatting & Linting:**
    *   Configure and use automated formatters (e.g., Black, Prettier) and linters (e.g., Flake8, Ruff, ESLint) within the IDE.
    *   Ensure consistent settings across the team (e.g., via configuration files like `pyproject.toml`, `.eslintrc.js`, `prettierrc.js` committed to the repository).
    *   Code should pass linting checks before merging.

## 6. Documentation

*   **README.md:** Every project repository *must* have a `README.md` file at the root containing:
    *   Project title and brief description.
    *   Prerequisites for setting up the development environment.
    *   Step-by-step instructions for local setup and running the project (including environment variable setup).
    *   Instructions for running tests.
    *   (Optional) Basic usage guide or key features overview.
    *   (Optional) Deployment instructions.
*   **Code Comments:** Write clear comments for complex logic, non-obvious code sections, or public APIs/functions. Avoid commenting on obvious code. Focus on the "why," not just the "what." Use standard docstring formats (e.g., Google style for Python, JSDoc/TSDoc for TypeScript).
*   **API Documentation:** For backend APIs, leverage frameworks like FastAPI that auto-generate interactive documentation (Swagger UI/ReDoc) based on code and type hints. Ensure Pydantic models and endpoint definitions are clear.

## 7. Global Configurations & Libraries

*   **UI Frameworks/Libraries:** Prefer established, well-maintained libraries (e.g., React, FastAPI). Justify the inclusion of new major dependencies.
*   **Styling:** Tailwind CSS is the preferred utility-first CSS framework for consistency, unless a project has specific needs justifying another approach.
*   **Icons:** Use a consistent icon set across projects where feasible (e.g., Heroicons, Feather Icons).
*   **Math Rendering:** For web projects requiring math display, **KaTeX** is the preferred library due to its performance and rendering quality.
*   **State Management (Frontend):** While Zustand is specified for the AI Math Chatbot, other projects may choose alternatives like Redux Toolkit or Context API based on complexity, but the choice should be documented and justified.
*   **IDE Settings:** Encourage team members to utilize IDE features for linting, formatting, and type checking based on project configuration files (`.eslintrc.js`, `pyproject.toml`, `tsconfig.json`, etc.) to ensure consistency regardless of the specific IDE (Cursor AI, Windsurf).

---
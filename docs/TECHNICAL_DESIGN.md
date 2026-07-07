# RoastLab AI: Technical Design Specification (TDS)

This document is the **single source of truth** for RoastLab AI. It defines the exact boundaries, data structures, APIs, and AI contracts required to implement the system.

---

## 1. Project Vision
**Vision:** Make software engineering education entertaining and deeply analytical through AI.
**Mission:** Provide developers with instant, personality-driven code reviews backed by industry-standard static analysis and retrieved RAG context.
**Scope:** Automated PR/File reviews, RAG-backed suggestions, gamified feedback.
**Non-goals:** Fully automated code refactoring (we review, we do not commit changes on behalf of the user).

## 2. Functional Requirements
- **Authentication:** JWT-based login, registration, and refresh mechanics.
- **Projects:** File/Zip uploads, GitHub repo linking, project deletion.
- **AI Review:** Roast, Security, Performance, Architecture, and Doc reviews.
- **Dashboard:** Historical analysis, gamified achievements (e.g. *Spaghetti Chef* badge).

## 3. Non-Functional Requirements
- **Performance:** Non-AI API latency < 300ms. AI inference streamed via WebSockets/Server-Sent Events (SSE).
- **Reliability:** Automatic retry on LLM timeout (max 3 retries).
- **Security:** Secret scanning prior to LLM submission, JWT HttpOnly cookies, API rate limiting (100 req/min).

## 4. Module Contracts

### Example: Review Module
- **Responsibilities:** Coordinate the upload of code, static analysis, and multi-agent execution.
- **Input:** `ProjectId`, `List[Files]`
- **Output:** `ReviewReportDto`
- **Dependencies:** `AIOrchestratorService`, `RAGEngine`, `GitHubClient`
- **Errors:** `REVIEW001 (Files missing)`, `AI010 (Orchestrator Timeout)`.

## 5. API Contract (Standard)

All endpoints prefixed with `/api/v1`.

```http
POST /api/v1/reviews
Authorization: Bearer <token>
```
**Request:**
```json
{
  "project_id": "uuid",
  "roast_level": "brutal"
}
```
**Response (202 Accepted - Async Stream Initiated):**
```json
{
  "success": true,
  "message": "Review queued.",
  "data": {
    "review_id": "uuid",
    "stream_url": "wss://api.roastlab.ai/v1/reviews/uuid/stream"
  }
}
```

## 6. Database Design (PostgreSQL)

- **`users`**: `id` (UUID), `email`, `hashed_password`, `created_at`
- **`projects`**: `id`, `user_id` (FK), `name`, `github_url`, `created_at`
- **`reviews`**: `id`, `project_id` (FK), `status` (Enum), `score`, `created_at`
- **`review_items`**: `id`, `review_id` (FK), `agent_type`, `severity`, `feedback`
- **`achievements`**: `id`, `user_id` (FK), `badge_name`, `unlocked_at`

*All tables use UUIDv4 primary keys and Alembic for migrations.*

## 7. AI Contracts

### Roast Agent
- **Purpose:** Synthesize technical errors into sarcastic, personality-driven feedback.
- **Input Schema:** `AST_Data`, `Lint_Errors`, `RAG_Context`
- **Output Schema:** 
  ```json
  {
    "roast_text": "string",
    "technical_suggestions": ["string"],
    "confidence_score": "float"
  }
  ```
- **Temperature:** 0.8 (High creativity).
- **Fallback:** If JSON parsing fails, retry with lower temperature (0.2).

## 8. RAG Contracts

- **Parser:** Tree-sitter extracts AST nodes (classes, functions).
- **Chunker:** Semantic chunker respecting function boundaries.
- **Embedder:** BAAI BGE (`BAAI/bge-large-en-v1.5`).
- **Vector DB:** Qdrant (cosine similarity, 1024 dimensions).
- **Reranker:** BAAI BGE Reranker to filter top-K down to highly relevant context.
- **LLM:** Ollama (Llama 3 / DeepSeek).

## 9. Frontend Design

- **Architecture:** React 19 + Vite.
- **State Management:** Zustand (Global State) + TanStack Query (Server State).
- **Routing:** React Router (File-based/Object-based).
- **Components:** shadcn/ui + Tailwind CSS.
- **Real-time:** Native WebSocket hooks for streaming AI responses.

## 10. Backend Design

- **Controllers (`routers/`):** FastAPI endpoints handling HTTP/WSS.
- **Services (`services/`):** Business logic and LLM orchestration.
- **Repositories (`repositories/`):** SQLAlchemy ORM wrappers.
- **Workers (`workers/`):** Background tasks (e.g., repository cloning).

## 11. AI Orchestration

```text
User -> Upload Code -> Static Analyzer (Ruff/ESLint)
   -> Tree-Sitter Parser -> RAG Chunking -> Qdrant
   -> Orchestrator Agent
      -> [Parallel] Roast Agent, Security Agent, Perf Agent
      -> Aggregator Agent
   -> Stream Response via WSS -> Frontend
```

## 12. Event Flow

- **Code Uploaded Event:** Triggers static analysis and Tree-sitter parsing.
- **Review Queued Event:** Pushes task to background worker; client subscribes to WebSocket.
- **Agent Completed Event:** Emits partial JSON patch to WebSocket for real-time UI typing effect.

## 13. Error Catalogue

- `AUTH001`: Invalid credentials.
- `AUTH002`: Token expired.
- `PROJ001`: Repository inaccessible (Check GitHub Permissions).
- `AI010`: LLM inference timeout.
- `RAG001`: Qdrant connection refused.

## 14. Logging Strategy

Structured JSON logging via `structlog`.
- **Fields:** `timestamp`, `level`, `request_id`, `user_id`, `module`, `latency_ms`.
- No sensitive data (tokens, raw code) logged in production.

## 15. Monitoring

- **API Metrics:** FastAPI Prometheus middleware (Request count, latency).
- **AI Metrics:** Langfuse tracking for LLM token usage, prompt size, and generation latency.

## 16. Testing Strategy

- **Backend:** `pytest` unit tests (mocking DB/LLMs), integration tests (TestContainers for Postgres).
- **Frontend:** Vitest + React Testing Library.
- **AI Evaluation:** Ragas framework for evaluating RAG retrieval accuracy.

## 17. Coding Guidelines

- **Backend:** PEP-8, Ruff (formatting/linting), Mypy (strict typing), Google-style docstrings.
- **Frontend:** ESLint, Prettier, strict TypeScript (`any` is forbidden).

## 18. Deployment Strategy

- **Development:** `docker-compose` (FastAPI, React, Postgres, Redis, Qdrant, Ollama).
- **Production:** Ready for Kubernetes. Stateless API containers, managed databases.

## 19. Versioning Strategy

- **API:** URI versioning (`/api/v1`).
- **Database:** Alembic revisions.
- **Git:** Semantic Versioning + Conventional Commits.

## 20. Future Extension Points

- **Interfaces:** `ILLMProvider` to easily swap Ollama for OpenAI/Anthropic.
- **Vector DBs:** `IVectorStore` to swap Qdrant for Pinecone/PgVector.
- **Agents:** Pluggable `BaseAgent` class to dynamically register new personalities.

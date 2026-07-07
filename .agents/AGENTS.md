# RoastLab AI — Engineering Constitution

This document defines the immutable coding standards, architectural boundaries, and development rules for the RoastLab AI workspace. Every future task, feature branch, and pull request must strictly comply with these rules.

---

## 1. Engineering Principles
* **Clean Architecture:** Keep code segregated by explicit boundaries (Presentation ➡️ Application ➡️ Domain ⬅️ Infrastructure).
* **SOLID Principles:** Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion.
* **DRY (Don't Repeat Yourself):** Abstract shared logic into modular components.
* **KISS (Keep It Simple):** Avoid over-engineering; keep implementations readable and straightforward.
* **YAGNI (You Aren't Gonna Need It):** Implement only the current sprint's requirements.
* **Composition over Inheritance:** Rely on composition patterns rather than heavy class hierarchies.
* **Explicit over Implicit:** Write clear, self-documenting code. Prefer readable parameters over obscure dynamic configurations.
* **Fail Fast:** Validate inputs and connections early; throw typed errors immediately rather than propagating failures.
* **Secure by Default:** Sanitize inputs, enforce least-privilege permissions, and validate boundaries.
* **Testability First:** Design functions and components so they can be easily mocked and unit-tested.

---

## 2. Architectural Boundaries
```text
Presentation
    ↓
Application
    ↓
Domain
    ↓
Infrastructure
```
* **Domain Independence:** The Domain layer MUST remain framework-independent. It cannot import FastAPI, SQLAlchemy, Ollama, Qdrant, or any other external driver/provider.
* **Single Responsibility Ownership:**
  - `presentation/`: Controls routers, endpoints, request formatting, and middlewares.
  - `application/`: Controls use-cases, query/command handlers, and DTO validations.
  - `domain/`: Controls business rules, domain entities, value objects, and interfaces.
  - `infrastructure/`: Controls client pools, DB sessions, vector stores, caches, and API integrations.
  - `shared/`: Controls configuration models, security helpers, and common utilities.
* **AI Platform Boundary (`app/ai/`):** All AI orchestration, prompt templates, memories, agent configurations, evaluations, and workflows must belong exclusively to `backend/app/ai/`. Do not mix AI concerns directly inside REST routes.

---

## 3. Code Standards & Naming Conventions
* **Python (Backend):**
  - Use `snake_case` for functions, variables, and modules.
  - Use `PascalCase` for classes and custom types.
  - Use `UPPER_SNAKE_CASE` for constants.
  - Strict MyPy type-hinting on all function parameters and return signatures.
  - All public classes, methods, and utilities must contain Google-style Python docstrings.
* **React / TypeScript (Frontend):**
  - Follow **Feature-Sliced Design (FSD)**: `app/`, `pages/`, `widgets/`, `features/`, `entities/`, `shared/`.
  - Use `PascalCase.tsx` for components.
  - Use `useSomething.ts` for custom React hooks.
  - Features must not cross-import other features directly; use composition or public interface endpoints.
* **File Size Limits:**
  - React Component: ≤ 250 lines
  - Services: ≤ 300 lines
  - Repositories: ≤ 250 lines
  - API Routers: ≤ 200 lines
  - Utilities: ≤ 150 lines

---

## 4. Error Handling & Logging
* **Structured Exceptions:** Catch, type, and map all exceptions to standard JSON error structures. Never swallow errors.
* **Structured Logging:** Use `structlog` to output JSON format containing `request_id`, `timestamp`, `log_level`, and processing latency.
* **No Print Statements:** Never use raw `print()` statements. Rely exclusively on structured loggers.

---

## 5. Testing & CI/CD
* Every feature is considered incomplete without corresponding unit and integration tests.
* All commits must pass local pre-commit checks (`ruff`, `mypy`, `eslint`, `prettier`) before they can be merged.

---

## 6. Permanent Instruction for Agent
```text
You are the Principal Software Architect, Lead Backend Engineer, Lead Frontend Engineer, AI Engineer, DevOps Engineer, and Security Engineer for RoastLab AI.

You are responsible for building a production-grade AI platform.

Every generated file must comply with the RoastLab AI Engineering Constitution.

Mandatory Rules:
- Follow Clean Architecture.
- Follow SOLID, DRY, KISS, and YAGNI.
- Use Feature-Sliced Design on the frontend.
- Use a modular monolith on the backend.
- Keep the Domain layer framework-independent.
- Separate AI functionality into the dedicated AI Platform module.
- Use strict typing throughout.
- Use dependency injection and environment-based configuration.
- Apply structured logging, centralized error handling, and robust validation.
- Generate production-ready code only.
- Avoid placeholder implementations.
- Respect file size limits and single-responsibility principles.
- Ensure every feature includes tests where applicable.
- Do not introduce undocumented architectural changes.
- Modify only the files required for the current task.

Treat RoastLab AI as an enterprise-grade, open-source project intended for long-term maintenance and production deployment.
```

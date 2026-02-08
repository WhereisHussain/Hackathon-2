# Project Constitution

## 1. Core Principles
- **Agentic Workflow**: All code changes must be performed by AI agents. No manual coding by the user.
- **Spec-Driven Development**: All features must be defined in a specification file before implementation.
- **Clean Code**: Adhere to PEP 8 standards, use type hinting, and maintain modular architecture.
- **Testing**: Changes should be verified.

## 2. Tech Stack Setup
- **Language**: Python 3.13+
- **Package Manager**: UV (uv)
- **Architecture**: In-memory storage (list/dict), Console UI.
- **Operating System**: Windows / WSL2 logic (compatible with Windows paths).

## 3. Workflow
1.  **Spec**: Define requirements in `specs/`.
2.  **Plan**: Create an implementation plan.
3.  **Execute**: Implement changes using `uv` and Python.
4.  **Verify**: Run tests and manual verification.

## 4. Constraint Checklist & Confidence Score
1. Is the spec clear?
2. Is the plan approved?
3. Are tests defined?

Confidence Score: 5/5 (if all met)

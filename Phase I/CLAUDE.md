# CLAUDE.md (Agentic Guide)

## Environment
- **Python**: 3.13+
- **Manager**: `uv`

## Commands
- **Run App**: `uv run src/main.py` (or `python src/main.py` if dependencies manageable)
- **Install**: `uv sync`
- **Add Dependency**: `uv add <package>`
- **Test**: `uv run pytest` (if tests exist)
- **Lint**: `uv run ruff check .`

## Project Structure
- `src/`: Source code
- `specs/`: Specifications history
- `Constitution.md`: Project rules

# CoachCal
Local-first agentic dietician & trainer (Python + Streamlit + LangGraph + Ollama + MCP + SQLite).

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
ollama pull llama3.1:8b
streamlit run app.py
```

## Commands to run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
pre-commit install

make run      # streamlit
make lint     # ruff + black --check
make fmt      # autoformat
make test     # pytest
```

## Acceptance Criteria

Repo builds on a clean machine:

- `pip install -e .[dev]` succeeds.
- `ruff .` and `black --check .` pass.
- `pytest -q` passes (sanity test).

Streamlit boots:

- `streamlit run app.py` opens with the five placeholder pages in sidebar and renders without errors.

CI green:

- GitHub Actions workflow runs lint + tests successfully on Python 3.11.

MCP config present:

- `mcp/servers.json` exists and scopes filesystem to `./coachcal/data`.

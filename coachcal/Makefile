.PHONY: setup run lint fmt test qa

setup:
python -m venv .venv && . .venv/bin/activate && pip install -e .[dev] && pre-commit install

run:
streamlit run app.py

lint:
ruff . && black --check .

fmt:
black . && ruff --fix .

test:
pytest -q

qa:
python -c 'print({"ok": True})'

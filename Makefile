.PHONY: install install-dev lint test run-api run-ui clean

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

lint:
	ruff check src/

lint-fix:
	ruff check src/ --fix

test:
	pytest -v tests/

run-api:
	uvicorn src.api.routes:app --reload --host 0.0.0.0 --port 8000

run-ui:
	streamlit run src/ui/app.py

clean:
	rm -rf build/ dist/ *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +

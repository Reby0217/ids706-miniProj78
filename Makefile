# Ensure pip is upgraded and install all required packages
install:
	pip install --upgrade pip && pip install -r requirements.txt

# Setup the virtual environment
setup:
	python3 -m venv venv
	@echo "Virtual environment created. Activate with: 'source venv/bin/activate'"
	. venv/bin/activate && pip install --upgrade pip

# Run tests within the virtual environment
test:
	. venv/bin/activate && PYTHONPATH=. pytest tests/ 

# Lint the source code and tests
lint:
	. venv/bin/activate && ruff check src tests

# Format all Python files
format:
	. venv/bin/activate && black .

# Clean the virtual environment
clean:
	rm -rf venv

# Run the application with messages
run:
	. venv/bin/activate && python src/cli.py

# Run all major tasks: install, setup, lint, test, format
all: install setup lint test format

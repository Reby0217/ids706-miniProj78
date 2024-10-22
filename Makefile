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
	. venv/bin/activate && ruff check word_counter_py tests

# Format all Python files
format:
	. venv/bin/activate && black .

# Clean the virtual environment
clean:
	rm -rf venv

# Run the application with messages
run:
	. venv/bin/activate && python word_counter_py/cli.py test.txt

# Install the package using setup.py
install-package:
	pip install .

# Clean up the package files
clean-package:
	. venv/bin/activate && python setup.py clean --all


# Generate performance comparison report
report:
	. venv/bin/activate && \
	python word_counter_py/cli.py test.txt > python_results.txt && \
	cd word_counter_rust && \
	cargo build --release && \
	./target/release/word_counter_rust ../test.txt > ../rust_results.txt && \
	cd .. && \
	python ./src/generate_comparison_report.py

# Run all major tasks: install, setup, lint, test, format
all: install setup lint test format

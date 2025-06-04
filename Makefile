# Makefile for RPAL Interpreter

PYTHON = python
MAIN = Tokernizer.py


# Paths
TEST_DIR = Tests

all:
	@echo "Usage:"
	@echo "  make run FILE=<file.rpal>     # Run full interpreter"
	@echo "  make ast FILE=<file.rpal>     # Output AST"
	@echo "  make st FILE=<file.rpal>      # Output Standardized Tree"
	@echo 

run:
	$(PYTHON) $(MAIN) $(TEST_DIR)/$(FILE)

ast:
	$(PYTHON) $(MAIN) -ast $(TEST_DIR)/$(FILE)

st:
	$(PYTHON) $(MAIN) -st $(TEST_DIR)/$(FILE)

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -r {} +

.PHONY: all run ast st clean

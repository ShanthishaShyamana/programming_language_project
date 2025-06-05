# Makefile for RPAL Interpreter

PYTHON = python
MAIN = myrpal.py

all:
	@echo "Usage:"
	@echo "  make run FILE=sample1.rpal            # Run full interpreter"
	@echo "  make -ast FILE=tests/sample1.rpal      # Show AST (any path)"
	@echo "  make -st FILE=sample1.rpal             # Show ST"
	@echo

# Run full interpreter
run:
	$(PYTHON) $(MAIN) $(FILE)

# Print Abstract Syntax Tree
ast:
	$(PYTHON) $(MAIN) -ast $(FILE)

# Print Standardized Tree
st:
	$(PYTHON) $(MAIN) -st $(FILE)

# Aliases for dash-style
-ast: ast
-st: st

# Clean cache
clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -r {} +

.PHONY: all run ast st -ast -st clean

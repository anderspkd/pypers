TEST_DIR="./test/"
RUN_TEST=python -m unittest discover -s $(TEST_DIR)
VENV_DIR="./venv/bin/activate"

TFLAGS="-v"
LOG_LEVEL=info

venv:
	( source VENV_DIR )

test: venv
	PYPER_LOG_LEVEL=$(LOG_LEVEL) $(RUN_TEST) $(TFLAGS)

.PHONY: test

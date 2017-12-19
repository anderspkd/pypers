TEST_DIR="./test/"
RUN_TEST=python -m unittest discover -s $(TEST_DIR)
TFLAGS="-v"
LOG_LEVEL=info

test:
	PYPER_LOG_LEVEL=$(LOG_LEVEL) $(RUN_TEST) $(TFLAGS)

.PHONY: test

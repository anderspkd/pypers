TEST_DIR="./test/"
RUN_TEST=python -m unittest discover -s $(TEST_DIR)
VENV_DIR="./venv/bin/activate"

venv:
	( source VENV_DIR )

test_full: venv
	$(RUN_TEST) -v

test_failfast: venv
	$(RUN_TEST) -f -v

all: check coverage lint

lint:
	@flake8 child_support_tables

check:
	@flake8 --select=F child_support_tables

test:
	@python setup.py test --addopts -vv

debug:
	@python setup.py test --addopts --pdbcls=IPython.terminal.debugger:TerminalPdb \
	                      --addopts --show-locals

coverage:
	@coverage html

clean:
	@rm -rf .coverage htmlcov

.PHONY: all check test coverage lint clean

# Project constants
PROJECT = aiohttp_middlewares
DOCS_DIR = docs

# Project vars
POETRY ?= poetry
PIP_COMPILE ?= pip-compile
PRE_COMMIT ?= pre-commit
PYTHON ?= $(POETRY) run python
TOX ?= tox

# Docs vars
DOCS_HOST ?= localhost
DOCS_PORT ?= 8241

include python.mk

all: install

.PHONY: clean
clean: clean-python

.PHONY: distclean
distclean: clean distclean-python

.PHONY: docs
docs: install
	$(PYTHON) -m sphinx_autobuild --host $(DOCS_HOST) --port $(DOCS_PORT) -b html $(DOCS_DIR)/ $(DOCS_DIR)/_build/

.PHONY: install
install: install-python

.PHONY: lint
lint: lint-python

.PHONY: lint-and-test
lint-and-test: lint test

.PHONY: list-outdated
list-outdated: list-outdated-python

.PHONY: test
test: install clean test-only

.PHONY: test-only
test-only:
	TOXENV=$(TOXENV) $(TOX) $(TOX_ARGS)

.PHONY: test-%
test-%: install clean
	TOXENV=$(subst test-,,$@) $(TOX) $(TOX_ARGS)

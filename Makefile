.PHONY: \
	clean \
	distclean \
	docs \
	install \
	lint \
	lint-and-test \
	list-outdated \
	test \
	test-only

# Project constants
PROJECT = aiohttp_middlewares
DOCS_DIR = ./docs

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

clean: clean-python

distclean: clean distclean-python

docs: install
	$(PYTHON) -m sphinx_autobuild --host $(DOCS_HOST) --port $(DOCS_PORT) -b html $(DOCS_DIR)/ $(DOCS_DIR)/_build/

install: install-python

lint: lint-python

lint-and-test: lint test

list-outdated: list-outdated-python

test: install clean test-only

test-only:
	TOXENV=$(TOXENV) $(TOX) $(TOX_ARGS)

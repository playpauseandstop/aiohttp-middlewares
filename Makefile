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

docs: .install $(DOCS_DIR)/requirements.txt $(DOCS_DIR)/requirements-sphinx.txt
	$(PYTHON) -m pip install -r $(DOCS_DIR)/requirements-sphinx.txt
	$(PYTHON) -m sphinx_autobuild --host $(DOCS_HOST) --port $(DOCS_PORT) -b html $(DOCS_DIR)/ $(DOCS_DIR)/_build/

$(DOCS_DIR)/requirements.txt: .install-python
	$(POETRY) export -f requirements.txt -o $(DOCS_DIR)/requirements.txt --without-hashes

$(DOCS_DIR)/requirements-sphinx.txt: $(DOCS_DIR)/requirements-sphinx.in
	$(PIP_COMPILE) -Ur --allow-unsafe $(DOCS_DIR)/requirements-sphinx.in

install: install-python

lint: lint-python

lint-and-test: lint test

list-outdated: list-outdated-python

test: install clean test-only

test-only:
	TOXENV=$(TOXENV) $(TOX) $(TOX_ARGS)

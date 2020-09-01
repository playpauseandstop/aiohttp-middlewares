.PHONY: \
	clean \
	distclean \
	docs \
	install \
	lint \
	lint-only \
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

all: install

clean:
	find . \( -name __pycache__ -o -type d -empty \) -exec rm -rf {} + 2> /dev/null

clean-egg-info:
	-find . \( -name *.egg-info -type d \) -exec rm -rf {} +

distclean: clean
	rm -rf build/ dist/ *.egg*/ .tox/ .venv/ .install

docs: .install $(DOCS_DIR)/requirements.txt $(DOCS_DIR)/requirements-sphinx.txt
	$(PYTHON) -m pip install -r $(DOCS_DIR)/requirements-sphinx.txt
	$(PYTHON) -m sphinx_autobuild --host $(DOCS_HOST) --port $(DOCS_PORT) -b html $(DOCS_DIR)/ $(DOCS_DIR)/_build/

$(DOCS_DIR)/requirements.txt: .install
	$(POETRY) export -f requirements.txt -o $(DOCS_DIR)/requirements.txt

$(DOCS_DIR)/requirements-sphinx.txt: $(DOCS_DIR)/requirements-sphinx.in
	$(PIP_COMPILE) -Ur --allow-unsafe --generate-hashes $(DOCS_DIR)/requirements-sphinx.in

install: .install
.install: pyproject.toml poetry.toml poetry.lock
	@$(MAKE) -s clean-egg-info
	$(POETRY) install
	touch $@

lint: install lint-only

lint-only:
	SKIP=$(SKIP) $(PRE_COMMIT) run --all $(HOOK)

list-outdated: install
	$(POETRY) show -o

poetry.toml:
	$(POETRY) config --local virtualenvs.create true
	$(POETRY) config --local virtualenvs.in-project true

test: install clean lint test-only

test-only:
	TOXENV=$(TOXENV) $(TOX) $(TOX_ARGS) -- $(TEST_ARGS)

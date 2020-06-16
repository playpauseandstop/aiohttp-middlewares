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
PRE_COMMIT ?= pre-commit
PYTHON ?= $(POETRY) run python
SPHINXBUILD ?= $(POETRY) run sphinx-build
TOX ?= tox

# Docs vars
DOCS_HOST ?= localhost
DOCS_PORT ?= 8241

all: install

clean:
	find . \( -name __pycache__ -o -type d -empty \) -exec rm -rf {} + 2> /dev/null

distclean: clean
	rm -rf build/ dist/ *.egg*/ .tox/ .venv/ .install

docs: .install
	$(PYTHON) -m pip install -r docs/requirements.txt
	$(POETRY) run sphinx-autobuild -B -H $(DOCS_HOST) -p $(DOCS_PORT) -b html $(DOCS_DIR)/ $(DOCS_DIR)/_build/

install: .install
.install: pyproject.toml poetry.toml poetry.lock
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

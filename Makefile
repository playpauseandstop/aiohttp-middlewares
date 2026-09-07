# Project constants
PROJECT = aiohttp_middlewares
DOCS_DIR = docs

# Docs vars
DOCS_HOST ?= localhost
DOCS_PORT ?= 8241

include python.mk

TOX_VERSION ?= 4.61.2
TOX_UV_VERSION ?= 1.36.0
TOX = $(UVX) --with="tox-uv==$(TOX_UV_VERSION)" tox==$(TOX_VERSION)

# Non-phony targets
all: install

.env:
	touch "$@"

# Phony targets
.PHONY: clean
clean: clean-python

.PHONY: distclean
distclean: clean distclean-python

.PHONY: docs
docs: install .env .env.local
	$(UV_RUN) -m sphinx_autobuild --host $(DOCS_HOST) --port $(DOCS_PORT) -b html $(DOCS_DIR)/ $(DOCS_DIR)/_build/

.PHONY: install
install: install-python

.PHONY: lint
lint: lint-python

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

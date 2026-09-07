GIT_DIR = .git
PYTHON_DIST_DIR ?= dist
SCRIPTS_DIR ?= scripts
VENV_DIR = .venv

PYTHON_BIN = $(VENV_DIR)/bin/python
PYTHON_VERSION = $(shell cat ".python-version")

UV ?= uv
UV_BUILD ?= $(UV) build
UV_RUN ?= $(UV) run --env-file=.env --env-file=.env.local
UV_SYNC ?= $(UV) sync
UVX ?= uvx -p $(PYTHON_VERSION)

PRE_COMMIT_VERSION ?= 4.6.2
PRE_COMMIT = $(UVX) pre-commit==$(PRE_COMMIT_VERSION)

# Non-phony targets
.env.local:
	touch $@

.install-python: $(PYTHON_BIN) uv.lock
	touch $@

uv.lock: pyproject.toml
	@$(MAKE) --no-print-directory install-python-only
	touch $@

$(PYTHON_BIN): .python-version uv.lock
	@$(MAKE) --no-print-directory install-python-only
	touch $@

# Phony targets
.PHONY: build-python
build-python: install-python build-python-only

.PHONY: build-python-only
build-python-only:
	$(UV_BUILD) --wheel -o $(PYTHON_DIST_DIR)/ $(ARGS)

.PHONY: clean-egg-info
clean-egg-info:
	-find . \( -name *.egg-info -a -type d -not -path '$(VENV_DIR)/*' \) -exec rm -rf {} + 2> /dev/null

.PHONY: clean-python
clean-python:
	-find . \( -name __pycache__ -o -type d -empty -not -path '$(GIT_DIR)/*' \) -exec rm -rf {} + 2> /dev/null

.PHONY: distclean-python
distclean-python: clean-python clean-egg-info
	-rm -rf .coverage .install-python $(VENV_DIR)/ $(PYTHON_DIST_DIR)/

.PHONY: install-pre-commit
install-pre-commit: .python-version
	$(PRE_COMMIT) install

.PHONY: install-python
install-python: .install-python

.PHONY: install-python-only
install-python-only:
	$(UV_SYNC) $(ARGS)

.PHONY: lint-python
lint-python: install-python lint-python-only

.PHONY: lint-python-only
lint-python-only:
	SKIP=$(SKIP) $(PRE_COMMIT) run --all $(HOOK) $(ARGS)

.PHONY: list-outdated-python
list-outdated-python: install-python list-outdated-python-only

.PHONY: list-outdated-python-only
list-outdated-python-only:
	$(UV) pip list --outdated $(ARGS)

.PHONY: python-version
python-version:
	@echo "Expected: Python $(PYTHON_VERSION)"
	@if [ -f "$(PYTHON_BIN)" ]; then echo "Virtual env: $$("$(PYTHON_BIN)" -V)"; else echo "Virtual env: -"; fi

.PHONY: run-python
run-python: install-python run-python-only

.PHONY: run-python-only
run-python-only: SHELL := /bin/bash
run-python-only: .env.local
	@if [ -z "$(PACKAGE)" ]; then echo >&2 "Usage make $@ PACKAGE=... [ARGS=...]"; exit 2; fi
	$(UV_RUN) -m $(PACKAGE) $(ARGS)

.PHONY: script
script: install-python script-only

.PHONY: script-only
script-only: SHELL := /bin/bash
script-only: .env.local
	@if [ -z "$(SCRIPT)" ]; then echo >&2 "Usage: make $@ SCRIPT=... [ARGS=...]"; exit 2; fi
	$(UV_RUN) $(SCRIPTS_DIR)/$(SCRIPT).py $(ARGS)

.PHONY: script-%
script-%: install-python
	@$(MAKE) --no-print-directory script SCRIPT="$(subst script-,,$@)" ARGS="$(ARGS)"

.PHONY: test-python
test-python: install-python test-python-only

# Use TEST_ARGS instead of ARGS to avoid conflicts with other targets (e.g.,
# install-python-only) when Make propagates command-line variables to recursive
# calls
.PHONY: test-python-only
test-python-only: .env.local test-python-setup
	# pytest options: $(PYTEST_ADDOPTS)
	$(UV_RUN) -m pytest $(TEST_ARGS)
	@$(MAKE) --no-print-directory test-python-teardown

.PHONY: test-python-setup
test-python-setup:

.PHONY: test-python-teardown
test-python-teardown:

.PHONY: update-pre-commit
update-pre-commit: install-pre-commit
	$(PRE_COMMIT) autoupdate

.PHONY: uv-update
uv-update: install-python uv-update-only
	# Need to call install python (uv sync) again after the update
	@$(MAKE) --no-print-directory install-python-only

.PHONY: uv-update-only
uv-update-only:
	@if [ -z "$(PACKAGE)" ]; then echo >&2 "Usage: make $@ PACKAGE=..."; exit 2; fi
	$(UV) lock $(foreach package,$(PACKAGE),--upgrade-package $(package))

.PHONY: uv-upgrade
uv-upgrade: SHELL := /bin/bash
uv-upgrade: install-python
	@if [ -z "$(PACKAGE)" ]; then echo >&2 "Usage: make $@ PACKAGE=..."; exit 2; fi
	@group_re='\(group: ([^)]+)\)'; \
	for package in $(PACKAGE); do \
		args=""; \
		if [[ "$$($(UV) tree -q -d 1 | grep -F " $${package} v")" =~ $${group_re} ]]; then \
			args="--group=$${BASH_REMATCH[1]}"; \
		fi; \
		echo "Upgrading $${package}"; \
		$(UV) remove $${args} $${package}; \
		$(MAKE) --no-print-directory uv-update-only PACKAGE="$${package}"; \
		if [ -n "$(BOUNDS)" ]; then args="$${args} --bounds=$(BOUNDS)"; fi; \
		$(UV) add $${args} $${package}; \
	done

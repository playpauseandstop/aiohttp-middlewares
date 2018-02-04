.PHONY: clean coveralls deploy distclean docs install lint setup-pyenv test

# Project settings
PROJECT = aiohttp_middlewares

# Virtual environment settings
ENV ?= env
VENV = $(shell python -c "import sys; print(int(hasattr(sys, 'real_prefix')));")

# Python commands
ifeq ($(VENV),1)
	COVERALLS = coveralls
	PYTHON = python
	SPHINXBUILD = sphinx-build
else
	COVERALLS = $(ENV)/bin/coveralls
	PYTHON = $(ENV)/bin/python
	SPHINXBUILD = `pwd`/$(ENV)/bin/sphinx-build
endif

# Bootstrapper args
ifeq ($(CIRCLECI),true)
	bootstrapper_args = --ignore-activated
endif

# Tox args
ifneq ($(TOXENV),)
	tox_args = -e $(TOXENV)
endif

all: install

clean:
	find . \( -name __pycache__ -o -type d -empty \) -exec rm -rf {} + 2> /dev/null

coveralls:
	-$(COVERALLS)

deploy:
ifeq ($(TWINE_USERNAME),)
	# TWINE_USERNAME env var should be supplied
	exit 1
endif
ifeq ($(TWINE_PASSWORD),)
	# TWINE_PASSWORD env var should be supplied
	exit 1
endif
ifeq ($(CIRCLECI),)
	$(MAKE) test
endif
	rm -rf build/ dist/
	python setup.py sdist bdist_wheel
	$(PYTHON) -m twine upload dist/*

distclean: clean
	rm -rf build/ dist/ *.egg*/ $(ENV)/

docs: .install
	$(MAKE) -C docs/ SPHINXBUILD=$(SPHINXBUILD) html

install: .install
.install: setup.py requirements-dev.txt
	python -m bootstrapper -r requirements-dev.txt -e $(ENV)/ $(bootstrapper_args)
	touch $@

lint:
	TOXENV=lint $(MAKE) test

list-outdated: .install
	$(PYTHON) -m pip list -lo

setup-pyenv:
ifneq ($(CIRCLECI),)
	pyenv local 3.5.3 3.6.2
else
	pyenv local 3.5.4 3.6.4
endif

test: .install clean
	$(PYTHON) -m tox $(tox_args) $(TOX_ARGS) -- $(TEST_ARGS)

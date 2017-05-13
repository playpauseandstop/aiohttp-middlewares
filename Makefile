PROJECT = aiohttp_middlewares
ENV ?= env

all: test

install: .install
.install: requirements.txt setup.py
	bootstrapper -e $(ENV)/ -d
	touch $@

lint: .install
	$(ENV)/bin/flake8 $(PROJECT)/ tests/
	$(ENV)/bin/mypy $(PROJECT)/

test: lint
	$(ENV)/bin/pytest tests/

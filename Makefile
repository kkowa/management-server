#!/usr/bin/env make -f

MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules
MAKEFLAGS += --silent

SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
.DEFAULT_GOAL := help
help: Makefile
	@grep -E '(^[a-zA-Z_-]+:.*?##.*$$)|(^##)' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}' | sed -e 's/\[32m##/[33m/'


# =============================================================================
# Common
# =============================================================================
install:  ## Install the app locally
	command -v pyenv > /dev/null && pyenv install --skip-existing "$$(pyenv local)"
	poetry install -vv
.PHONY: install

init:  ## Initialize project repository
	git submodule update --init
	poetry run pre-commit autoupdate
	poetry run pre-commit install --install-hooks --hook-type pre-commit --hook-type commit-msg
.PHONY: init

run:  ## Run development server
	poetry run uvicorn config.asgi:application --host 0.0.0.0 --reload --log-level debug
.PHONY: run


# =============================================================================
# CI
# =============================================================================
ci: lint test scan  ## Run CI tasks
.PHONY: ci

generate:  ## Generate codes from schemas
	mkdir -p _generated/grpc
	poetry run python -m grpc_tools.protoc \
		--proto_path=idl/grpc/protos \
		--grpc_python_out=_generated/grpc \
		--python_out=_generated/grpc \
		--pyi_out=_generated/grpc \
		idl/grpc/protos/helloworld/*.proto
.PHONY: generate

format:  ## Run autoformatters
	poetry run black .
	poetry run isort .
.PHONY: format

lint:  ## Run all linters
	poetry run black --check .
	poetry run isort --diff .
	poetry run flake8
	poetry run pydocstyle
	poetry run mypy --show-error-codes --pretty .
.PHONY: lint

test:  ## Run tests
	poetry run pytest
.PHONY: test

scan:  ## Run all scans

.PHONY: scan

# TODO: Move generation codes to config/{api,graphql}.py, to generate when execute them directly (__main__)
schema-export:  ## Export service schemas
	poetry run python manage.py shell -c 'exec("""\nimport json\nfrom config.api import get_api_application\nwith open("idl/openapi/schemas/server.openapi.json", mode="wt", encoding="utf-8") as f:\n    json.dump(get_api_application().openapi_schema, f)\n""")'
	poetry run python manage.py export_schema config.graphql:schema --path idl/graphql/schemas/server.graphql
.PHONY: export


# =============================================================================
# Handy Scripts
# =============================================================================
shell:  ## Start new python interactive shell
	poetry run python manage.py shell_plus
.PHONY: shell

notebook:  ## Start jupyter notebook server
	poetry run python manage.py shell_plus --notebook
.PHONY: notebook

clean:  ## Remove temporary files
	rm -rf .mypy_cache/ .pytest_cache/ htmlcov/ staticfiles/ .coverage coverage.xml report.xml
	find . -path '*/__pycache__*' -delete
	find . -path "*.log*" -delete
.PHONY: clean

#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

poetry run python manage.py collectstatic --noinput
poetry run uvicorn config.asgi:application --host 0.0.0.0

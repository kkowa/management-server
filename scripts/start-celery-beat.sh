#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

rm -f './celerybeat.pid'
poetry run celery -A config.celery_app beat -l DEBUG

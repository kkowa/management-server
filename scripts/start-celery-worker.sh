#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

poetry run celery -A config.celery_app worker -l DEBUG

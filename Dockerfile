# =============================================================================
# Core: Build
# =============================================================================
ARG PYTHON_VERSION="3.11"
ARG POETRY_VERSION="1.2.2"

# Application directory
ARG APP_HOME="/var/app"

FROM python:${PYTHON_VERSION}-slim-bullseye AS build

ARG POETRY_VERSION
ARG APP_HOME

# Core deps
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

WORKDIR ${APP_HOME}

COPY poetry.lock poetry.toml pyproject.toml ./

# Full installation
RUN poetry install --verbose --no-ansi --no-interaction --no-root --sync --with dev

# Extra processing stage to remove non-default dependencies
# TODO: Caching maybe effective
FROM build AS build-minimal

# Uninstall non-main dependencies
RUN poetry install --verbose --no-ansi --no-interaction --no-root --sync --only main

# =============================================================================
# Core: Base
# =============================================================================
FROM python:${PYTHON_VERSION}-slim-bullseye AS base

ARG POETRY_VERSION
ARG APP_HOME

# App user (worker) for manual UID and GID set
ARG UID="1000"
ARG GID="1000"

# Python control variables
ENV PYTHONUNBUFFERED="1"
ENV PYTHONDONTWRITEBYTECODE="1"

# Add gRPC stub path for imports
ENV PYTHONPATH="${APP_HOME}/_generated/grpc:${PYTHONPATH}"

SHELL ["/bin/bash", "-c"]

# Core deps
RUN apt-get update && apt-get install --no-install-recommends -y \
    curl \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

# Change working directory
WORKDIR ${APP_HOME}

# Create app user and set as app owner
RUN groupadd --gid ${GID} worker \
    && useradd  --system --uid ${UID} --gid ${GID} --create-home worker \
    && chown -R worker:worker ${APP_HOME}

EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=5 \
    CMD ["curl", "-fsSL", "localhost:8000/ht/"]

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["start.sh"]

# =============================================================================
# Environment: Development
# =============================================================================
FROM base AS development

ARG APP_HOME

VOLUME ["${APP_HOME}/.venv"]

# Install dev-only utilities
RUN apt-get update && apt-get install --no-install-recommends -y \
    gettext \
    git \
    gnupg2 \
    libpq-dev \
    make \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# Install python deps
COPY --from=build --chown=worker:worker ${APP_HOME}/.venv ${APP_HOME}/.venv

# Copy script files implicitly
COPY --chown=worker:worker --chmod=755 \
    ./scripts/docker-entrypoint.sh ./scripts/start-celery-beat.sh \
    ./scripts/start-celery-worker.sh ./scripts/start-flower.sh ./scripts/start.sh \
    /usr/local/bin/

# Copy source codes
COPY --chown=worker:worker . .

USER worker:worker

# =============================================================================
# Environment: Production
# =============================================================================
FROM base AS production

# Install python deps
COPY --from=build-minimal --chown=worker:worker ${APP_HOME}/.venv ${APP_HOME}/.venv

# Copy script files implicitly
COPY --chown=worker:worker --chmod=755 \
    ./scripts/docker-entrypoint.sh ./scripts/start-celery-beat.sh \
    ./scripts/start-celery-worker.sh ./scripts/start-flower.sh ./scripts/start.sh \
    /usr/local/bin/

# Copy source codes
COPY --chown=worker:worker . .

USER worker:worker

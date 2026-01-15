FROM python:3.13-slim AS base
WORKDIR /app


FROM base AS devcontainer
ENV UV_LINK_MODE=copy
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update && apt-get install -y git \
    && rm -rf /var/lib/apt/lists/*

ARG USER_UID=1234
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID developer
RUN useradd --uid $USER_UID --gid $USER_GID --create-home --shell /bin/bash developer
USER developer

#!/bin/bash
set -euo pipefail

uv sync --frozen --all-groups
uv run pre-commit install --install-hooks

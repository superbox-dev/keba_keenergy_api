#!/usr/bin/env bash

set -e

cd "$(dirname "$0")/.."

uv sync --locked --dev
uv run prek install --force

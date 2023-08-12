#!/usr/bin/env bash
set -e

black --check --diff src tests
isort --check --diff --profile black src tests
mypy --strict src tests
pip install --quiet .
pytest --quiet tests

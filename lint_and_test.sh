#!/usr/bin/env bash
set -e

black --check --diff src tests
mypy --strict src
pip install --quiet .
pytest --quiet tests

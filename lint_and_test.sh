#!/usr/bin/env bash
set -e

black --check --diff src tests
mypy src tests
pip install --quiet .
pytest --quiet tests

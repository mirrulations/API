#!/bin/bash

# Lint Python files with flake8
echo "Running flake8..."
flake8 endpoints/ || exit 1

echo "Running black (format check)..."
black --check endpoints/ || exit 1

# Lint YAML files (AWS SAM and configs)
echo "Running yamllint..."
yamllint template.yml || exit 1
yamllint samconfig.toml || exit 1

echo "All lint checks passed!"

# To run linting before each commit, add this script to .git/hooks/pre-commit 
# and make it executable with the following command:
# chmod +x .git/hooks/pre-commit


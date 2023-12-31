#!/bin/bash

# Exit in case of error
set -e

# Define your package directory and PyPI repository
PACKAGE_DIR="bashgpt"
PYPI_REPOSITORY="https://upload.pypi.org/legacy/"  # Use this for the real PyPI
# PYPI_REPOSITORY="https://test.pypi.org/legacy/" # Use this for TestPyPI

echo "Building the package..."

# Remove previous builds
rm -rf dist/ build/ *.egg-info/

# Create the distribution package
python setup.py sdist bdist_wheel

echo "Uploading the package to PyPI..."
# Upload the package to PyPI using Twine
twine upload --repository-url $PYPI_REPOSITORY dist/* --verbose

echo "Package uploaded successfully!"
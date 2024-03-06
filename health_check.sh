#!/bin/bash

# Run pytest and capture its output
response=$(pytest -p no:warnings -v -s 2>&1)
exit_code=$?

# Check the exit code of pytest
if [ $exit_code -eq 0 ]; then
    echo "pytest execution was normal."
    exit 1
else
    echo "pytest encountered some errors."
    echo "$response"
    exit 0
fi
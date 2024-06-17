#!/bin/bash

# Find all .tar.gz files in the current directory
files=$(find . -maxdepth 1 -type f -name "*.tar.gz")

# Check if files were found
if [ -z "$files" ]; then
    echo "No .tar.gz files found in the current directory."
    exit 1
fi

# Extract each found tar.gz file
for file in $files; do
    echo "Extracting '$file'..."
    tar -xzvf "$file"
    echo "'$file' extracted."
done

echo "All files extracted."

echo "Running Python scripts"

python main.py pharmacies claims reverts
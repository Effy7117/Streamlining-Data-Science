#!/bin/bash

# Paths
INPUT_FILE="/home/effy/deaths-leading-causes.xlsx"
TMP_CSV="/tmp/deaths-leading-causes.csv"

# Check if xlsx2csv is installed
if ! command -v xlsx2csv &> /dev/null; then
    echo "xlsx2csv is required for extraction. Please install it first."
    exit 1
fi

# Extract data
echo "Extracting data..."
xlsx2csv "$INPUT_FILE" > "$TMP_CSV"
echo "Extraction process completed."


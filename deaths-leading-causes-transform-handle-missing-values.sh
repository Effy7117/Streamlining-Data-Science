#!/bin/bash

# Paths
TMP_NO_DUPLICATES_XLSX="/home/effy/deaths-leading-causes-no-duplicates.xlsx"
TMP_CLEANED_XLSX="/home/effy/deaths-leading-causes-cleaned.xlsx"

# Handle missing values
echo "Handling missing values..."
python3 <<EOF
import pandas as pd

df = pd.read_excel("$TMP_NO_DUPLICATES_XLSX")
df['Total Deaths'] = pd.to_numeric(df['Total Deaths'], errors='coerce')
df['Total Deaths'].fillna(df['Total Deaths'].median(), inplace=True)
df.to_excel("$TMP_CLEANED_XLSX", index=False)
EOF
echo "Missing values handled."


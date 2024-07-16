#!/bin/bash

# Paths
TMP_XLSX="/home/effy/deaths-leading-causes.xlsx"
TMP_NO_DUPLICATES_XLSX="/home/effy/deaths-leading-causes-no-duplicates.xlsx"

# Remove duplicates
echo "Removing duplicates..."
python3 <<EOF
import pandas as pd

df = pd.read_excel("$TMP_XLSX")
df.drop_duplicates(inplace=True)
df.to_excel("$TMP_NO_DUPLICATES_XLSX", index=False)
EOF
echo "Duplicates removed."


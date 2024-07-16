#!/bin/bash

# Paths
TMP_CLEANED_XLSX="/home/effy/deaths-leading-causes-cleaned.xlsx"
TMP_CLEANED_NUMERIC_XLSX="/home/effy/deaths-leading-causes-cleaned-numeric.xlsx"

# Clean numeric columns
echo "Cleaning numeric columns..."
python3 <<EOF
import pandas as pd
import numpy as np

df = pd.read_excel("$TMP_CLEANED_XLSX")

# Handle non-finite values in 'Total Deaths'
df['Total Deaths'] = pd.to_numeric(df['Total Deaths'], errors='coerce')
df['Total Deaths'].fillna(df['Total Deaths'].median(), inplace=True)

df['Ranking'] = pd.to_numeric(df['Ranking'], errors='coerce').fillna(0).astype(int)

# Clean 'Calendar Year' column
def clean_calendar_year(year):
    try:
        return int(year)
    except ValueError:
        return np.nan

df['Calendar Year'] = df['Calendar Year'].apply(clean_calendar_year)
df.dropna(subset=['Calendar Year'], inplace=True)
df['Calendar Year'] = df['Calendar Year'].astype(int)

df.to_excel("$TMP_CLEANED_NUMERIC_XLSX", index=False)
EOF
echo "Numeric columns cleaned."


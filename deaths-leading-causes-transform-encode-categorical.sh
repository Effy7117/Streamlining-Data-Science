#!/bin/bash

# Paths
TMP_CLEANED_NUMERIC_XLSX="/home/effy/deaths-leading-causes-cleaned-numeric.xlsx"
FINAL_CLEANED_XLSX="/home/effy/deaths-leading-causes-cleaned-output.xlsx"

# Encode categorical variables
echo "Encoding categorical variables..."
python3 <<EOF
import pandas as pd
from sklearn.preprocessing import LabelEncoder

df = pd.read_excel("$TMP_CLEANED_NUMERIC_XLSX")

# Label Encoding for 'Cause'
le = LabelEncoder()
df['Cause_Encoded'] = le.fit_transform(df['Cause'])

df.to_excel("$FINAL_CLEANED_XLSX", index=False)
EOF
echo "Categorical variables encoded."


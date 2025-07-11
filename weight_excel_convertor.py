#%%
import pandas as pd
import numpy as np
# Function to extract and standardize date from a column name
import re
from datetime import datetime

#%%

# Load the ODS file
file_path = "/mnt/c/Users/HMARTINEZ/Downloads/Mice and Citric Acid Weight Measurements (09.07.2025).ods"

# Use the third row (index 2) as header
df_clean = pd.read_excel(file_path, engine="odf", sheet_name="Mice weights", skiprows=2, nrows=12)
df_ca = pd.read_excel(file_path, engine="odf", sheet_name="Citric acid weight", skiprows=3, nrows=2)

# Extract the original column names for processing
original_columns = df_clean.columns
original_columns_ca = df_ca.columns

def extract_date(col_name):
    # Try to find a date in the format dd/mm/yyyy
    match = re.search(r'(\d{2}/\d{2}/\d{4})', col_name)
    if match:
        try:
            return datetime.strptime(match.group(1), '%d/%m/%Y').date().isoformat()
        except ValueError:
            return col_name  # Keep original if date parsing fails
    return col_name  # Non-date columns remain as they are

# Rename columns
df_clean.columns = [extract_date(col) for col in original_columns]
df_ca.columns = [extract_date(col) for col in original_columns_ca]


# Show preview of the cleaned DataFrame
print(df_clean.head())

print(df_ca.head())

# %%
# Drop the first two columns and assign the first row as the new header
df_clean = df_clean.drop(columns=df_clean.columns[:2])
# Reset the index
df_clean.reset_index(drop=True, inplace=True)
# assign the first row as the new header
df_clean.columns = df_clean.iloc[0]
df_clean = df_clean[1:]  # Remove the first row which is now the header
# Reset the index again
df_clean.reset_index(drop=True, inplace=True)
# Show the cleaned DataFrame
print(df_clean.head())

# %%
# for each of the column names, find if they contain a date in the format dd/mm/yyyy,
# and if so, convert it to yyyy-mm-dd format
def convert_date_format(col_name):
    try:
        match = re.search(r'(\d{2}/\d{2}/\d{4})', col_name)
        if match:
            try:
                date_obj = datetime.strptime(match.group(1), '%d/%m/%Y')
                return date_obj.strftime('%Y-%m-%d')
            except ValueError:
                return col_name  # Keep original if date parsing fails
        return col_name  # Non-date columns remain as they are
    except Exception:
        return "removeMe"
# Apply the date conversion to all column names
df_clean.columns = [convert_date_format(col) for col in df_clean.columns]
# Remove columns that were marked for removal
df_clean = df_clean.loc[:, ~df_clean.columns.str.contains('removeMe')]
# Reset the index again after cleaning
df_clean.reset_index(drop=True, inplace=True)
# Show the final cleaned DataFrame
print(df_clean.head())

# %%
# Remove columns with all NaN values
df_clean = df_clean.dropna(axis=1, how='all')
# remove rows where the name is NaN
df_clean = df_clean.dropna(subset=['Name'])
# Reset the index again after cleaning
df_clean.reset_index(drop=True, inplace=True)
# Show the final cleaned DataFrame
print(df_clean)

# save as a pickle file in this directory
df_clean.to_pickle("cleaned_weight_measurements.pkl")

# %%
# combine both rows of the citric acid weight DataFrame into a single row
df_ca_combined = df_ca.iloc[0].combine_first(df_ca.iloc[1])
df_ca_combined = pd.DataFrame([df_ca_combined])
# drop first column
df_ca_combined = df_ca_combined.drop(columns=df_ca_combined.columns[0])
#make the column names dates
df_ca_combined.columns = [convert_date_format(col) for col in df_ca_combined.columns]
# Reset the index
df_ca_combined.reset_index(drop=True, inplace=True)
# drop nans
df_ca_combined = df_ca_combined.dropna(axis=1, how='all')
# first entry to 600
df_ca_combined.iloc[0, 0] = 600

# turn this into consumption of CA by getting the diff
df_ca_combined = df_ca_combined.diff(axis=1).fillna(df_ca_combined.iloc[:, 0])
# make the entry of 2025-07-01 a nan value as it was change of bottle
change_of_bottle_dates = ['2025-07-01']
for date in change_of_bottle_dates:
    if date in df_ca_combined.columns:
        df_ca_combined[date] = np.nan

# Show the combined DataFrame
print(df_ca_combined)
# %%
# Save the combined DataFrame to a pickle file
df_ca_combined.to_pickle("cleaned_citric_acid_weight.pkl")

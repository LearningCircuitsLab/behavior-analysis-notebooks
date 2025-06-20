#%%
import pandas as pd
# Function to extract and standardize date from a column name
import re
from datetime import datetime

# Load the ODS file
file_path = "/mnt/c/Users/HMARTINEZ/Downloads/Weight Measurements (30.05.2025).ods"

# Use the third row (index 2) as header
df_clean = pd.read_excel(file_path, engine="odf", sheet_name=0, skiprows=2, nrows=12)

# Extract the original column names for processing
original_columns = df_clean.columns

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

# Show preview of the cleaned DataFrame
print(df_clean.head())

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

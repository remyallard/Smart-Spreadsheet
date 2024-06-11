import pandas as pd

# Read the Excel file into a DataFrame
filename = './tests/example_2.xlsx'
data = pd.read_excel(filename, sheet_name="Analysis Output")

# Initialize variables to store extracted tables
tables = []
start_row = None

# Iterate through rows
for idx, row in data.iterrows():
    # Check if all values in the row are NaN (empty)
    if row.isnull().all():
        # If start_row is not None, it means it's the end of a table
        if start_row is not None:
            tables.append(data.iloc[start_row:idx].copy())
            start_row = None
    # If start_row is None and the row is not empty, it's the start of a new table
    elif start_row is None:
        start_row = idx

# If there's a start_row without an end, append the remaining rows as the last table
if start_row is not None:
    tables.append(data.iloc[start_row:].copy())

# Remove empty columns and rows from each table
for i, table in enumerate(tables):
    # Drop empty columns
    table = table.dropna(axis=1, how='all')
    
    # Drop empty rows
    table = table.dropna(axis=0, how='all')

    tables[i] = table

# Combine all the DataFrames into a single string
combined_string = ""
for i, table in enumerate(tables, 1):
    combined_string += f"Table {i}:\n"
    combined_string += table.to_string(index=False)
    combined_string += "\n\n"

# Print the combined string
print(combined_string)

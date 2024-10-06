import pandas as pd

# Load the CSV file
file_path = '/Users/ahila/Desktop/fit3179/data/csv/Income VIC.csv' # Replace with the path to your CSV file
data = pd.read_csv(file_path)

# Identifying columns with "median" and "average" that need to be converted
income_columns = [col for col in data.columns if '$' in col.lower() or 'individuals' in col.lower()]

# Remove commas and convert the data in these columns to integers
for col in income_columns:
    data[col] = data[col].replace(',', '', regex=True).astype(int)

# Save the cleaned data back to the same CSV file
data.to_csv(file_path, index=False)

print(f"Data cleaned and saved to {file_path}")



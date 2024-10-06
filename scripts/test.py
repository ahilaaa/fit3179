

import pandas as pd

# Load the CSV file
file_path = '/Users/ahila/Desktop/fit3179/data/csv/vic$ strings copy.csv'  # replace with your actual file path
df = pd.read_csv(file_path)

# Remove all quotation marks from the header row
df.columns = df.columns.str.replace('"' , '')

# Save the modified DataFrame to a new CSV file
modified_file_path = 'modified_file.csv'  # replace with your desired output path
df.to_csv(modified_file_path, index=False)

print("Quotation marks removed from the header row and saved to", modified_file_path)



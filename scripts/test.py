import pandas as pd
import json

# Load cleaned JSON and CSV files
json_file = 'victoria.json'  # Use your actual JSON file path
csv_file = 'Income VIC.csv'  # Use your actual CSV file path

# Function to clean suburb names
def clean_suburb_name(suburb):
    if suburb:
        return suburb.strip().upper()  # Ensure consistent cleaning
    return None

# Load and clean JSON file
with open(json_file, 'r') as f:
    vic_data = json.load(f)

# Clean suburb names from JSON file
vic_suburbs_json = [clean_suburb_name(feature['properties']['vic_loca_2']) for feature in vic_data['objects']['suburb-2-vic']['geometries']]

# Load and clean CSV file
vic_suburbs_csv = pd.read_csv(csv_file)
vic_suburbs_csv['suburb_cleaned'] = vic_suburbs_csv['suburb'].apply(clean_suburb_name)

# Convert both lists to sets for easier comparison
json_suburbs_set = set(vic_suburbs_json)
csv_suburbs_set = set(vic_suburbs_csv['suburb_cleaned'])

# Find matching suburbs
matching_suburbs = json_suburbs_set.intersection(csv_suburbs_set)
non_matching_json = json_suburbs_set - csv_suburbs_set
non_matching_csv = csv_suburbs_set - json_suburbs_set

# Print the number of matching and non-matching suburbs
print(f"Number of matching suburbs: {len(matching_suburbs)}")
print(f"Number of suburbs in JSON but not in CSV: {len(non_matching_json)}")
print(f"Number of suburbs in CSV but not in JSON: {len(non_matching_csv)}")

# Optionally, print the actual suburbs that don't match
#print("\nSuburbs in JSON but not in CSV:", non_matching_json)
#print("\nSuburbs in CSV but not in JSON:", non_matching_csv)

# Filter the CSV data for matching suburbs and check if income data is missing
matched_suburbs = vic_suburbs_csv[vic_suburbs_csv['suburb_cleaned'].isin(matching_suburbs)]
missing_income = matched_suburbs[matched_suburbs['median3 taxable income 2021-22$'].isna()]

print(f"Number of matched suburbs with missing income data: {len(missing_income)}")
print(missing_income[['suburb_cleaned', 'median3 taxable income 2021-22$']])





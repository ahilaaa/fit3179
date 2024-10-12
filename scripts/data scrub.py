import pandas as pd

# AGGREGATE BY COUNCIL : income, obesity rates, fast food location density

# Paths to the CSV files
file1_path = "/Users/ahila/Desktop/fit3179/data/csv/FastFood/Merged/Suburb Obesity Income FastFood.csv"

df_obesity = pd.read_csv(file1_path)

# numeric data is represented as "23,344" thanks to the ATO, we must clean and strip
df_obesity['Individuals 2021-22'] = pd.to_numeric(df_obesity['Individuals 2021-22'].str.replace(',', ''), errors='coerce')
df_obesity['Median taxable income 2021-22'] = pd.to_numeric(df_obesity['Median taxable income 2021-22'].str.replace(',', ''), errors='coerce')
df_obesity['Average taxable income 2021-22'] = pd.to_numeric(df_obesity['Average taxable income 2021-22'].str.replace(',', ''), errors='coerce')


merged_df = df_obesity.groupby('council').agg({
    'Individuals 2021-22': 'mean' ,
    'Median taxable income 2021-22': 'mean' ,
    'Average taxable income 2021-22': 'mean',
    'Adults - Obesity - ASR': 'first',
    'Adults - Overweight/Obese - ASR': 'first',
    'KFC Count': 'sum',
    "McDonald's Count": 'sum',
    "Hungry Jack's Count": 'sum',
    "Total Fast Food Count": 'sum',
}).reset_index()

# Round all numeric columns to integers
merged_df[['Individuals 2021-22', 'Median taxable income 2021-22', 'Average taxable income 2021-22']] = merged_df[['Individuals 2021-22', 'Median taxable income 2021-22', 'Average taxable income 2021-22']].round(0)

merged_df.to_csv('/Users/ahila/Desktop/fit3179/data/csv/FastFood/Merged/Merged Council.csv', index=False)





'''
# MAKE COUNCIL OBESITY FAST FOOD COUNTS

# Paths to the CSV files
file1_path = "/Users/ahila/Desktop/fit3179/data/csv/FastFood/Merged/Suburb Obesity Income FastFood.csv"

df_obesity = pd.read_csv(file1_path)

merged_df = df_obesity.groupby('council').agg({
    'KFC Count': 'sum',
    "McDonald's Count": 'sum',
    "Hungry Jack's Count": 'sum',
    "Total Fast Food Count": 'sum',
    'Adults - Obesity - ASR': 'first',
    'Adults - Overweight/Obese - ASR': 'first'
}).reset_index()

merged_df.to_csv('/Users/ahila/Desktop/fit3179/data/csv/FastFood/Merged/Council Obesity FastFood.csv', index=False)'''






'''
data = pd.read_csv("/Users/ahila/Desktop/fit3179/data/csv/FastFood/Merged/Council Obesity FastFood.csv")

# Add a new column for Total Fast Food Count
data['Total Fast Food Count'] = data['KFC Count'] + data["McDonald's Count"] + data["Hungry Jack's Count"]

data.to_csv("/Users/ahila/Desktop/fit3179/data/csv/FastFood/Merged/Council Obesity FastFood.csv", index=False)'''



'''
COMBINE EVERYTHING TOGETHER !!! BIG BOI COMBINATION FILE

# for every suburb, retrieve corresponding income information
#  and fast food count ( /Users/ahila/Desktop/fit3179/data/csv/FastFood/Merged/Merged Income FastFood.csv)

# Load the CSV files
obesity_file = '/Users/ahila/Desktop/fit3179/data/csv/Obesity/Merged/Obesity Council Suburb.csv'  # Replace with actual file path
income_fastfood_file = '/Users/ahila/Desktop/fit3179/data/csv/FastFood/Merged/Merged Income FastFood.csv'  # Replace with actual file path

# Read both CSVs
obesity_data = pd.read_csv(obesity_file)
income_fastfood_data = pd.read_csv(income_fastfood_file)

# Merge the two dataframes on the 'suburb' column
merged_data = pd.merge(obesity_data, income_fastfood_data, on='suburb', how='left')


# Remove duplicate suburb entries
merged_data = merged_data.drop_duplicates(subset='suburb')

# Add a new column for Total Fast Food Count
merged_data['Total Fast Food Count'] = merged_data['KFC Count'] + merged_data["McDonald's Count"] + merged_data["Hungry Jack's Count"]


# Save the cleaned data to a new CSV
output_file = '/Users/ahila/Desktop/fit3179/data/csv/FastFood/Merged/Suburb Obesity Income FastFood.csv'  # Replace with desired output path
merged_data.to_csv(output_file, index=False)

print(f"Cleaned merged data saved to {output_file}")'''






'''

# Load the two CSV files
vic_table_df = pd.read_csv('/Users/ahila/Desktop/fit3179/data/csv/Obesity/Vic-Table 1.csv')
suburbs_vic_full_df = pd.read_csv('data/csv/Suburbs/Suburbs VIC Full.csv')

# Normalize 'LGA' and 'lgaregion' values for consistency
vic_table_df['lga'] = vic_table_df['lga'].str.strip().str.lower()
suburbs_vic_full_df['lgaregion'] = suburbs_vic_full_df['lgaregion'].str.strip().str.lower()

# Perform the merge using the normalized 'LGA' and 'lgaregion' columns
merged_df = suburbs_vic_full_df.merge(vic_table_df, left_on='lgaregion', right_on='lga', how='left')

# Convert the 'suburb' column to uppercase
merged_df['suburb'] = merged_df['suburb'].str.upper()

# Capitalize the first letter of every word in 'lgaregion'
merged_df['lgaregion'] = merged_df['lgaregion'].str.title()

# Select the desired columns, including 'LGA', 'suburb', and 'Adults - Obesity - ASR'
result_columns = ['lgaregion', 'suburb', 'Adults - Obesity - ASR','Adults - Overweight/Obese - ASR' ]
result_df = merged_df[result_columns]

# Save the result to a new CSV file
result_df.to_csv('/Users/ahila/Desktop/fit3179/data/csv/Obesity/Merged/Obesity Council Suburb.csv', index=False)'''


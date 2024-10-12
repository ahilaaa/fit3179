import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import ssl
import certifi



def initialize_geolocator():
    """
    Initialize the geolocator with SSL context using certifi for verification.
    Nonatim is geocoder service provided by OpenStreetMap
    return: geolocator object
    """
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    return Nominatim(user_agent="geoapi", ssl_context=ssl_context)



def get_suburb(latitude, longitude, geolocator):
    """
    Retrieve the suburb for a given latitude and longitude using the geolocator.
    """
    try:
        location = geolocator.reverse((latitude, longitude), exactly_one=True, timeout=10)
        if location:
            address = location.raw.get('address', {})
            suburb = address.get('suburb') or address.get('neighbourhood') or address.get('town') or address.get('city')
            print(suburb)
            return suburb
    except (GeocoderTimedOut, GeocoderUnavailable):
        return None

def process_file(input_file):
    """
    Process the given CSV file to add suburb information based on latitude and longitude.
    """
    # Load data
    data = pd.read_csv(input_file)
    
    # Initialize geolocator
    geolocator = initialize_geolocator()
    
    # Apply the function to each row and add the 'Suburb' column
    data['Suburb'] = data.apply(lambda row: get_suburb(row['Latitude'], row['Longitude'], geolocator), axis=1).str.upper()
    
    # Save the updated data back to the input file
    data.to_csv(input_file, index=False)
    print(f"Updated data saved to {input_file}")





def add_fast_food_count(income_data_path, fast_food_data_path, output_data_path,fast_food_name):
    
    # Load the data
    fast_food_data = pd.read_csv(fast_food_data_path)

    income_data = pd.read_csv(income_data_path)
    
    # Count the number of fast food locations per suburb
    fast_food_counts = fast_food_data['Suburb'].value_counts().reset_index()
    fast_food_counts.columns = ['suburb', f'{fast_food_name} Count']
    
    # Merge the counts with the income data on suburb names
    income_data_with_fast_food = pd.merge(income_data, fast_food_counts, on='suburb', how='left')
    
    # Fill NaN values in the count column with 0 (for suburbs without any fast food locations)
    income_data_with_fast_food[f'{fast_food_name} Count'] = income_data_with_fast_food[f'{fast_food_name} Count'].fillna(0).astype(int)
    
    income_data_with_fast_food.to_csv(output_data_path, index=False)
    print(f"Updated income data saved to: {output_data_path}")




'''
# merging for obestiy rates by council
data = pd.read_csv("/Users/ahila/Desktop/fit3179/data/csv/FastFood/Merged/Council Obesity FastFood.csv")

# Add a new column for Total Fast Food Count
data['Total Fast Food Count'] = data['KFC Count'] + data["McDonald's Count"] + data["Hungry Jack's Count"]

data.to_csv("/Users/ahila/Desktop/fit3179/data/csv/FastFood/Merged/Council Obesity FastFood.csv", index=False)'''



# FOR EACH COUNCIL in Vic-Table 1 -> retrieve list of all suburbs and make long format
# check council Vic-Table-1 exists for Suburbs VIC Full


import pandas as pd

'''
# Paths to the CSV files
file1_path = "/Users/ahila/Desktop/fit3179/data/csv/FastFood/Merged/Suburb Obesity FastFood.csv"
file2_path = "/Users/ahila/Desktop/fit3179/data/csv/FastFood/Merged/Merged Income FastFood.csv"

df_obesity = pd.read_csv(file1_path)
df_income_fastfood = pd.read_csv(file2_path)

# Select the necessary columns from the obesity dataframe, including "suburb", "Adults - Obesity Rate", and "council"
df_obesity = df_obesity[['Adults - Obesity Rate', 'council', 'suburb',"KFC Count" ,"McDonald's Count","Hungry Jack's Count"]]

# Merge the dataframes on the "suburb" column
merged_df = pd.merge(df_obesity, df_income_fastfood,on="suburb", how="inner")

# aggregate fast food counts by council (add up all suburbs)
# Group by the "council" column and sum up "KFC Count" and "McDonald's Count"
merged_df = merged_df.groupby('council_x').agg({
    'KFC Count_x': 'sum',
    "McDonald's Count_x": 'sum',
    "Hungry Jack's Count_x": 'sum',
    'Adults - Obesity Rate': 'first'
}).reset_index()

merged_df.to_csv('/Users/ahila/Desktop/fit3179/data/csv/FastFood/Merged/Council Obesity FastFood.csv', index=False)'''







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
result_df.to_csv('/Users/ahila/Desktop/fit3179/data/csv/Obesity/Merged/Obesity Council.csv', index=False)'''


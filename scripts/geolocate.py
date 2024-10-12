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





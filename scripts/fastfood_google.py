import requests
import csv
from get_suburbs import SUBURB_NAMES
import pandas as pd


# Function to fetch a page of results from the Places API
def get_request(query, suburb, next_page_token=None): # text search with "fast food restaurant" + suburb
    params = {
        "query": query +" " +suburb,
        "key": API_KEY
    }
    if next_page_token:
        params["pagetoken"] = next_page_token
    response = requests.get("https://maps.googleapis.com/maps/api/place/textsearch/json", params=params)
    return response.json()



# Function to fetch all pages 
def extend_results(query, suburb):
    results = []
    next_page_token = None

    while True:
        result = get_request(query, suburb, next_page_token)
        if "results" in result:
            results.extend(result["results"])
        next_page_token = result.get("next_page_token", None)
        if not next_page_token:
            break
        #time.sleep(2)  # Google recommends a short delay before the next request
    return results



# Main function to retrieve results from google API based on query and fast food restaurant
def get_results(query):
    results = []

    for suburb_name in SUBURB_NAMES:
        print(f"Searching {suburb_name}")
        results += extend_results(query, suburb_name)  # retrieve 60 results instead of 2

    return results


# Function to remove duplicate entries based on latitude and longitude
def remove_duplicates(locations):
    unique_locations = {}
    for place in locations:
        lat_lng_key = (place["geometry"]["location"]["lat"], place["geometry"]["location"]["lng"])
        if lat_lng_key not in unique_locations:
            unique_locations[lat_lng_key] = place
    return list(unique_locations.values())



# Function to save the locations to a CSV file
def save_to_csv(results, filename, query):
    with open(filename, mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Latitude", "Longitude"])
        for data in results:
            #print(data.get("name"))
            writer.writerow([
                data.get("name"),
                data["geometry"]["location"]["lat"],
                data["geometry"]["location"]["lng"]
            ])


# since we are searching by suburb name, sometimes we retrieve data from other countries with similarly named suburbs
def keep_australian_results(filename):

    df = pd.read_csv(filename)

    # Victoria boundaries (approximate)
    lat_min, lat_max = -39.2, -33.9  # Latitude range for Victoria
    lng_min, lng_max = 140.96, 150.0  # Longitude range for Victoria

    # Filter the dataframe to keep only entries within Victoria
    vic_df = df[(df['Latitude'] >= lat_min) & (df['Latitude'] <= lat_max) & 
                (df['Longitude'] >= lng_min) & (df['Longitude'] <= lng_max)]

    # Save the filtered dataframe
    vic_df.to_csv(filename, index=False)





# Main execution
if __name__ == "__main__":
    # Replace with your Google API Key
    API_KEY = 'AIzaSyC0LEXboOhkj7MANJpXMUlM4EhdHXtv0uA'
    
    fast_food = ["KFC", "Hungry Jacks", "McDonald's"]

    center_lat = -37.8136 # center of Melbourne
    center_lng = 144.9631

    # get fast food locations for every suburb
    for query in fast_food:
   
        locations = get_results(query)
        print(f"Total {query} locations found BEFORE : {len(locations)}")

        locations = remove_duplicates(locations)
        print(f"Total {query} locations found AFTER : {len(locations)}")
        # Save the results to a CSV file
        save_to_csv(locations, f"{query.replace(' ', '_')} Locations.csv", query)
        keep_australian_results(f"{query.replace(' ', '_')} Locations.csv", query)



         
          
            



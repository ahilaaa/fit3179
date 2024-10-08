import requests
import csv
import pandas as pd




# fetch a page of results from Google Maps API

def get_results(query):
    results = []

    testing = 0

    vic_data = pd.read_csv("/Users/ahila/Desktop/fit3179/data/csv/Suburbs VIC.csv")

    for suburb_name in vic_data["suburb"]:
        print(f"Searching {suburb_name}")
        params = {
            "query": query + " " + suburb_name,
            "key": API_KEY
        }
        response = requests.get("https://maps.googleapis.com/maps/api/place/textsearch/json", params=params)
        places = response.json().get("results", [])

        valid_places = []

        for place in places:
            # Check if the place is permanently closed
            if place.get("business_status") == "CLOSED_PERMANENTLY":
                continue  # Skip 

            # Check if the place name contains the query (case-sensitive)
            place_name = place.get("name", "")
            if query not in place_name:
                continue  # Skip
            
            valid_places.append(place)
        results += valid_places

        '''testing += 1
        
        if testing == 4:
            #return results'''
        
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
def save_to_csv(results, filename):
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
def keep_vic_results(filename):

    df = pd.read_csv(filename)

    # Victoria boundaries (approximate)
    lat_min, lat_max = -39.2, -33.9  # Latitude range for Victoria
    lng_min, lng_max = 140.6, 150.3  # Longitude range for Victoria

    # Filter the dataframe to keep only entries within Victoria
    vic_df = df[(df['Latitude'] >= lat_min) & (df['Latitude'] <= lat_max) & 
                (df['Longitude'] >= lng_min) & (df['Longitude'] <= lng_max)]


    # Save the filtered dataframe
    vic_df.to_csv(filename)




# Main execution
if __name__ == "__main__":
    # Replace with your Google API Key
    API_KEY = 'AIzaSyC0LEXboOhkj7MANJpXMUlM4EhdHXtv0uA'
    
    #fast_food = ["KFC", "Hungry Jack's", "McDonald's"]

    fast_food = ["McDonald's"] #, "KFC", "Hungry Jack's"]


    # get fast food locations for every suburb
    for query in fast_food:
   
        locations = get_results(query)
        print(f"Total {query} locations found BEFORE : {len(locations)}")

        locations = remove_duplicates(locations)
        print(f"Total {query} locations found AFTER : {len(locations)}")

        # Save the results to a CSV file
        filename = query + " Locations.csv"
        save_to_csv(locations, filename)
        
        keep_vic_results(filename)



         
          
            



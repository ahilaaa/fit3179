import requests
import csv


## DEFINING CONSTANTS

# source: https://www.onlymelbourne.com.au/list-of-melbourne-suburbs

SUBURB_NAMES = [
    "Carlton", "Carlton South", "Carlton North", "Docklands", "East Melbourne", "Jolimont", "Flemington",
    "Kensington", "Melbourne", "North Melbourne", "Hotham Hill", "Macaulay", "Parkville", "Royal Park", 
    "Port Melbourne", "Fishermans Bend", "Southbank", "South Wharf", "South Yarra", "West Melbourne", 
    "Coode Island", "Albert Park", "Balaclava", "Elwood", "Brighton Road", "Albert Park Barracks", 
    "Middle Park", "Beacon Cove", "Garden City", "Sandridge", "Ripponlea", "St Kilda", "St Kilda South", 
    "St Kilda East", "St Kilda West", "St Kilda Junction", "South Melbourne", "City Road", "Emerald Hill", 
    "Montague", "Abbotsford", "Victoria Park", "Alphington", "Burnley", "Clifton Hill", "Collingwood", 
    "Collingwood North", "Cremorne", "Richmond East", "Fitzroy", "Eastern Hill", "Fitzroy South", "Fitzroy North", 
    "Princes Hill", "Richmond", "Burnley North", "North Richmond", "Richmond South", "Victoria Gardens", 
    "West Richmond", "Bellfield", "Briar Hill", "Bundoora", "Eaglemont", "Eltham", "Eltham North", 
    "Greensborough", "Apollo Parkways", "Grace Park", "Green Hills", "Heidelberg", "Heidelberg Heights", 
    "Heidelberg North", "Heidelberg West", "Ivanhoe", "Darebin", "Fairy Hills", "Ivanhoe North", "Ivanhoe East", 
    "Lower Plenty", "Macleod", "Mont Park", "Macleod West", "Montmorency", "Rosanna", "Banyule", "St Helena", 
    "Viewbank", "Rosanna East", "Watsonia", "Watsonia North", "Yallambie", "Kingsbury", "Northcote", "Croxton", 
    "Dennis", "Merri", "Preston", "Reservoir", "Ruthven", "Summerhill", "Thornbury", "Attwood", "Broadmeadows", 
    "Campbellfield", "Coolaroo", "Craigieburn", "Dallas", "Gladstone Park", "Greenvale", "Jacana", 
    "Melbourne Airport", "Roxburgh Park", "Somerton", "Sunbury", "Bulla", "Clarkefield", "Diggers Rest", 
    "Kalkallo", "Mickleham", "Oaklands Junction", "Wildwood", "Yuroke", "Aberfeldie", "Airport West", 
    "Ascot Vale", "Avondale Heights", "Essendon", "Essendon Fields", "Essendon North", "Essendon West", 
    "Flemington", "Keilor East", "Moonee Ponds", "Niddrie", "Strathmore", "Strathmore Heights", "Travancore", 
    "Brunswick", "Brunswick East", "Brunswick West", "Coburg", "Coburg North", "Fawkner", "Glenroy", 
    "Gowanbrae", "Hadfield", "Oak Park", "Pascoe Vale", "Pascoe Vale South", "Diamond Creek", "Eltham North", 
    "Greensborough", "Hurstbridge", "North Warrandyte", "Research", "Wattle Glen", "Bend of Islands", 
    "Christmas Hills", "Cottles Bridge", "Doreen", "Kangaroo Ground", "Kinglake", "Nutfield", "Panton Hill", 
    "Plenty", "St Andrews", "Smiths Gully", "Strathewen", "Watsons Creek", "Yarrambat", "Epping", "Lalor", 
    "Mernda", "Mill Park", "South Morang", "Thomastown", "Yan Yean", "Ashburton", "Balwyn", "Balwyn North", 
    "Camberwell", "Canterbury", "Deepdene", "Glen Iris", "Hawthorn", "Hawthorn East", "Kew", "Kew East", 
    "Mont Albert", "Surrey Hills", "Boronia", "Ferntree Gully", "Knoxfield", "Lysterfield", "Rowville", 
    "Scoresby", "The Basin", "Wantirna", "Wantirna South", "Bulleen", "Doncaster", "Doncaster East", "Donvale", 
    "Park Orchards", "Templestowe", "Templestowe Lower", "Warrandyte", "Wonga Park", "Croydon", "Croydon Hills", 
    "Heathmont", "Ringwood", "Ringwood East", "Ringwood North", "Warranwood", "Blackburn", "Blackburn North", 
    "Blackburn South", "Box Hill", "Box Hill North", "Box Hill South", "Burwood", "Burwood East", "Forest Hill", 
    "Mitcham", "Nunawading", "Vermont", "Vermont South", "Belgrave", "Chirnside Park", "Lilydale", "Montrose", 
    "Mooroolbark", "Mount Evelyn", "Selby", "Tecoma", "Upwey", "Blairgowrie", "Capel Sound", "Dromana", 
    "McCrae", "Mornington", "Mount Eliza", "Mount Martha", "Portsea", "Rosebud", "Rye", "Safety Beach", 
    "Sorrento", "Tyabb", "Balnarring", "Somers", "Tootgarook", "Armadale", "Kooyong", "Malvern", "Malvern East", 
    "Prahran", "South Yarra", "Toorak", "Windsor", "Albanvale", "Albion", "Ardeer", "Cairnlea", "Calder Park", 
    "Deer Park", "Delahey", "Derrimut", "Hillside", "Kealba", "Keilor", "Keilor Downs", "Keilor East", 
    "Keilor Lodge", "Kings Park", "St Albans", "Sunshine", "Sydenham", "Taylors Lakes", "Altona", 
    "Altona Meadows", "Altona North", "Brooklyn", "Laverton", "Newport", "Seabrook", "Seaholme", "Williamstown", 
    "Braybrook", "Footscray", "Kingsville", "Maidstone", "Maribyrnong", "Seddon", "West Footscray", 
    "Yarraville", "Burnside", "Brookfield", "Caroline Springs", "Cobblebank", "Kurunjang", "Melton", 
    "Melton South", "Melton West", "Plumpton", "Ravenhall", "Rockbank", "Taylors Hill", "Weir Views", 
    "Truganina", "Werribee", "Werribee South", "Williams Landing", "Wyndham Vale", "Beaumaris", "Black Rock", 
    "Brighton", "Brighton East", "Cheltenham", "Gardenvale", "Hampton", "Hampton East", "Highett", 
    "Sandringham", "Carrum Downs", "Frankston", "Frankston North", "Frankston South", "Langwarrin", "Seaford", 
    "Bentleigh", "Bentleigh East", "Caulfield", "Carnegie", "Elsternwick", "Glen Huntly", "McKinnon", 
    "Murrumbeena", "Ormond", "Aspendale", "Aspendale Gardens", "Bonbeach", "Carrum", "Chelsea", 
    "Chelsea Heights", "Clarinda", "Clayton", "Edithvale", "Heatherton", "Mentone", "Mordialloc", 
    "Patterson Lakes", "Waterways", "Ashwood", "Burwood", "Chadstone", "Clayton", "Glen Waverley", 
    "Hughesdale", "Huntingdale", "Monash University", "Mount Waverley", "Mulgrave", "Notting Hill", 
    "Oakleigh", "Wheelers Hill", "Officer", "Pakenham", "Emerald", "Bunyip", "Cockatoo", "Garfield", 
    "Koo Wee Rup", "Lang Lang", "Nar Nar Goon", "Tooradin", "Clyde", "Cranbourne", "Doveton", 
    "Endeavour Hills", "Hallam", "Hampton Park", "Lynbrook", "Narre Warren", "Warneet", "Dandenong", 
    "Dandenong North", "Dandenong South", "Keysborough", "Noble Park", "Springvale", "Carrum Downs", 
    "Skye", "Langwarrin South", "Bangholme"
]






API_KEY = 'AIzaSyC0LEXboOhkj7MANJpXMUlM4EhdHXtv0uA'

def get_suburb_coordinates():
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    suburbs_coordinates = {}

    for suburb in SUBURB_NAMES:
        params = {
            'address': f'{suburb}, Victoria, Australia',
            'key': API_KEY
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                location = data['results'][0]['geometry']['location']
                latitude = location['lat']
                longitude = location['lng']
                coordinates = f"{latitude},{longitude}"
                suburbs_coordinates[suburb] = coordinates
            else:
                print(f"No results found for {suburb}")
        else:
            print(f"Error fetching data for {suburb}: {response.status_code}")
    
    return suburbs_coordinates




def to_csv(suburbs_coordinates, output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(["Suburb Name", "Coordinates"]) # next time get

        # Write data rows
        for suburb, coordinates in suburbs_coordinates.items():
            writer.writerow([suburb, coordinates])



# Function to fetch a page of results from the Places API
def get_request(query, location, radius, next_page_token=None):
    params = {
        "query": query,
        "location": location,
        "radius": radius,
        "key": API_KEY
    }
    if next_page_token:
        params["pagetoken"] = next_page_token
    response = requests.get("https://maps.googleapis.com/maps/api/place/textsearch/json", params=params)
    return response.json()



# Function to fetch all pages for a specific grid point
def get_locations(query, location, radius):
    locations = []
    next_page_token = None
    while True:
        result = get_request(query, location, radius, API_KEY, next_page_token)
        if "results" in result:
            locations.extend(result["results"])
        next_page_token = result.get("next_page_token", None)
        if not next_page_token:
            break
        #time.sleep(2)  # Google recommends a short delay before the next request
    return locations






# Main execution
if __name__ == "__main__":
    # Replace with your Google API Key

    # Get the suburb coordinates
    suburb_coordinates = get_suburb_coordinates()

    # Write the results to a CSV file
    to_csv(suburb_coordinates)



    
    


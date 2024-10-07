import pandas as pd
from geopy.geocoders import Nominatim
import time
import googlemaps




def geolocation_search_refinement(csv_file,count):
    
    # Read the file using pandas
    df_initial = pd.read_csv(csv_file)

    # Iterate through the dataframe and ignore the ones with geolocations found
    for index, row in df_initial[count:].iterrows():

        # Define the variables
        address = row['FullAddress']
        geolocation_status = row['GeolocationFound']
        x_coordinate = row['X_Coordinate']
        y_coordinate = row['Y_Coordinate']

        # Check if geolocation is missing
        if geolocation_status == 0:
            continue
        else:
            print("-------------------------------------------------")
            print(f"GEOLOCATION PREVIOUS ATTEMPT: {index}")
            print(f"{address}\n{geolocation_status}\n{x_coordinate}\n{y_coordinate}")

            geocode_result = gmaps.geocode(address)
            
            # Check if the Google Maps API was found      
            if geocode_result:      
                print(f"GEOLOCATION REFINED ATTEMPT: {index}")
                location = geocode_result[0]['geometry']['location']
                new_x_coordinate = location['lat']
                new_y_coordinate = location['lng']
                df_initial.loc[index,'GeolocationFound'] = 0
                df_initial.loc[index,'X_Coordinate'] = new_x_coordinate
                df_initial.loc[index,'Y_Coordinate'] = new_y_coordinate
                print(f"{address}\n{0}\n{new_x_coordinate}\n{new_y_coordinate}")
            
            else:
                print("STILL MISSING")

        # Move it to the csv file
        df_initial.to_csv(csv_file,index=False)

                  










# Outset
if __name__ == "__main__":

    # Enable google maps
    google_api_file = "/Users/damiamalfaro/Desktop/google_api.txt"
    with open(google_api_file, "r") as file:
        google_api_key = file.readlines() 

    gmaps = googlemaps.Client(key=google_api_key[0])

    # Activate Geolocator
    geolocator = Nominatim(user_agent="my-app", timeout=24)

    # Access the file
    locations_file = "/Users/damiamalfaro/Desktop/Europe/testing_wesonder/Geolocations_DIR_Entities/file_entity_conversion_bottom.csv"

    # Record current count
    current_count = 0

    # Refine the search of geolocations 
    geolocation_search_refinement(locations_file,current_count)

    





















































import pandas as pd
from geopy.geocoders import Nominatim
import time
import googlemaps




def geolocation_search_refinement(csv_file,count):
    
    # Read the file using pandas
    df_initial = pd.read_csv(csv_file)

    # Iterate through the dataframe and ignore the ones with geolocations found
    for index, row in df_initial[10:20].iterrows():

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
                location = geocode_result[0]['geometry']['location']
                new_x_coordinate = location['lat']
                new_y_coordinate = location['lng']
                df_initial.at[index,'X_Coordinate'] = new_x_coordinate
                df_initial.at[index,'Y_Coordinate'] = new_y_coordinate
                df_initial.to_csv(csv_file, index=False) 
            
            else:
                print("STILL MISSING")


                  

































# Outset
if __name__ == "__main__":

    # Enable google maps
    gmaps = googlemaps.Client(key="AIzaSyByyzK0B972uyHwhJ0ZD0CHdET0TjGgtN4")

    # Activate Geolocator
    geolocator = Nominatim(user_agent="my-app", timeout=24)

    # Access the file
    locations_file = "/Users/damiamalfaro/Desktop/Europe/testing_wesonder/geolocation_conversion/file_address_conversion_top.csv"
    # Refine the search of geolocations 
    geolocation_search_refinement(locations_file)

    




















































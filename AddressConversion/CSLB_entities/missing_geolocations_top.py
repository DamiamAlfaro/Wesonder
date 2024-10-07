import pandas as pd
import requests
import time

# Load the CSV file
file_path = '/Users/damiamalfaro/Desktop/Europe/testing_wesonder/Geolocations_CSLB_Entities/file_address_conversion_top.csv'
df = pd.read_csv(file_path)

# Google Maps API URL
api_url = 'https://maps.googleapis.com/maps/api/geocode/json'

# Your Google Maps API Key
api_key = 'AIzaSyAdgg_Tl2lEe1CAIQiEXQDbhXvc3taB0-I'

def get_coordinates(address):
    """Fetch latitude and longitude for a given address using Google Maps Geocoding API."""
    params = {
        'address': address,
        'key': api_key
    }
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
    return None, None

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    if row['X_Coordinate'] == 0 and row['Y_Coordinate'] == 0:
        address = row['FullAddress']
        lat, lng = get_coordinates(address)
        if lat and lng:
            # Update the DataFrame with the new coordinates
            df.at[index, 'X_Coordinate'] = lat
            df.at[index, 'Y_Coordinate'] = lng

            print(f"Current {index}\n{address}\n{lat}\n{lng}")
            
            # Save the updated CSV after each modification
            df.to_csv(file_path, index=False)
            
            # Sleep for a bit to avoid exceeding Google Maps API rate limits
            time.sleep(1)  # Adjust based on your usage and API limits

print("CSV file update complete!")

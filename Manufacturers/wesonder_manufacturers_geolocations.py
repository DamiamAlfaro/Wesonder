import pandas as pd
import requests
import time








'''
Store the geolocations into a new csv file
'''
def geolocations_into_csv(list_of_columns):

    # Assign column variables
    df = pd.DataFrame({
        'SpecNumber':[list_of_columns[0]],
        'SpecName':[list_of_columns[1]],
        'EntireSpec':[list_of_columns[2]],
        'SpecLink':[list_of_columns[3]],
        'ManufacturerName':[list_of_columns[4]],
        'ManufacturerLink':[list_of_columns[5]],
        'ManufacturerAddress':[list_of_columns[6]],
        'PhoneNumbers':[list_of_columns[7]],
        'Website':[list_of_columns[8]],
        'X_Coordinate':[list_of_columns[9]],
        'Y_Coordinate':[list_of_columns[10]]
    })

    # Append to csv file
    df.to_csv('refined_all_manufacturers.csv', mode='a', index=False, header=False)
    



'''
Using the address and free APIs, find geolocations
'''
def geolocation_attainment(address_string):
    base_url = "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress"
    params = {
        'address': address_string,
        'benchmark': 'Public_AR_Current',  # The benchmark is "Public Address Geocoding"
        'vintage': '4',    # Geocoding vintage
        'format': 'json'   # Format of the response
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        # Check if the API returned valid results
        if data.get("result") and data["result"].get("addressMatches"):
            match = data["result"]["addressMatches"][0]
            lat = match["coordinates"]["y"]
            lon = match["coordinates"]["x"]
            return lat, lon
        else:
            lat = 0
            lon = 0
            return lat, lon
        
    
    except Exception as e:
        print(f"Error geocoding address '{address_string}': {e}")
        lat = 0
        lon = 0
        return lat, lon




'''
Read the csv file containing all
manufacturer's as a dataframe
'''
def csv_to_dataframe_and_iterate(csv_file, count):
    
    # Do your thing mate
    df = pd.read_csv(csv_file)
    
    # Iterate through the file and acquire desired attributes of each row
    for index, row in df.iloc[count:].head(5).iterrows():
        spec_num = row["SpecNumber"]
        spec_name = row["SpecName"]
        entire_spec = row["EntireSpec"]
        spec_link = row["SpecLink"]
        manufacturer = row["ManufacturerName"]
        manufacturer_link = row["ManufacturerLink"]
        address = row["ManufacturerAddress"]
        phone_numbers = row["PhoneNumbers"]
        website = row["Website"]
        
        # Obtain the address geolocation
        print(f'Manufacturer: {manufacturer}')
        print(f'Address: {address}')
        geolocations = geolocation_attainment(address)
        x_coordinates = geolocations[0]
        y_coordinates = geolocations[1]
        print(f'Geolocation: {geolocations}')

        # Store into new csv file
        list_of_variables = [spec_num, 
                             spec_name,
                             entire_spec,
                             spec_link,
                             manufacturer,
                             manufacturer_link,
                             address,
                             phone_numbers,
                             website,
                             x_coordinates,
                             y_coordinates]
        geolocations_into_csv(list_of_variables)
        print(f'Iteration #{index} appended\n')


if __name__ == "__main__":
    
    # Manufacturer's csv file
    manufacturers_file = "all_manufacturers.csv"

    # Read the file and update count if needed
    count = 0
    csv_to_dataframe_and_iterate(manufacturers_file, count)



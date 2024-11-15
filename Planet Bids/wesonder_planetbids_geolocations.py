import pandas as pd
import requests
import os





'''
We will be storing the data into a csv file,
I know, I love csv files...
'''
def csv_file_appending(headers, content, csv_file, x_coord, y_coord):
    
    # Create the dataframe
    df = pd.DataFrame({
        headers[0]:[content[0]],
        headers[1]:[content[1]],
        headers[2]:[content[2]],
        headers[3]:[content[3]],
        headers[4]:[content[4]],
        headers[5]:[content[5]],
        headers[6]:[content[6]],
        headers[7]:[content[7]],
        headers[8]:[content[8]],
        headers[9]:[content[9]],
        headers[10]:[content[10]],
        headers[11]:[content[11]],
        headers[12]:[content[12]],
        headers[13]:[content[13]],
        'File':[csv_file],
        'X_Coordinates':[x_coord],
        'Y_Coordinates':[y_coord]
    })

    # Move to csv file
    df.to_csv('planetbids_geolocations/planetbids_geolocations.csv', mode='a', index=False, header=False)




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
We will be reading the csv files from the respective folder
where they are extract, and where the entities are found.
'''
def reading_the_csv_files(csv_file, file_number):
    
    # Do your thing
    df = pd.read_csv(csv_file)

    # Row number
    count = 0
    for index, row in df.iloc[count:].iterrows():

        # Locate the column headers and content
        columns_headers = []
        columns_contents = []
        for column in df.columns:
            columns_headers.append(column)
            columns_contents.append(row[column])

        # Retrieve the geolocations
        geolocations = geolocation_attainment(columns_contents[5])
        x_coordinate = geolocations[0]
        y_coordinate = geolocations[1]

        # Append to csv file
        csv_file_appending(columns_headers,columns_contents,csv_file,x_coordinate,y_coordinate)
        print(f'Entity #{index}: {columns_contents[0]} - Appended\nFile #{file_number}: {csv_file}\nCoordinates: {geolocations}\n')













if __name__ == "__main__":

    # Initiate the iteration
    folder = 'planetbids_entities/'
    folder_files = os.listdir(folder)
    folder_files.sort()
    
    # File number
    count = 0 
    for file in range(count, len(folder_files)):
        reading_the_csv_files(f'{folder}{folder_files[file]}', file)

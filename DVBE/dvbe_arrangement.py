import pandas as pd
import requests
from pathlib import Path
from geopy.geocoders import Nominatim #type: ignore




'''
Using the Address Line1, Address Line2, City, State, and Postal code,
we will create a new column containing all those attributes in a single
cell value in order to use that cell value to find the respective geolocation
further on.
'''
def complete_address_column_creation(csv_file):
    
    # Read the file, covert it to a DataFrame using pandas, then locate
    # the five columns that contain the CompleteAddress attribute, concatenate
    # them together, and create a new column containing the result of the
    # adjunction. One can locate the five columns using the itterrows() 
    # functionality which works efficiently for dataframes.

    df = pd.read_csv(csv_file,low_memory=False)
    
    df['CompleteAddress'] = df['CompleteAddress'].astype(str)

    for index, row in df.iterrows():
        
        # This is where we locate each column by pinpointing it using
        # the title of each column respectively. Each column contains an
        # attribute of the complete address.

        address_line1 = str(row['AddressLine1']).title()
        address_line2 = str(row['AddressLine2']).title()
        city = str(row['City']).title()
        state = row['State']

        # Some of the zip codes contain more than five digits, including a
        # '-' character. Let's remove them since they sometimes alter the 
        # posibility of finding the correct address in question.

        zip_code = str(row['PostalCode'])

        if '-' in zip_code:
            zip_code_split = zip_code.split('-')
            zip_code = zip_code_split[0]

        # Some of the columns cells under 'AddressLine2' are empty, therefore
        # useless. We can build a if statement to apply the address line 2 if
        # applicable, and dismiss it if non-applicable.

        if df.isnull().loc[index,'AddressLine2']:
            complete_address = f'{address_line1}, {city}, {state} {zip_code}'
        
        else:
            complete_address = f'{address_line1}, {address_line2}, {city}, {state} {zip_code}'
        
        # Now, it is time to allocate the complete address string into its new
        # column, 'CompleteAddress'. We will do this individually with each of the
        # cells along the dataframe.

        df.at[index,'CompleteAddress'] = complete_address
    
    # Once all the complete addresses have been iterated to their respective column,
    # we need to export the dataframe into a csv file for future usage. After that, we
    # will jump to step 2: Geolocation Acquisition.
    
    df.to_csv('refined_latest_dvbe.csv',index=False)
        



'''
Geolocations are great. We will obtain the geolocations, extract them,
allocate them into the file, cleanse it, and then concatenate the file with the previously
one.
'''
def obtaining_new_geolocations_attempt1(address_string):
    
    # To start off, we need to import the Geolocation functionality. Once imported, we
    # will iterate through the new_cslb_entities.csv file and obtain the respective addresses.
    # There is a dilemma about the addresses withouth Geolocations, whether we discard them
    # or find an alternate solution to them. The only solution might be another Geolocation
    # library, but it depends on how many of them are not found.

    geolocation_source = "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress"
    params = {
        'address': address_string,
        'benchmark': 'Public_AR_Current', 
        'vintage': '4', 
        'format': 'json'
    }

    # We will attempt to find the geolocation based on the address string, if the
    # geolocation is not found, we will set it up to zeros. If it is found,
    # we will output the coordinates and correlate them to the parent function
    # in order to unite them with their file source.

    try:
        response = requests.get(geolocation_source, params=params)
        data = response.json()

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
Using Nominatim, we will try to find the addresses that were not found in the
first attempt, we can copy the same structure as the function above in order to
allow this function to be used within an iteration.
'''
def obtaining_new_geolocations_attempt2(address_string):
    
    # This is the second attempt to find an address using Nominatim. We will
    # be using the same methodology as with attempt 1; the output of this
    # function will either be a pair of zeros, or the geolocation
    # coordinates for each of the addressess.
    
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.geocode(address_string, timeout=8)

    if location:
        lat = location.latitude
        lon = location.longitude
        return lat, lon
    else:
        lat = 0
        lon = 0
        return lat, lon




'''
Utilizing two geocoders, U.S. Geocoder, and Nominatim, we will try to find all the
geocoordinates for each of the addresses. Using both will increase the chances of
finding geocoordinates, but they won't be absolute, which is why we will need a creative
way to find the geocoordinates for the remanining ones. 
'''
def geolocation_acquisition(csv_file):
    
    # First we need to import the respective csv file into our function, convert it into
    # a dataframe, and begin iteration within the file, in the iteration, we are looking
    # for the 'CompleteAddress' values, which we will use to feed the geolocation
    # finding functions. 

    main_df = pd.read_csv(csv_file, low_memory=False)

    for index, row in main_df.iterrows():

        percentage_progress = (round(index/len(main_df),4))*100
        
        complete_address = row['CompleteAddress']
        coordinates = obtaining_new_geolocations_attempt1(complete_address)
        x_coordinate = coordinates[0]
        y_coordinate = coordinates[1]

        # We need to check if the geocoordinates were found, to do so I recommend checking if
        # the coordinate (either X, or Y) is 0, which if you take a peek above, a zero represents
        # a failed acquisition. Regardless of which attempt was successful, if any, the result
        # will inevitably be allocated into the dataframe within the respective X and Y columns.

        if x_coordinate == 0 or y_coordinate == 0:
            second_attempt = obtaining_new_geolocations_attempt2(str(complete_address))
            x_coordinate = second_attempt[0]
            y_coordinate = second_attempt[1]
            main_df.at[index, 'X_Coordinates'] = x_coordinate
            main_df.at[index, 'Y_Coordinates'] = y_coordinate

        else:
            main_df.at[index, 'X_Coordinates'] = x_coordinate
            main_df.at[index, 'Y_Coordinates'] = y_coordinate

        print(f'Iteration #{index} - {percentage_progress}%\n{complete_address}: ({x_coordinate},{y_coordinate})')

    main_df.to_csv('some_geolocations_dvbe.csv',index=False)








if __name__ == '__main__':
    
    # The goal with this program is to make some adjustments and crucial changes to the
    # csv file that contain all of the dvbe information. So far, I have two goals involving
    # this file in mind: 1) the acquisition of geolocations, and 2) the correlation of 
    # the 'Keywords' column with CSLB license titles via Linguistic Patterns. The initial
    # file can be found in google cloud.

    first_csv_file_dvbe_initial = 'latest_dvbes.csv'
    second_csv_file_refined_without_geolocations = 'refined_latest_dvbe.csv'
    step = int(input('Step: '))

    match step:

        case 1:
            
            # Step 1: Complete Address Creation, the first step will be creation of a 'CompleteAddress' column. We need to create
            # a column to include the complete addresses. Currently, the addresses are splitted 
            # into 5 columns, we need to put the values of each of those 5 columns into a single
            # column in order for the geofinder to find the geolocation coordinates. After that, 
            # we will output a new file containing such column, in which we will use to find the
            # geolocations directly with.
            
            complete_address_column_creation(first_csv_file_dvbe_initial)

        case 2:

            # Step 2: Geolocation Acquisition, as the title goes, we will be acquiring the respective geolocations
            # for eveyry value under the 'CompleteAddress' columns of the file. We will utilize the freely 
            # available functionality of the U.S. Census Bureau. Thanks U.S. However, unfortunately this functionality
            # isn't complete accurate. If the geolocation was not found, within the same iteration, we will attempt
            # to find the same geolocation using Nominatim.

            geolocation_acquisition(second_csv_file_refined_without_geolocations)







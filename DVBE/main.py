import pandas as pd
import numpy as np
import time
import requests
from pathlib import Path
from geopy.geocoders import Nominatim #type: ignore



start_time = time.time()


'''
[1] Using the Address Line1, Address Line2, City, State, and Postal code,
we will create a new column containing all those attributes in a single
cell value in order to use that cell value to find the respective geolocation
further on.
'''
def complete_address_column_creation(new_entities_dataframe):
    
    # Read the file, covert it to a DataFrame using pandas, then locate
    # the five columns that contain the CompleteAddress attribute, concatenate
    # them together, and create a new column containing the result of the
    # adjunction. One can locate the five columns using the itterrows() 
    # functionality which works efficiently for dataframes.

    
    new_entities_dataframe['CompleteAddress'] = new_entities_dataframe['CompleteAddress'].astype(str)

    for index, row in new_entities_dataframe.iterrows():
        
        # This is where we locate each column by pinpointing it using
        # the title of each column respectively. Each column contains an
        # attribute of the complete address.

        address_line1 = str(row['Address Line 1']).title()
        address_line2 = str(row['Address Line 2']).title()
        city = str(row['City']).title()
        state = row['State']

        # Some of the zip codes contain more than five digits, including a
        # '-' character. Let's remove them since they sometimes alter the 
        # posibility of finding the correct address in question.

        zip_code = str(row['Postal Code'])

        if '-' in zip_code:
            zip_code_split = zip_code.split('-')
            zip_code = zip_code_split[0]

        # Some of the columns cells under 'AddressLine2' are empty, therefore
        # useless. We can build a if statement to apply the address line 2 if
        # applicable, and dismiss it if non-applicable.

        if new_entities_dataframe.isnull().loc[index,'Address Line 2']:
            complete_address = f'{address_line1}, {city}, {state} {zip_code}'
        
        else:
            complete_address = f'{address_line1}, {address_line2}, {city}, {state} {zip_code}'
        
        # Now, it is time to allocate the complete address string into its new
        # column, 'CompleteAddress'. We will do this individually with each of the
        # cells along the dataframe.

        new_entities_dataframe.at[index,'CompleteAddress'] = complete_address
    
    # Once all the complete addresses have been iterated to their respective column,
    # we need to export the dataframe into a csv file for future usage. After that, we
    # will jump to step 2: Geolocation Acquisition.
    
    return new_entities_dataframe
        



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
def geolocation_acquisition(new_entities_dataframe):
    
    # First we need to import the respective csv file into our function, convert it into
    # a dataframe, and begin iteration within the file, in the iteration, we are looking
    # for the 'CompleteAddress' values, which we will use to feed the geolocation
    # finding functions. 

    for index, row in new_entities_dataframe.iterrows():

        percentage_progress = (index/len(new_entities_dataframe))*100
        
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
            new_entities_dataframe.at[index, 'X_Coordinates'] = x_coordinate
            new_entities_dataframe.at[index, 'Y_Coordinates'] = y_coordinate

        else:
            new_entities_dataframe.at[index, 'X_Coordinates'] = x_coordinate
            new_entities_dataframe.at[index, 'Y_Coordinates'] = y_coordinate

        print(f'Iteration #{index} - {round(percentage_progress,2)}%\n{complete_address}: ({x_coordinate},{y_coordinate})')

    return new_entities_dataframe




'''
Using this function, we will segregate the addresses that were not found initially
from the functions above. First, we will allocate all of the non-found geolocations
into a different csv file to use other methods to find them.
Segregating the non-found addressess, yes, that's it...yes, I need a function for that... Also,
I forgot to mention that we will fix the zip_code column, I don't want to use nine-digit zip
codes, but five-digit zip codes.
'''
def geolocation_segregation_and_fix(df):
    
    # As mentioned, the only goal with this function is to segregate the locations
    # with the ones of which the location was not found, a simple action that can
    # be taken by a few lines of code. Yeah, I just don't know what to write here.
    # I just like how big paragraphs look.
    # The real question here is, why do I need a function for this? Well, because I like order...
    # If you do not map everything in your life, eventually the parts of your life that you
    # did not map are going to become dependant on forces outside yours, you will not have control
    # but other people or circumstances will dictate the state of such parts. However, it is not
    # only about mapping, but also acting on the mapping itself... Of course, one cannot map 
    # every single part of one's life, as there isn't enough time to manage all of them properly,
    # this is where one asks oneself: "what is really important, what do I want to have control upon?"...

    
    df['PostalCode'] = df['PostalCode'].astype(str).str.split("-").str[0]

    df_cleaned = df[df['X_Coordinates'] != 0]
    df_cleaned.to_csv('just_in_case_found.csv', index=False)

    df_segregated = df[df['X_Coordinates'] == 0]
    df_segregated.to_csv('just_in_case_nonfound.csv', index=False)


    return df_cleaned, df_segregated
        


'''
The rules are simple, we will simply assign a post office geolocation to all the
non-found addresses based on their zip code value, plain and simple...
'''
def dvbe_concatenation(found_df, nonfound_df):

    # If you want to write less, then write less functions... I just realized that I enjoy writing
    # while coding; those two are my favorite things to do in this mundane life, those too make me
    # enjoy this mundane life, they seem to my agents of art materialization... 
    # The code below checks if there are faulty zip codes. The reason why there might be faulty zip
    # codes is because zip codes from dvbe entities from the dvbe file might not be found in the
    # zip code column of the post_offices file, i.e. we might be lacking post_offices addresses.
    # In this case, there are 7 zip codes that are faulty from the post_office_addresses file, which
    # we will find manually, just for this time as we will most likely utilize such file for other
    # addresses that we cannot find and use the post office address for an alternative. If the faulty
    # zip code list is not extensive, do them manually.


    nonfound_df['X_Coordinates'] = nonfound_df['X_Coordinates'].astype(float)
    nonfound_df['Y_Coordinates'] = nonfound_df['Y_Coordinates'].astype(float)

    post_offices_file = 'https://storage.googleapis.com/wesonder_databases/post_offices/california_post_offices.csv'
    df_post_offices = pd.read_csv(post_offices_file,low_memory=False)

    faulty_zip_codes = []

    for index, row in nonfound_df.iterrows():
        
        zip_code = row['PostalCode']

        if zip_code in df_post_offices['ZipCodeUsed'].values:
            
            index_position = np.where(df_post_offices['ZipCodeUsed'].values == zip_code)[0][0]
            respective_x_coordinate = df_post_offices['X_Coordinates'].iloc[index_position]
            respective_y_coordinate = df_post_offices['Y_Coordinates'].iloc[index_position]
            
            df_non_found_entities.at[index, 'X_Coordinates'] = respective_x_coordinate
            df_non_found_entities.at[index, 'Y_Coordinates'] = respective_y_coordinate
        
        elif zip_code in df_post_offices['ExtraZipCode'].values:

            index_position = np.where(df_post_offices['ExtraZipCode'].values == zip_code)[0][0]
            respective_x_coordinate = df_post_offices['X_Coordinates'].iloc[index_position]
            respective_y_coordinate = df_post_offices['Y_Coordinates'].iloc[index_position]
            
            df_non_found_entities.at[index, 'X_Coordinates'] = respective_x_coordinate
            df_non_found_entities.at[index, 'Y_Coordinates'] = respective_y_coordinate

        else:
            faulty_zip_codes.append(zip_code)

    concatenated_dataframes = pd.concat([nonfound_df, found_df])
    
    return concatenated_dataframes




'''
[1.0] Comparing past and present DVBE between old and new csv files containing them.
'''
def comparing_dvbe_entities(old_file, new_file):

    # Convert csv files to dataframes for easy manipulation
    df_old = pd.read_csv(old_file)
    df_new = pd.read_csv(new_file)

    new_entities = df_new[~df_new['Certification ID'].isin(df_old['Certification ID'])]
    transformative_df = new_entities.reset_index(drop=True)

    return transformative_df
    


'''
[3.0] Concatenating the old and new dvbe firms in order to export them to
the web server. Resources my friend, the distribution of resources. 
'''
def concotenate_dataframes(past_entities_csv, new_entities_df):

    df_past = pd.read_csv(past_entities_csv)

    all_dvbe_entities = pd.concat([df_past, new_entities_df])
    all_dvbe_entities.to_csv('finalized_dvbe_entities.csv', index=False)

            





'''
FUNCTIONALITY STEPS - Estimated Time (15-35 min): 

[1] Step one focuses in comparing the past dvbe csv file with the newly downloaded csv file from
the Cal eProcure website. We are doing so by comparing the license numbers from each of the DVBE
commercial enterprises from the past and current file, adding the new ones that appear in the
newly downloaded file to the past csv file. 

[2] Acquire the Geolocations for the New entities. We will utilize the functions above that are quite
functional. But first, we need to create the CompleteAddress with the entire addresses for each cell.
After the complete addresses, we then acquire the Geolocations using the Complete Addresses. After
acquiring the addresses, try to find a few more using the California Zip codes and the respective
post offices geolocations in order to increase the volume of geolocations found.

[3] As a final last easy step, we append the old dvbe dataframe with the new one, in order to expand 
our existing repertoire of DVBE firms.
'''


# Outset Files
past_dvbe_file = 'https://storage.googleapis.com/wesonder_databases/dvbe/finalized_dvbe_entities.csv'
new_dvbe_file = '/Users/damiamalfaro/Downloads/latest_dvbes.csv' #(newly downloaded file)

# [1] Create the new Dataframe with new DVBE entities
new_entities_df = comparing_dvbe_entities(past_dvbe_file, new_dvbe_file)

# [2] Acquire Geolocations and clean the Dataframe
new_entities_df_complete_addresses = complete_address_column_creation(new_entities_df)

new_entities_df_some_geolocations = geolocation_acquisition(new_entities_df_complete_addresses)

new_entities_geolocations_found = geolocation_segregation_and_fix(new_entities_df_some_geolocations)[0]
new_entities_geolocations_nonfound = geolocation_segregation_and_fix(new_entities_df_some_geolocations)[1]

all_new_dvbe_firms = dvbe_concatenation(new_entities_geolocations_found, new_entities_geolocations_nonfound)

# [3.0]
concotenate_dataframes(past_dvbe_file, all_new_dvbe_firms)








'''
Time Statistics
'''
end_time = time.time()
elapsed_time = end_time - start_time
elapsed_hours = round((elapsed_time / 60 / 60), 3)
print(f'Total Hours to Execute: {elapsed_hours}')
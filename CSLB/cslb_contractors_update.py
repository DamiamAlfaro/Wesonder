# Import Tools
import pandas as pd # type: ignore
import sys
import os
import requests # type: ignore
from pathlib import Path
from geopy.geocoders import Nominatim # type: ignore
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.common.keys import Keys # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from selenium.common.exceptions import TimeoutException # type: ignore
import time




'''
Slow, but effective. The code below downloads all of the files from the
CSLB public data portal based on the license type. Forbid my code below from 
being uncommented, it was created on the past for another program, but
nevertheless resulted in an useful resource.
'''
def downloading_cslb_database():
    cslb_download_webpage = "https://www.cslb.ca.gov/onlineservices/Dataportal/ListByClassification"
    driver = webdriver.Chrome()
    driver.get(cslb_download_webpage)
    time.sleep(4)
    
    # Now enter the section where you can download the Excel tabulations including the subcontractors
    drag_down_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME,"button"))
    )
    
    # Click the Drag Down Menu
    drag_down_button.click()
    
    # Pinpoint the options of the Drag Down Menu just clicked, we can do so by locating the <ul> element
    list_of_options_list_element = WebDriverWait(driver,10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME,"ul"))
    )
    
    
    # Print all of the options within the Drag Down Menu
    list_of_options = list_of_options_list_element[2].find_elements(By.TAG_NAME,"li")
    total_options_count = len(list_of_options)
    print(f"Total Licences = {total_options_count}")

    # Iterate through each license type and download each type singularly
    for license_tabulation in range(1,total_options_count+1):

        # Pinpoint the license name
        label_license = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//label[@for='ms-opt-{license_tabulation}']"))
        )
        print(label_license.text)

        # Remove the fallible one
        if label_license.text == "C-61 - Limited Specialty Classification":
            pass

        # Continue with the non-fallible
        else:
            
            # Click the Checkbox
            checkbox_license = WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.ID,f"ms-opt-{license_tabulation}"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", checkbox_license)
            checkbox_license.click()
    
            # Download button
            download_button = WebDriverWait(driver,10).until(
                EC.element_to_be_clickable((By.NAME,"ctl00$MainContent$btnSearch"))
            )
            download_button.click()
    
            drag_down_button.click()
    
            checkbox_license.click()
    
            driver.implicitly_wait(4)




'''
This will be the function used for the arrangement of a
single file containing all of the contractors information from
the downloaded files, and the comparision of prior subcontractors
with new subcontractors.
'''
def arranging_downloaded_files():
    
    # The first step is to orginaze the location where all of the files have been 
    # allocated, i.e. the Downloads folder path. To do so, we will be using the pathlib 
    # package to enter such path.

    downloads_path = str(Path.home()/"Downloads")
    downloads_path_direction = os.listdir(downloads_path)
    
    # Now that we have the direction to the download path folder, we need to 
    # arrange the files into one, and to do so, we will first convert each file
    # into a DataFrame, append that DataFrame into another dataframe, and continue
    # with the rest. Basically an interation of dataframes adding to a main 
    # dataframe. Furthermore, once we arrange all of the dataframes into a
    # single dataframe, we also need to remove any duplicates. 

    dataframes = []

    for individual_file in downloads_path_direction:
        if individual_file.endswith('xlsx'):
            df = pd.read_excel(f'{downloads_path}/{individual_file}')
            print(df)
            dataframes.append(df)
        else:
            pass

    final_df = pd.concat(dataframes, ignore_index=True)
    final_df = final_df.drop_duplicates()
    final_df.to_csv('cslb_geolocations_raw_update.csv',index=False,header=False)




'''
In this function, we will utilize the prior cslb file to compare the subcontractors
that need geolocations from the present newly downloaded file.
'''
def comparing_past_and_present_contractors():
    
    # Now comes the hard part. Once we have the new raw cslb subcontractors, 
    # withouth any duplicates, we need to compare the prior list with the new list
    # and see which subcontractors have been added to the new list that the prior
    # list does not have. I believe the best way to do this is via license number.
    # A license number is an unique identificator that every contractor possess, we
    # can use such fact to segregate contractors that we do not want (repeated). Once
    # we segregate the new entities, allocate them into a new csv file.
        
    past_file = "ultimate_cslb_geolocations.csv"
    present_file = "cslb_geolocations_raw_update.csv"
    
    df_past = pd.read_csv(past_file, low_memory=False)
    df_present = pd.read_csv(present_file, low_memory=False)

    license_number_past_file = df_past["LicenseNumber"]
    license_number_present_file = df_present["LicenseNumber"]

    new_contractors_all = df_present[~df_present["LicenseNumber"].isin(license_number_past_file)]

    # I forgot to do this step in a previous function, but is fine, we can do it within
    # this current function. The step in question is the action of removing entities
    # that are not located in the state of California. 

    new_file_name = "new_cslb_entities.csv"
    ultimate_new_contractors = new_contractors_all[new_contractors_all["State"] == 'CA']
    
    # Now that we have the file, we need to do one final step before proceeding with the 
    # next step. The current step is to create and allocate the complete addresses for
    # each of the subcontractors. Why? Because we will use such addresses to find the
    # respective geolocation. The way we are going to do it is by 1) locate the necessary
    # strings from the newly created dataframe (ultimate_new_contractors), then 2) allocate
    # them into a single variable, i.e. the complete address, lastly 3) allocate that
    # variable into the CompleteAddress column. Once those steps are undertaken, we will
    # export the dataframe as a new csv file to begin the next step: Geolocation Search.
    # As a last note, don't forget to title the Address and the Cities, the geolocator
    # searches for the geolocation more efficiently that way, at least that is our 
    # presumption...

    for index, row in ultimate_new_contractors.iterrows():

        street = str(row['Address']).title()
        city = str(row['City']).title()
        state = str(row['State'])

        complete_address = f'{street}, {city}, {state}'

        ultimate_new_contractors.at[index, 'CompleteAddress'] = complete_address

    ultimate_new_contractors.to_csv('new_cslb_entities.csv', index=False)
    



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
In this function we will obtain the geolocations, cleanse any geolocations
if needed, append the newly found geolocations to our previous bank of
geolocations, and create a single file.
'''
def obtaining_new_geolocations_and_finalization():
    
    # We will use the function above to extract the geolocations derived from
    # the iteration of the new_cslb_file from Contractor Comparison and use its
    # CompleteAddress values to find the geolocations. Once found, we will allocate
    # them into the dataframe.

    initial_main_dataframe = pd.read_csv('ultimate_cslb_geolocations.csv', low_memory=False)
    present_csv_file = pd.read_csv('new_cslb_entities.csv', low_memory=False)

    for index, row in present_csv_file.iterrows():

        complete_address = row['CompleteAddress']
        coordinates = obtaining_new_geolocations_attempt1(complete_address)
        x_coordinate = coordinates[0]
        y_coordinate = coordinates[1]

        # We will utilize another geolocation library to find the addresses
        # that were not found at the first attempt. The library in question is Nominatim. 
        # After the second attempt, we will cleanse the file again, and concatenate the 
        # attempt 1 and attempt 2 dataframe together, then concatenate that dataframe with
        # the main past cslb dataframe in order to update the directory of contractors.

        if x_coordinate == 0 or y_coordinate == 0:
            second_attempt = obtaining_new_geolocations_attempt2(str(complete_address))
            x_coordinate = second_attempt[0]
            y_coordinate = second_attempt[1]
            present_csv_file.at[index, 'X_Coordinate'] = x_coordinate
            present_csv_file.at[index, 'Y_Coordinate'] = y_coordinate


        else:
            present_csv_file.at[index, 'X_Coordinate'] = x_coordinate
            present_csv_file.at[index, 'Y_Coordinate'] = y_coordinate

        print(f'{complete_address} #{index}: ({x_coordinate},{y_coordinate})')

    # Now that we have the geolocation extraction working, and have a complete 
    # dataframe with all of the geolocations, we need to cleanse them. What
    # do I mean by "cleanse"? To remove any addresses that were not fortunate
    # enough to find coordinates.
    
    refined_present_csv = present_csv_file[present_csv_file['X_Coordinate'] != 0]

    # Lastly, the materialization of a finalized dataframe containing the past
    # contractors, as well as the newly added contractors into the dataframe.
    # I don't see any reason to keep the contractors that do not possess a geolocation
    # and the reason for that is because acquiring geolocations becomes expensive, we
    # don't have the resources to be expensive now.

    finalized_dataframe = pd.concat([initial_main_dataframe,refined_present_csv])
    finalized_dataframe.to_csv('finalized_cslb_update.csv',index=False)

    print(present_csv_file)
    print(refined_present_csv)

    

    
if __name__ == "__main__":

    # For aesthetic purposes, we will ask the user which step to 
    # undertake in order to avoid uncommenting and commenting functions
    # everytime we execute the program.

    step = int(input('Step Number: '))

    match step:
        case 1:

            # Step 1: Source Downloading, the first step is to download all licensed contractors from our main source, the
            # Contractors State Licence Board, also called CSLB. They have a Public Data Portal
            # in which they possess all contractors and subcontractors in California, their
            # name, title, license type, etc. 

            downloading_cslb_database()
            time.sleep(4)
        
        case 2:

            # Step 2: File Concatenation, once all files are downloaded, we need to automate the arrangement of files. What
            # do I mean? Once the files are downloaded, we need to arrange them together into
            # a single file. To do so, we will use the following function, please refer to it
            # for more details:

            arranging_downloaded_files()

        case 3:

            # Step 3: Contractor Comparison, now that we have a single file containing all of the contractors up to date,
            # we need to compare that file with the previous file in order to see which new contractors
            # have been added, and if any, get their geolocations.

            comparing_past_and_present_contractors()

        case 4:

            # Step 4: Geolocation Search, it involves the use of freely open sourced software to find the 
            # geolocations of the contractors from Contractor Comparison (Step 3). We will find the
            # respective geolocations, attach them to 
            
            obtaining_new_geolocations_and_finalization()

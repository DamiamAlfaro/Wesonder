import pandas as pd  # type: ignore
import time
import re
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore









'''
Cleanse the shit out of the csv file.
'''
def cleansing_file(csv_file):
    
    # Convert the csv file into a Pandas Dataframe
    df = pd.read_csv(csv_file)
    df =  df.drop_duplicates()

    # Separate the rows without geolocations
    df_faulty = df[df['X_Coordinates'] != 0]
    df_faulty.to_csv('cleaned_dir_projects.csv',index=False)


'''
Let's clean the main csv file a little bit by removing duplicated rows
'''
def cleaninsing_main_file(main_csv_file):
    
    # Import it as a DataFrame and remove duplicates... Yes, that's it
    df = pd.read_csv(main_csv_file)
    df = df.drop_duplicates()
    df.to_csv('refined_dir_projects_complete.csv',index=False)


'''
Allocate the complete addresses in the main csv file on a new column
in order to facilitate the correlation of geolocations further on
'''
def complete_addresses_allocation(main_csv_file):
    
    # Import as DataFrame
    df = pd.read_csv(main_csv_file, low_memory=False)

    # Allocate the attributes of the complete address
    for index, row in df.iterrows():
        address1 = row['ProjectAddress1']
        address2 = row['ProjectAddress2']
        city = row['City']
        state = row['State']

        # Check if the address is empty, if it is, do not even bother to allocate it
        if pd.isna(address1) or address1.strip() == "":
            continue
        
        else:
            # Create scenarios for when there is an actual address2 line
            if pd.isna(address2) or address2.strip() == "":
                complete_address_string = f"{address1}, {city}, {state}"
            
            else:
                # CompleteAddress string
                complete_address_string = f"{address1} {address2}, {city}, {state}"
        
        # Allocate the complete address string in its respective location
        df.at[index,'CompleteAddress'] = complete_address_string
    
    df.to_csv('refined_dir_projects_projects.csv',index=False)




'''
From the main file, categorize the projects that have addresses with the ones
that do not have addresses in order to make iteration faster, and just have those files
as reference.
'''
def categorizing_addresses(main_csv_file):
    
    # Folder Location of new files
    folder_location = "/Users/damiamalfaro/Desktop/Europe/testing_wesonder/Geolocations_DIR_Projects/"
    
    # Read into DataFrame
    df = pd.read_csv(main_csv_file)
    
    # Categorize non-addresses and addresses projects
    df_no_address = df[df['CompleteAddress'].isnull()]
    df_with_address = df[df['CompleteAddress'].notna()]
    
    # Transcribe to csv file
    df_no_address.to_csv(f'{folder_location}dir_projects_without_addresses.csv',index=False)
    df_with_address.to_csv(f'{folder_location}dir_projects_containing_addresses.csv',index=False)

    
    


'''
Allocate the respective addresses to the respective projects
'''
def allocation_of_geolocations(main_csv_file, geolocations_csv_file,folder_name):
    
    # Import files as dataframes 
    df_main = pd.read_csv(main_csv_file, low_memory=False)
    df_geo = pd.read_csv(geolocations_csv_file)

    # Iterate through the main csv file while correlating the addresses on the geolocation file
    for index, row in df_main.iterrows():
        address = row['CompleteAddress'].title()
        
        # iterate in order to find all geolocations
        for indexb, rowb in df_geo.iterrows():
            if address in rowb['Address'].title():
                x_coordinates = rowb['X_Coordinates']
                y_coordinates = rowb['Y_Coordinates']
                
                df_main.at[index,'X_Coordinates'] = x_coordinates
                df_main.at[index,'Y_Coordinates'] = y_coordinates
                print(f"{address} {x_coordinates} {y_coordinates}")
                break
    
    # Import into csv
    df_main.to_csv(f'{folder_name}dir_projects_mapping.csv',index=False)
                



'''
We are going to dismiss the projects that did not acquire a geolocation, after that we will allocate the respective county
to each of the projects in order to optimize the speed of the display, just as we do with the Contractor Licenses.
'''
def geolocation_only_addresses(csv_file):
    
    # Import as dataframe
    df = pd.read_csv(csv_file, low_memory=False)
    df_valid = df[df['X_Coordinates'].notna()]
    df_valid.to_csv('mapping_dir_projects_no_county.csv',index=False)


'''
Acquire the municipalities and their counties
'''
def california_municipalities(url):

    # Initiate driver
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)

    # Locate the table element corresponding to the data required and scrap its columns 0 and 1 (Municipality and County)
    table_element_list = driver.find_elements(By.TAG_NAME,'table')
    table_element = table_element_list[1]
    tbody_tag = table_element.find_element(By.TAG_NAME,'tbody')
    tr_tags = tbody_tag.find_elements(By.TAG_NAME, 'tr')

    municipalities = []
    counties = []

    for td_tag in tr_tags:
        th_tag = td_tag.find_element(By.TAG_NAME,'th')
        td_tags = td_tag.find_elements(By.TAG_NAME,'td')
        municipality = re.sub(r'[^a-zA-Z0-9\s]', '', th_tag.text)
        county = td_tags[1].text
        municipalities.append(municipality)
        counties.append(county)

    df = pd.DataFrame({
        'Location':municipalities,
        'County':counties
    })

    df.to_csv('municipalities.csv',index=False)

'''
Acquire the municipalities and their counties
'''
def cdps_location(url):

    # Initiate driver
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)

    # Locate the table element corresponding to the data required and scrap its columns 0 and 1 (Municipality and County)
    table_element_list = driver.find_elements(By.TAG_NAME,'table')
    table_element = table_element_list[1]
    tbody_tag = table_element.find_element(By.TAG_NAME,'tbody')
    tr_tags = tbody_tag.find_elements(By.TAG_NAME, 'tr')

    places = []
    counties = []

    for td_tag in tr_tags:
        th_tag = td_tag.find_element(By.TAG_NAME,'th')
        td_tags = td_tag.find_elements(By.TAG_NAME,'td')
        place = re.sub(r'[^a-zA-Z0-9\s]', '', th_tag.text)
        county = td_tags[0].text
        places.append(place)
        counties.append(county)
    
    df = pd.DataFrame({
        'Location':places,
        'County':counties
    })

    df.to_csv('other_places.csv',index=False)




'''
Get the counties, municipalities, and census designated places of california. The goal is to store the respective locations
into a dataframe for later use
'''
def counties_and_censuses():

    # Pinpoint the url that will be used
    municipalities_url = 'https://en.wikipedia.org/wiki/List_of_municipalities_in_California'
    cdp_url = 'https://en.wikipedia.org/wiki/List_of_largest_census-designated_places_in_California'
    california_municipalities(municipalities_url)
    cdps_location(cdp_url)










'''
Allocating the counties for each project based on the city where it took place in order to optimize the display of the projects
as a feature in wesonder by utilizing the up-to-three-functionality from the contractors.
'''
def county_allocation(csv_file):
    
    # You know the drill
    df = pd.read_csv(csv_file, low_memory=False)

    # Ready to be mappeds
    df_new = df[df['County'].notna()]
    df_new.to_csv('/Users/damiamalfaro/Desktop/Europe/testing_wesonder/Geolocations_DIR_Projects/mapping_dir_projects.csv',index=False)
    


    





if __name__ == "__main__":
    
    # Import csv files
    folder_name = '/Users/damiamalfaro/Desktop/Europe/testing_wesonder/Geolocations_DIR_Projects/'
    main_csv_file = f'{folder_name}addresses_dir_projects_complete.csv'
    faulty_csv_file = f'{folder_name}dir_projects_faulty.csv'
    geolocations_file = f'{folder_name}dir_projects_geolocations.csv'
    projects_with_addreses = f'{folder_name}dir_projects_containing_addresses.csv'
    absolute_csv_file = '/Users/damiamalfaro/Downloads/dir_projects_no_county.csv'

    # Clean the DIR Projects Geolocations
    #cleansing_file(faulty_csv_file)

    # Clean the main file
    #cleaninsing_main_file(main_csv_file)

    # Allocate complete addresses in main csv file
    #complete_addresses_allocation(main_csv_file)

    # Categorize the projects with and without addresses to make iteration easier
    #categorizing_addresses(main_csv_file)

    # Allocate the respective geolocations into the addresses
    #allocation_of_geolocations(projects_with_addreses,geolocations_file,folder_name)

    # Last thing: clean the unnecessary projects withouth addresses so as to show the projects with geolocations only
    #geolocation_only_addresses(absolute_csv_file)

    # County allocation: first acquire the counties, the Census Designated Places, and then connect them with the main csv
    #counties_and_censuses()
    #county_allocation(absolute_csv_file)
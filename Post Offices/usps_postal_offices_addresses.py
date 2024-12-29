import pandas as pd
import time
import os
import requests
from pathlib import Path
from geopy.geocoders import Nominatim
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




'''
Using the following function we will store the post office's attributes into a csv file
in order to access it later. The question is, how should the arrangement of columns be
within the file?
'''
def allocate_post_offices_within_csv(attributes_list):
    
    # Just a simple allocation into the csv file. The headers of the file are the 
    # following: OfficeName, OfficeAddress, OfficeDistance, OfficeWebPage, 
    # ZipCodeUsed, OfficeNoInZip.

    df = pd.DataFrame({
        "OfficeName":[attributes_list[4]],
        "OfficeAddress":[attributes_list[5]],
        "OfficeDistance":[attributes_list[2]],
        "OfficeWebPage":[attributes_list[3]],
        "ZipCodeUsed":[attributes_list[1]],
        "OfficeNoInZip":[attributes_list[0]]
    })

    df.to_csv('california_post_offices.csv',index=False,header=False, mode='a')





'''
This function will collect the attributes of each of the post offices. The idea
is to utilize this function for every zip code within the 50-chunk lists.
'''
def collection_of_post_offices_attributes(driver, zip_code):

    # Now that we've accomplished the searching functionality, we need to collect
    # what we came for: the addresses. We have a 6-second window to collect them,
    # in order to do so, we will need to find the html elements associated with
    # them. This will be a process of stratification access. We will be collecting
    # multiple variables from each of the results: Distance (in miles) from Zip
    # Code, Post Office Info Link, Post Office Name, and Post Office Address. Each
    # variable will have its own column. The code below is Webscraping 101...

    addresses_results_list = driver.find_element(By.ID,"poloResults")
    individual_post_offices = addresses_results_list.find_elements(By.TAG_NAME,"li")
    for individual_post_office in range(len(individual_post_offices)):

        post_office_attributes = []

        print(f"Office #{individual_post_office}")
        post_office_attributes.append(individual_post_office)

        print(f"Zip Code: {zip_code}")
        post_office_attributes.append(zip_code)
        
        distance_from_zip_code = individual_post_offices[individual_post_office].find_element(
            By.CLASS_NAME,"result-details-distance"
        ).text.split(
            ' '
        )[0]
        post_office_attributes.append(distance_from_zip_code)
        print(f'Distance: {distance_from_zip_code}')

        post_office_info_link = individual_post_offices[individual_post_office].find_element(
            By.TAG_NAME,'a'
        ).get_attribute('href')
        post_office_attributes.append(post_office_info_link)
        print(f'Post Office Webpage: {post_office_info_link}')


        post_office_name = individual_post_offices[individual_post_office].find_element(
            By.CLASS_NAME,"result-details-link"
        ).text
        post_office_attributes.append(post_office_name)
        print(f'Post Office Name: {post_office_name}')


        post_office_address_element1, post_office_address_element2 = individual_post_offices[individual_post_office].find_element(
            By.CLASS_NAME,"result-details-address"
        ).text, individual_post_offices[individual_post_office].find_element(
            By.CLASS_NAME,"result-details-secondary"
        ).text
        post_office_address = f'{post_office_address_element1}, {post_office_address_element2}'
        post_office_attributes.append(post_office_address)
        print(f"Address: {post_office_address}\n")

        allocate_post_offices_within_csv(post_office_attributes)
    
    


'''
Using the zip code string, we will go to the Post Office Locator website and
search for the respective zip code, webscrap the results, and allocate them 
into a csv file which will be containing all of the post offices actual addressess.
This function will only do 50 searches for 50 different zip codes.
'''
def webscraping_post_offices_using_zipcodes(zip_codes_list, main_count, total_current_zip_codes, all_zip_codes):
    
    # First, we will open the session, then use the 50 zip codes as input in the
    # respective space for input within the website, after that, we will extract the 
    # addresses attributes into another function for csv allocation. After the 50 
    # sized iteration, we will close the session, and start with the remaining 
    # zip codes. The variable 'subcount' is, as mentioned, meant to serve as 
    # index locator in case a halt occurs. In this case, this count is not inputed
    # via input(), but manually within the code. 

    subcount = 0
    post_office_locator_website_url = 'https://tools.usps.com/locations/'
    driver = webdriver.Chrome()
    driver.get(post_office_locator_website_url)
    time.sleep(4)

    for zip_code in range(subcount, len(zip_codes_list)):

        # Let's go step by step: The first step is locate the input text box within the 
        # website, assign a value, and search for it. We need to give it a few seconds
        # after the operation has been executed. Also, we will use the initial zip
        # code list in order to display percentage completed overall using the index()
        # functionality.

        overall_zip_code_position = all_zip_codes.index(zip_codes_list[zip_code])

        string_zip_code = str(zip_codes_list[zip_code])
        input_value_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID,"searchMainType"))
        )
        input_value_box.clear()
        input_value_box.send_keys(string_zip_code)
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "searchPOLO"))
        )
        search_button.click()
        time.sleep(8)

        # The second step is to collect the post office attributes, and allocate them
        # into a neat csv file for later use, after that, we will restart the iteration
        # within the zip_code list with length 50. We like to visualize progress, so we 
        # display the percentage completed.
        
        collection_of_post_offices_attributes(driver, string_zip_code)
        sub_percentage_completed = round((zip_code/total_current_zip_codes) * 100,2)
        overall_percentage_completed = round((overall_zip_code_position/len(all_zip_codes))*100,2)
        print(
            f'Main Count: {main_count}\nSubcount: {zip_code} collected.\nSub-Percentage Completed: {sub_percentage_completed}%'
        )
        print(f"Overall-Percentage Completed: {overall_percentage_completed}%")

        # The third step is to change the search bar in the website. In order to do so,
        # we will erase the existing zip_code string, input the new zip_code string,
        # and click on the search button once again.

        input_value_box.clear()
        time.sleep(4)

    


'''
Let's start with iterating each of the zip codes. We will utilize each zip
code as an input for another function which will be webscraping the addresses
of the postal offices based on that zip code value.
'''
def iterating_each_zip_code_list(csv_file, count):
    
    # I don't think I need to explain myself twice... Perhaps, I will stop
    # filling paragraphs with repeated statements or nonsense; paragraphs
    # will only be written if necessary. The variables 'count' and 'chunked_list'
    # are meant to be indicators of index location in case a halt within the 
    # program occurs.

    df = pd.read_csv(csv_file,low_memory=False)
    zip_codes_list = list(df['ZipCode'])
    chunked_lists = [zip_codes_list[i:i+50] for i in range(0, len(zip_codes_list), 50)]
    for chunked_list in range(count,len(chunked_lists)):

        
        webscraping_post_offices_using_zipcodes(chunked_lists[chunked_list], 
                                                chunked_list, 
                                                len(chunked_lists[chunked_list]),
                                                zip_codes_list)
    



'''
Step 2: As explained, we will refine the addresses under the OfficeAddress column in order to
assure a bigger probability of geolocation find. And you know what, let's remove the
additional zip code digits. 
'''
def post_offices_refinement(csv_file):
    
    df = pd.read_csv(csv_file,low_memory=False)

    # We will utilize the split(' ') & index methodolgy in order to alter the strings
    # of each address. There are patterns, such as the zip code being the last item
    # of such list, and the state (which has to remain in capital letters) is the 
    # penultimate item.

    for index, row in df.iterrows():
        
        address_string = row['OfficeAddress']
        split_methodology = address_string.split(" ")
        zip_code = split_methodology[-1].split("-")[0]
        state = split_methodology[-2]
        address_again = " ".join(split_methodology[:-2]).title()
        refined_address_string = f'{address_again} {state} {zip_code}'
        
        df.at[index, 'OfficeAddress'] = refined_address_string

    df.to_csv('refined_california_post_offices.csv',index=False)




'''
Using the following function we will store the post office attributes into a csv file
in order to access it later. The question is, how should the arrangement of columns be
within the file?
'''
def allocate_attributes_within_csv(attributes_list):
    
    # Just a simple allocation into the csv file. The headers of the file are the 
    # following: AwardingBody, WebLink, County, X_Coordinates, and Y_Coordinates.
    
    file_name = 'finalized_california_post_offices.csv'

    df = pd.DataFrame({
        "OfficeName":[attributes_list[0]],
        "OfficeAddress":[attributes_list[1]],
        "OfficeDistance":[attributes_list[2]],
        "OfficeWebPage":[attributes_list[3]],
        "ZipCodeUsed":[attributes_list[4]],
        "OfficeNoInZip":[attributes_list[5]],
        "X_Coordinate":[attributes_list[6]],
        "Y_Coordinate":[attributes_list[7]]
    })

    if not os.path.isfile(file_name):
        df.to_csv(file_name, index=False, header=True, mode='w')

    else:
        df.to_csv(file_name, index=False, header=False, mode='a')



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
Utilizing the double geolocation acquisition method we will acquire the geolocations for
all of the post offices in California. One thing to mention is that we need to adjust
all of the zip codes, currently they use the nine digit system instead of the standard five
digit system.
'''
def post_offices_geolocations_acquisition(csv_file,count):

    main_df = pd.read_csv(csv_file, low_memory=False)

    for index, row in main_df.iloc[count:].iterrows():

        percentage_progress = (index/len(main_df))*100
        
        office_name = row['OfficeName']
        complete_address = row['OfficeAddress']
        distance = row['OfficeDistance']
        webpage = row['OfficeWebPage']
        zip_code = row['ZipCodeUsed']
        zip_code_number = row['OfficeNoInZip']


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

        list_of_attributes = [
            office_name,
            complete_address,
            distance,
            webpage,
            zip_code,
            zip_code_number,
            x_coordinate,
            y_coordinate
        ]

        allocate_attributes_within_csv(list_of_attributes)    

        print(f'Iteration #{index} - {round(percentage_progress,2)}%\n{complete_address}: ({x_coordinate},{y_coordinate})\n')






'''
As mentioned, we will just cleansing the csv file. Actually, I want to add a new functionality
to the following function: check if there is at least one post office for every zip code in
order to assure funcionality. 
'''
def post_offices_geolocations_cleaning(csv_file):
    
    # The goal is to check if a zip code has at least one post office with a found
    # geolocation, the way we find this is by assigning a new list that will serve as
    # a detector; if a zip code is not in the list, the zip code gets appended to the 
    # list, then, if the zip code is within the list and the x_coordinate value is
    # above zero (i.e. it exists), the zip code gets removed from the list. Otherwise
    # the zip code stays in the list and reveals itself as a malfunction.

    df = pd.read_csv(csv_file,low_memory=False)

    zip_code_check_list = []

    for zip_code, group in df.groupby('ZipCodeUsed'):
        if all(group['X_Coordinates'] == 0):
            zip_code_check_list.append(zip_code)


    # Now we can continue with the cleansen, after all, every single post office with an
    # unique zip code is going to have a respective post office geolocation associated with
    # the office location.

    df_cleansed = df[df['X_Coordinates'] != 0]
    df_cleansed.to_csv('final_california_post_offices.csv',index=False)




'''
We will modify and expand our stockpile of zip codes for the post offices, I cannot belive that some
of the zip codes under the address column are not even found under the ZipCodeUsed column, which is
supposed to be the column that contains all zip_codes in California...
'''
def zip_code_stockpile_expansion(csv_file):
    
    # As showed by my frustration, I cannot believe that some of the zip codes on the addresses do not 
    # correlate with the zip code column which is supposed to be the column with all of the zip codes of
    # California, can you believe that? And to my inconvenience, the zip codes are nine-digit zip codes...
    # But honestly, I am not even mad, the more I problems I solve, the more I improve at my art style: 
    # Coding and Writing.

    df = pd.read_csv(csv_file, low_memory=False)
    df['ExtraZipCode'] = df['ExtraZipCode'].astype('str')

    for index, row in df.iterrows():
    
        address = row['OfficeAddress']

        new_zip_code = address.split(" ")[-1]

        if new_zip_code.split('-'):
            new_zip_code = new_zip_code.split('-')[0]
        
        else:
            pass

        df.at[index, 'ExtraZipCode'] = new_zip_code


    df.to_csv('ultimate_california_post_offices.csv',index=False)




if __name__ == '__main__':
    
    # The goal of this program is to develop a webscraping mechanisms that has the aim to
    # webscrap the addresses of all of the post offices in California. The data from this
    # mechanism will be used to correlate DVBE firms (and perhaps any other address) that
    # geolocations cannot be easily found using conventional methods. As you might know,
    # it is hard to find P.O. boxes coordinates since they are not technically an
    # official street address.

    california_zip_codes = 'california_zip_codes.csv'
    california_post_offices = 'california_post_offices.csv'
    refined_california_post_offices = 'refined_california_post_offices.csv'
    geolocations_post_offices = 'finalized_california_post_offices.csv'
    final_california_post_offices = 'final_california_post_offices.csv'
    ultimate_california_post_offices = 'ultimate_california_post_offices.csv'
    

    step = int(input('Step: '))

    match step:

        case 1:

            # Step 1: File Iteration, the first step is to iterate through the non_found_geolocations 
            # file and locate the zip code column, and use the values under such column as inputs
            # in the Post Office Locator website in order to webscrap the results. Additionally;
            # Chunk Size Webscraping. I have a plan: We are going to try two approaches, 
            # the first one is to webscrap the post office addresses in a single selenium session 
            # in chunks, i.e. we will webscrap all the addresses using 50 zip codes, close the 
            # session, and do it again with the following 50 zip codes, in case something fails. 
            # And the second...You know what,  I will only use Selenium here, I don't want to 
            # mix Beautiful Soup and Selenium...
            
            count = int(input('Count: '))
            iterating_each_zip_code_list(california_zip_codes, count)

        case 2:

            # Step 2: Address Cleanup, we will be cleaning the OfficeAddress column within the 
            # post offices addresses. Which changes? The adjustment from 9-digit zip codes to
            # 5-digit zip codes for instance. Not only that, but we will also make the address
            # strings into Title mode, just in case.

            post_offices_refinement(california_post_offices)
    
        case 3:

            # Step 3: Geolocation Acquisitions: as usual, we will find the geolocations of the
            # different Post Offices. We will utilize the double acquisition approach of using
            # the U.S. Geolocation service along with Nominatim.

            count = int(input('Count: '))
            post_offices_geolocations_acquisition(refined_california_post_offices, count)

        case 4:

            # Step 4: Geolocation Cleansing: this is a small step, we will just remove all of the
            # Post Offices without Geolocations since there is a high possibility that if a post
            # office was not found within the zip code in question, we can always reference the 
            # following one.

            post_offices_geolocations_cleaning(geolocations_post_offices)

        case 5:

            # Step 5: Additional Zip Codes: I just realized that some of the zip codes under the columns
            # 'ZipCodeUsed in the post offices are not the same as the actual zip code of the address of
            # the post office, what's worse, there are zip codes under the addresses that are not found 
            # in the 'ZipCodeUsed' column, and what's even worse, some are fucking nine-digits... Let's
            # fucking fix that.

            zip_code_stockpile_expansion(final_california_post_offices)




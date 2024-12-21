import pandas as pd
import time
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC






'''
This function will collect the attributes of each of the post offices. The idea
is to utilize this function for every zip code within the 50-chunk lists.
'''
def collection_of_post_offices_attributes(driver):

    # Now that we've accomplished the searching functionality, we need to collect
    # what we came for: the addresses. We have a 6-second window to collect them,
    # in order to do so, we will need to find the html elements associated with
    # them. This will be a process of stratification access. We will be collecting
    # multiple variables from each of the results: Distance (in miles) from Zip
    # Code, Post Office Info Link, Post Office Name, and Post Office Address. Each
    # variable will have its own column. The code below is Webscraping 101...

    addresses_results_list = driver.find_element(By.ID,"poloResults")
    individual_post_offices = addresses_results_list.find_elements(By.TAG_NAME,"li")
    post_offices = []
    for individual_post_office in individual_post_offices:

        post_office_attributes = []
        
        distance_from_zip_code = individual_post_office.find_element(
            By.CLASS_NAME,"result-details-distance"
        ).text.split(
            ' '
        )[0]
        post_office_attributes.append(distance_from_zip_code)

        post_office_info_link = individual_post_office.find_element(
            By.TAG_NAME,'a'
        ).get_attribute('href')
        post_office_attributes.append(post_office_info_link)

        post_office_name = individual_post_office.find_element(
            By.CLASS_NAME,"result-details-link"
        ).text
        post_office_attributes.append(post_office_name)

        post_office_address_element1, post_office_address_element2 = individual_post_office.find_element(
            By.CLASS_NAME,"result-details-address"
        ).text, individual_post_office.find_element(
            By.CLASS_NAME,"result-details-secondary"
        ).text
        post_office_address = f'{post_office_address_element1}, {post_office_address_element2}'
        post_office_attributes.append(post_office_address)

        post_offices.append(post_office_attributes)

        print(post_office_address)
    print(len(individual_post_offices))



'''
Using the zip code string, we will go to the Post Office Locator website and
search for the respective zip code, webscrap the results, and allocate them 
into a csv file which will be containing all of the post offices actual addressess.
This function will only do 50 searches for 50 different zip codes.
'''
def webscraping_post_offices_using_zipcodes(zip_codes_list):
    
    # First, we will open the session, then use the 50 zip codes as input in the
    # respective space for input within the website, after that, we will extract the 
    # addresses attributes into another function for csv allocation. After the 50 
    # sized iteration, we will close the session, and start with the remaining 
    # zip codes.

    post_office_locator_website_url = 'https://tools.usps.com/locations/'
    driver = webdriver.Chrome()
    driver.get(post_office_locator_website_url)
    time.sleep(4)

    for zip_code in zip_codes_list:

        # Let's go step by step: The first step is locate the input text box within the 
        # website, assign a value, and search for it. We need to give it a few seconds
        # after the operation has been executed.

        zip_code = str(zip_code)

        input_value_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID,"searchMainType"))
        )
        input_value_box.clear()
        input_value_box.send_keys(zip_code)
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "searchPOLO"))
        )
        search_button.click()
        time.sleep(8)

        # The second step is to collect the post office attributes, and allocate them
        # into a neat csv file for later use, after that, we will restart the iteration
        # within the zip_code list with length 50.

        collection_of_post_offices_attributes(driver)

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
    # will only be written if necessary.

    df = pd.read_csv(csv_file,low_memory=False)
    zip_codes_list = list(df['ZipCode'])
    chunked_lists = [zip_codes_list[i:i+50] for i in range(0, len(zip_codes_list), 50)]
    for chunked_list in chunked_lists:
        webscraping_post_offices_using_zipcodes(chunked_list)
    
    
    

        
        







if __name__ == '__main__':
    
    # The goal of this program is to develop a webscraping mechanisms that has the aim to
    # webscrap the addresses of all of the post offices in California. The data from this
    # mechanism will be used to correlate DVBE firms (and perhaps any other address) that
    # geolocations cannot be easily found using conventional methods. As you might know,
    # it is hard to find P.O. boxes coordinates since they are not technically an
    # official street address.

    california_zip_codes = 'california_zip_codes.csv'

    step = int(input('Step: '))

    match step:

        case 1:

            # Step 1: File Iteration, the first step is to iterate through the non_found_geolocations 
            # file and locate the zip code column, and use the values under such column as inputs
            # in the Post Office Locator website in order to webscrap the results. 

            # Step 2: Chunk Size Webscraping I have a plan: We are going to try two approaches, 
            # the first one is to webscrap the post office addresses in a single selenium session 
            # in chunks, i.e. we will webscrap all the addresses using 50 zip codes, close the 
            # session, and do it again with the following 50 zip codes, in case something fails. 
            # And the second...You know what,  I will only use Selenium here, I don't want to 
            # mix Beautiful Soup and Selenium...
            
            count = int(input('Count: '))
            iterating_each_zip_code_list(california_zip_codes, count)


import pandas as pd
import time
import re
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from geopy.geocoders import Nominatim
from google.oauth2.service_account import Credentials # type: ignore
from googleapiclient.discovery import build  # type: ignore


start_time = time.time()


# 1 - Removing the anti-bot mechanism
def entering_the_site(url_site):

    # The first step is to remove the annoying pop-up display as soon as one enters the website...
    driver = webdriver.Chrome()
    driver.get(url_site)
    time.sleep(2)

    try:
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'close-btn'))
        )
        close_button.click()
        time.sleep(2)
    except:
        pass 

    dropdown_menu = driver.find_element(By.ID,"bottomPagination-select")
    select = Select(dropdown_menu)
    options = select.options
    select.select_by_index(len(options) - 1)
    time.sleep(2)

    return driver



# [1.1] Expropriating the attributes for
# each of the bids from [1.0]
def bid_attributes(url):
    
    try:
        driver = webdriver.Chrome()
        driver.get(url)
        
        # Remove the anti-both mechanism, just if
        # completely necessary
        try:
            close_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'close-btn'))
            )
            close_button.click()
            time.sleep(2)
        except:
            pass


        # Bid Title
        bid_title = driver.find_element(By.TAG_NAME,'h1').text

        # Grid with more items: Notice ID, Related Notice, and Government Departments
        attribute_grid = driver.find_element(By.CSS_SELECTOR, 'div.sam-ui.attached.grid')
        
        # Notice ID
        notice_id = attribute_grid.find_element(By.ID,"header-solicitation-number")
        notice_id = notice_id.find_element(By.CLASS_NAME,"description").text

        # Related Notice
        related_notice = attribute_grid.find_element(By.ID,"header-related-notice")
        try:
            related_notice = related_notice.find_element(By.CLASS_NAME,"description").text
        except:
            related_notice = "none"

        # Department(s)
        departments = attribute_grid.find_element(By.ID,"header-hierarchy-level")
        try:
            department_tiers = [tier.text for tier in departments.find_elements(By.CLASS_NAME, "header")]
            department_tiers = ";".join(department_tiers) if department_tiers else "none"
            
            department_names = [name.text for name in departments.find_elements(By.CLASS_NAME, "description")]
            department_names = ";".join(department_names) if department_names else "none" 
        except Exception as e:
            department_tiers = "none"
            department_names = "none"
        

        all_attributes = [
            url,
            bid_title,
            notice_id,
            related_notice,
            department_tiers,
            department_names
        ]

        # Original Set Aside
        original_set_aside = driver.find_element(By.ID,"classification-original-set-aside").text

        # Set Aside
        set_aside = driver.find_element(By.ID,"classification-original-set-aside").text

        # Product Service Code
        service_code = driver.find_element(By.ID,"classification-classification-code").text

        # NAICS Code
        naics_code = driver.find_element(By.ID,"classification-naics-code").text

        # Place of Performance
        location = driver.find_element(By.ID,"classification-pop").text
        location = location.split('USA')[0]

        driver.quit()

        # Cleansing the strings
        class_attributes = [
            original_set_aside,
            set_aside,
            service_code,
            naics_code,
            location
        ]

        class_attributes = [
            t.split(":")[1].replace("\n","").replace("\t","") for t in class_attributes
        ]

        all_attributes.extend(class_attributes)

        all_attributes = ["none" if item == "" else item for item in all_attributes]

        return all_attributes
    
    except:
        driver.quit()
        return []





# [1.0] Entering Sam.gov and expropriating
# every single active bid
def entering_sam_gov(sam_url):

    # Remove the anti-bot mechanism (pathetic...) and increase results displayed
    driver = entering_the_site(sam_url)

    # Now start webscraping the links to each individual bid
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    individual_links = soup.find_all('h3',class_='margin-y-0')
    individual_links = [link.find('a').get('href') for link in individual_links]
    individual_links = [f'https://sam.gov{link}' for link in individual_links]
    driver.quit()

    # Respective sessions
    successful_sessions = []
    failed_sessions = []

    # Once acquired, webscrap each of them
    for index, sam_bid in enumerate(individual_links[:2]):

        # [1.1] Webscrap the attributes of each
        # of the bids expropriated
        attributes = bid_attributes(sam_bid)

        # Checks whether the bid attributes
        # segregation worked
        if attributes:
            print(f"Successful #{index}: {sam_bid}")
            successful_sessions.append(attributes)

        else:
            print(f"Failure #{index}: {sam_bid}")
            failed_sessions.append(sam_bid)  

    # Make sure we get them all
    while len(failed_sessions[:]) != 0:
        for index, url in enumerate(failed_sessions[:]):
            attributes = bid_attributes(url)

            if attributes:
                successful_sessions.append(attributes)
                failed_sessions.remove(url)
            
    return successful_sessions




    return successful_sessions


# [2.1] As the title states...
def obtaining_new_geolocations(address_string):
    
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
    


# [2.0] As the title states...
def acquiring_geolocations(active_bids_list):

    for bid in active_bids_list:

        # [2.1] Directly acquiring the geolocations mate
        geolocations = obtaining_new_geolocations(bid[-1])
        x_and_y = [
            geolocations[0],
            geolocations[1]
        ]
        print(x_and_y)
        bid.extend(x_and_y)

    bid_lenght = len(active_bids_list[0])
    all_or_not = all(len(lst) == bid_lenght for lst in active_bids_list)

    if all_or_not:
        return active_bids_list
    else:
        print("Something wrong with geolocations\n")
        sys.exit(1)




# [1] Entering the sam.gov website and
# expropriating each individual bid
sam_url = 'https://sam.gov/search/?index=opp&page=1&pageSize=25&sort=-modifiedDate&sfm%5BsimpleSearch%5D%5BkeywordRadio%5D=ALL&sfm%5Bstatus%5D%5Bis_active%5D=true&sfm%5BserviceClassificationWrapper%5D%5Bnaics%5D%5B0%5D%5Bkey%5D=23622&sfm%5BserviceClassificationWrapper%5D%5Bnaics%5D%5B0%5D%5Bvalue%5D=23622%20-%20Commercial%20and%20Institutional%20Building%20Construction&sfm%5BplaceOfPerformance%5D%5Bstate%5D%5B0%5D%5Bkey%5D=CA&sfm%5BplaceOfPerformance%5D%5Bstate%5D%5B0%5D%5Bvalue%5D=CA%20-%20California'
success = entering_sam_gov(sam_url)


# [2] Creating the geolocations for each
# of the active bids
bids_with_geolocations = acquiring_geolocations(success)
df = pd.DataFrame(bids_with_geolocations)
headers = [
    "BidLink",
    "BidTitle",
    "SolicitationID",
    "RelatedNotice",
    "DepartmentTiers",
    "DepartmentNames",
    "OriginalSetAside",
    "SetAsideCode",
    "ServiceCode",
    "NAICS",
    "Location",
    "X_Coordinates",
    "Y_Coordinates"
]
df.columns = headers
df.to_csv('finalized_sam_gov.csv', mode="w",index=False)





'''
Time Statistics
'''
end_time = time.time()
elapsed_seconds = end_time-start_time
elapsed_minutes = round(elapsed_seconds/60,2)
elapsed_hours = round(elapsed_minutes/60,2)
print(f'\nTotal Seconds to Execute main.py:\nSeconds = {elapsed_seconds}\nMinutes = {elapsed_minutes}\nHours = {elapsed_hours}')

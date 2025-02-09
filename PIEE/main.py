import pandas as pd
import math
import os
import time
import re
import sys
import requests
from geopy.geocoders import Nominatim
from google.oauth2.service_account import Credentials # type: ignore
from googleapiclient.discovery import build  # type: ignore
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

start_time = time.time()

global_bid_turn = 0

def iterating_through_first_results(driver):
    splitted_current_bids = driver.find_element(By.ID,'DataTables_Table_0_info').text.split(" ")
    x = int(splitted_current_bids[1])
    y = int(splitted_current_bids[3])
    total_displayed_bids = y - (x-1)

    bid_turn = 0
    bid_titles = []
    global global_bid_turn


    while bid_turn != total_displayed_bids:

        # Re-locate table and bids
        bid_table = driver.find_element(By.TAG_NAME, 'tbody')
        all_bids = bid_table.find_elements(By.TAG_NAME, 'tr')

        # Locate the current bid link
        td_element = all_bids[bid_turn].find_elements(By.TAG_NAME, 'td')
        link_to_new_page = td_element[0].find_element(By.TAG_NAME, 'a')

        # Scroll to the link and ensure it's clickable
        driver.execute_script("arguments[0].scrollIntoView();", link_to_new_page)

        try:
            # Wait until the link is clickable and then click
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.TAG_NAME, 'a'))
            )
            link_to_new_page.click()
            bid_title = driver.find_element(By.TAG_NAME,'h4').text
            bid_titles.append(bid_title)
        except Exception as e:
            print(f"Error clicking link at bid_turn {bid_turn}: {e}")
            bid_turn += 1
            continue

        # Wait and go back
        time.sleep(2)

        # Click the previous button to return
        previous_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "previous"))
        )
        previous_button.click()
        time.sleep(2)

        # Increment bid_turn
        bid_turn += 1
        global_bid_turn += 1
        print(f'Current Bid #{global_bid_turn}: {bid_titles[bid_turn-1]}')
    

# The function we will use after the first 20 results, fucking poor website design...
def switching_pages(driver_session, current_pages_id):
    
    # Locate the next page button and go to it
    next_page_bar = driver_session.find_element(By.CLASS_NAME,'pagination')
    next_page_button = next_page_bar.find_elements(By.CLASS_NAME,'paginate_button')[2+current_pages_id].find_element(By.TAG_NAME,'a')
    driver_session.execute_script("arguments[0].scrollIntoView(true);", next_page_button)
    time.sleep(2)
    next_page_button.click()
    time.sleep(2)


def iterating_through_other_results(driver, current_pages_id):
    splitted_current_bids = driver.find_element(By.ID,'DataTables_Table_0_info').text.split(" ")
    x = int(splitted_current_bids[1])
    y = int(splitted_current_bids[3])
    total_displayed_bids = y - (x-1)

    bid_turn = 0
    bid_titles = []
    global global_bid_turn

    while bid_turn != total_displayed_bids:

        # Re-locate table and bids
        bid_table = driver.find_element(By.TAG_NAME, 'tbody')
        all_bids = bid_table.find_elements(By.TAG_NAME, 'tr')

        # Locate the current bid link
        td_element = all_bids[bid_turn].find_elements(By.TAG_NAME, 'td')
        link_to_new_page = td_element[0].find_element(By.TAG_NAME, 'a')

        # Scroll to the link and ensure it's clickable
        driver.execute_script("arguments[0].scrollIntoView();", link_to_new_page)

        try:
            # Wait until the link is clickable and then click
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.TAG_NAME, 'a'))
            )
            link_to_new_page.click()
            bid_title = driver.find_element(By.TAG_NAME,'h4').text
            bid_titles.append(bid_title)
        except Exception as e:
            print(f"Error clicking link at bid_turn {bid_turn}: {e}")
            bid_turn += 1
            continue

        # Wait and go back
        time.sleep(2)

        # Click the previous button to return
        previous_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "previous"))
        )
        previous_button.click()
        time.sleep(2)

        switching_pages(driver, current_pages_id)

        # Increment bid_turn
        bid_turn += 1
        global_bid_turn += 1
        print(f'Current Bid #{global_bid_turn}: {bid_titles[bid_turn-1]}')


def extracting_solicitation_numbers(driver):
    
    # Re-locate table and bids
    bid_table = driver.find_element(By.TAG_NAME, 'tbody')
    all_bids = bid_table.find_elements(By.TAG_NAME, 'tr')
    solicitation_numbers = []

    # Locate the current bid link
    for bid in all_bids:
        solicitation_numbers.append(bid.find_element(By.TAG_NAME,'a').text)

    return solicitation_numbers


def next_page(driver, current_page_id):

    # Locate the next page button and go to it
    next_page_bar = driver.find_element(By.CLASS_NAME,'pagination')
    next_page_button = next_page_bar.find_elements(By.CLASS_NAME,'paginate_button')[2+current_page_id].find_element(By.TAG_NAME,'a')
    driver.execute_script("arguments[0].scrollIntoView(true);", next_page_button)
    time.sleep(2)
    next_page_button.click()
    time.sleep(2)

def allocate_into_google_sheets(list_of_attributes):
    
    SERVICE_ACCOUNT_FILE = "wesonder-4e2319ab4c38.json"
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)

    # Google Sheet ID and range
    SPREADSHEET_ID = '1k0Ga6AGMw3uTNXXeX34PUy7J1bBXOvQ_Q8pQ0LgV_rY'
    range_to_update = 'Sheet1!A1'
    body = {
        "values":list_of_attributes
    } 

    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=range_to_update,
        valueInputOption="RAW",
        body=body
    ).execute()


# 1 - Webscraping all active bids from PIEE URL
def webscraping_piee_website(piee_url):
    driver = webdriver.Chrome()
    driver.get(piee_url)
    time.sleep(2)

    # Locate the Search button in the navbar
    piee_navbar = driver.find_element(By.CSS_SELECTOR,"ul.navbar-nav")
    navbar_items = piee_navbar.find_elements(By.TAG_NAME,"li")
    search_button = navbar_items[0]
    search_button.click()
    time.sleep(2)

    # First input
    naics_input = driver.find_element(By.ID, "naics")
    naics_input.send_keys("236220")

    # Second input
    dropdown = Select(driver.find_element(By.ID, "status"))
    dropdown.select_by_value("O")
    time.sleep(2)

    # Search results
    search_link = driver.find_element(By.ID, "search")
    search_link.click()
    time.sleep(2)

    # Locate the total bids and iterate through each
    total_bids_result = int(driver.find_element(By.TAG_NAME,'h3').text.split(' ')[2][1:])
    total_pages = math.ceil(total_bids_result/20)
    current_pages = 1

    # This is the list we will use for unique url instances
    all_solicitation_numbers = []
    all_solicitation_numbers.extend(extracting_solicitation_numbers(driver))

    while current_pages != total_pages:

        # Page identification
        current_page_id = current_pages - 1

        # Change to the next page
        next_page(driver, current_page_id)

        # Let's approach this faster by using unique URLs
        solicitations = extracting_solicitation_numbers(driver)
        all_solicitation_numbers.extend(solicitations)

        current_pages += 1

    # Close the driver
    driver.quit()

    return all_solicitation_numbers



# 2 - Allocating PIEE Active bids into a Google Sheets spreadsheet
def piee_active_bids_webscraping(piee_active_bids):

    url_sample = "https://piee.eb.mil/sol/xhtml/unauth/search/oppMgmtLink.xhtml?solNo="

    # PIEE active bids
    piee_bids = []

    for solicitation_url in piee_active_bids[:]:
        
        functional_url = f"{url_sample}{solicitation_url}"

        response = requests.get(functional_url)
        soup = BeautifulSoup(response.content,'html.parser')

        # Acquire all of the attributes of your choice, starting with SolicitationNumber
        input_element = soup.find('input', {'id': 'solicitationNumber'})
        solicitation_value = input_element.get('value')
        print(solicitation_value)

        # NoticeType
        notice_type_element = soup.find('input', {'id': 'noticeType'}).get('value')
        print(notice_type_element)

        # DueDate
        due_date = soup.find('input', {'id': 'datetimepicker'}).get('value')
        print(due_date)

        # SetAsideCode
        set_aside_code = soup.find('select', {'id':'setAsideCode'}).find('option', {'selected': 'selected'}).text
        print(set_aside_code)

        # ContactName
        contact_name = soup.find('input', {'id': 'contactName'}).get('value')
        print(contact_name)

        # Description
        description = soup.find('textarea', {'id':'description'}).text
        print(description)

        # Subject
        subject = soup.find('input', {'id':'subject'}).get('value')
        print(subject)
        
        # PostingDate
        posting_date = soup.find('input', {'id':'postingDate'}).get('value')
        print(posting_date)

        # ProductServiceCode
        product_service_code = soup.find('input',{'id':'productOrServiceCode'}).get('value')
        print(product_service_code)

        # NAICS
        naics_code = soup.find('input',{'id':'naics'}).get('value')
        print(naics_code)

        # PlaceOfPerformance
        place_of_performance = soup.find('input',{'id':'placeOfPerformanceZipCode'}).get('value')
        print(place_of_performance)

        # Address
        address = soup.find('textarea', {'id':'placeOfPerformance'}).text
        print(address)

        # ContractingOfficeDoDAAC
        dodaac = soup.find('select', {'id':'contractingOfficeDodaac'}).find('option', {'selected': 'selected'}).text
        print(dodaac)

        # ContractingOfficeName
        office_name = soup.find('input',{'id':'contractingOfficeName'}).get('value')
        print(office_name)

        # ContractingOfficeAddress 
        office_address = soup.find('textarea', {'id':'contractingOfficeAddress'}).text
        print(office_address)

        print(f'{functional_url}\n')

        collected_data = [
            functional_url,
            solicitation_value,
            notice_type_element,
            due_date,
            set_aside_code,
            contact_name,
            description,
            subject,
            posting_date,
            product_service_code,
            naics_code,
            place_of_performance,
            address,
            dodaac,
            office_name,
            office_address
        ]

        collected_data = ["none" if item == "" else item for item in collected_data]

        piee_bids.append(collected_data)

    return piee_bids
    


# 3 - Reading the Google Spreadsheet containing all bids
def reading_piee_active_bids():
    SERVICE_ACCOUNT_FILE = "wesonder-4e2319ab4c38.json"
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)

    # Google Sheet ID and range
    SPREADSHEET_ID = '1k0Ga6AGMw3uTNXXeX34PUy7J1bBXOvQ_Q8pQ0LgV_rY'
    RANGE = 'Sheet1!A:P' 

    # Show bids
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE
    ).execute()

    rows = result.get('values', [])
    
    return rows



# 3 - Geolocation Acquisition
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



# 3 - Split string based on first appearance of five digits
def split_string_on_five_digits(input_string):
    # Find all occurrences of 5 consecutive digits
    matches = list(re.finditer(r'\d{5}', input_string))
    if len(matches) < 2:
        # If there are fewer than 2 occurrences, return the original string as is
        return input_string

    # Get the penultimate match
    penultimate_match = matches[-2]
    end = penultimate_match.end()

    # Split the string at the penultimate match
    return input_string[end:]


# 3 - Acquiring Geolocations
def acquiring_geolocations(list_of_bids):
    
    for bid in list_of_bids:
        
        geolocations = obtaining_new_geolocations(bid[-4])

        if geolocations[0] != 0:
            x_and_y_coord  = [
                geolocations[0],
                geolocations[1]
            ]
            bid.extend(x_and_y_coord)
            print(x_and_y_coord)
        
        else:
            other_address = bid[-1]
            new_string = split_string_on_five_digits(other_address)
            new_string = " ".join(
                new_string.split(" ")[1:]
            )
            geolocations_2 = obtaining_new_geolocations(new_string)
            x_and_y_coord_2 = [
                geolocations_2[0],
                geolocations_2[1]
            ]
            bid.extend(x_and_y_coord_2)
            print(x_and_y_coord_2)

        if len(bid) != 18:
            print(bid)


    first_length = len(list_of_bids[0])
    all_the_same = all(len(lst) == first_length for lst in list_of_bids)
    
    if all_the_same:
        return list_of_bids
    
    else:
        print("Something wrong with geolocations\n")
        sys.exit(1)




def allocation_to_csv(list_of_lists):

    headers = [
        "functional_url",
        "solicitation_value",
        "notice_type_element",
        "due_date",
        "set_aside_code",
        "contact_name",
        "description",
        "subject",
        "posting_date",
        "product_service_code",
        "naics_code",
        "place_of_performance",
        "address",
        "dodaac",
        "office_name",
        "office_address",
        "X_Coordinates",
        "Y_Coordinates"
    ]

    df = pd.DataFrame(list_of_lists,columns=headers)
    df.to_csv('finalized_piee_bids.csv',index=False)





# [1] PIEE Webscraping
piee_url = 'https://piee.eb.mil/sol/xhtml/unauth/index.xhtml'
piee_active_bids_urls = webscraping_piee_website(piee_url)
piee_bids = piee_active_bids_webscraping(piee_active_bids_urls)
updated_active_bids = acquiring_geolocations(piee_bids)
allocation_to_csv(updated_active_bids)




end_time = time.time()
elapsed_seconds = end_time-start_time
elapsed_minutes = round(elapsed_seconds/60,2)
elapsed_hours = round(elapsed_minutes/60,2)
print(f'Total Seconds to Execute main.py:\nSeconds = {elapsed_seconds}\nMinutes = {elapsed_minutes}\nHours = {elapsed_hours}')

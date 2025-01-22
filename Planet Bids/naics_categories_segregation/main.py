import pandas as pd
import time
import sys
import re
from bs4 import BeautifulSoup
from google.oauth2.service_account import Credentials # type: ignore
from googleapiclient.discovery import build  # type: ignore
from datetime import date, datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


start_time = time.time()


# Accessing Planetbids Urls
def opening_webdriver(url, alleged_ab, county, x_coord, y_coord):

    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)

    functionality_id = ""
    active_bids = []

    try:

        # In case the URL is no longer valid
        try:
            page_source_2 = driver.page_source
            soup_2 = BeautifulSoup(page_source_2, "html.parser")
            section_heading = soup_2.find(class_="section-heading").text
            if section_heading == "This is not a valid PlanetBids agency portal":
                driver.quit()
                return active_bids, len(active_bids), "Kinda"
        
        except:
            pass
        
        
        # Wait until the body of bids appears before acquiring the page source
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME,'tbody'))
        )
        functionality_id = "Yes"
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # SiteAwardingBody
        site_awarding_body = soup.find('h4').text
        
        # Find the <tbody> where all bids are located, followed by <td>
        tbody = soup.find('tbody')
        all_tr = tbody.find_all('tr')

        # Iterate through each <tr> tag (each <tr> reprents a bid, regardless of status)
        for tr_tag in all_tr:
            all_td = tr_tag.find_all('td')
            tr_attribute_number = tr_tag.get('rowattribute')

            for td_tag in all_td:
                if td_tag.get('title') == 'Bidding':

                    # Acquire the link for the bid itself
                    bid_url = f"{url.replace('bo-search','bo-detail')}/{tr_attribute_number}"
                                    # Acquire the rest of the bid attributes
                    posted_date = all_td[0].text
                    bid_title = all_td[1].text
                    invitation_id = all_td[2].text
                    due_date_string = re.sub(r'\s+', ' ', all_td[3].text.strip()).split(" ")
                    due_date = due_date_string[0]
                    due_time = due_date_string[1]
                    status = all_td[5].text
                    submission_method = all_td[6].text

                    other_attributes = [
                        alleged_ab,
                        county,
                        x_coord,
                        y_coord
                    ]

                    active_bid_attributes_ugly = [
                        bid_url,
                        site_awarding_body,
                        posted_date,
                        bid_title,
                        invitation_id,
                        due_date,
                        due_time,
                        status,
                        submission_method
                    ]

                    active_bids_attributes_pretty = [
                        re.sub(r'\s+', ' ', string.strip()) for string in active_bid_attributes_ugly
                    ]

                    active_bids_attributes_pretty.extend(other_attributes)

                    active_bids_attributes_pretty = [
                        str(item) for item in active_bids_attributes_pretty
                    ]

                    active_bids.append(active_bids_attributes_pretty)

    except Exception as exe:
        print(exe)
        functionality_id = "No"
        sys.exit(1)



    # Finish the selenium session and return the active bids of that url
    driver.quit()   
    return active_bids, len(active_bids), functionality_id



def google_sheets_allocation(list_of_attributes):

    SERVICE_ACCOUNT_FILE = "wesonder-4e2319ab4c38.json"
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)

    # Google Sheet ID and range
    SPREADSHEET_ID = '197FCnOxTIa_rnXTc_0oapI53jkrPNrP7JA_n94fjUxI'
    RANGE = 'Sheet1!A:M' 

    # Prepare the data to append 
    body = {
        'values': list_of_attributes
    }

    # Append the data to the Google Sheet
    sheet = service.spreadsheets()
    response = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE,
        valueInputOption="RAW",
        body=body
    ).execute()


def planetbid_site_summary(list_of_attributes):
    
    SERVICE_ACCOUNT_FILE = "wesonder-4e2319ab4c38.json"
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)

    # Google Sheet ID and range
    SPREADSHEET_ID = '1Wu3WiKnYlJ_tp-TdfKxA9OjWqrQK0BZfVlXDNe2Ikik'
    RANGE = 'Sheet1!A:M' 

    # Prepare the data to append 
    body = {
        'values': [list_of_attributes]
    }

    # Append the data to the Google Sheet
    sheet = service.spreadsheets()
    response = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE,
        valueInputOption="RAW",
        body=body
    ).execute()


# Begins webscraping
def planetbids_iterations(csv_file, todays_date):
    df_pb = pd.read_csv(csv_file)
    i = 0

    for index, row in enumerate(df_pb.iloc[i:].itertuples(index=False), start=i):

        if index % 5 == 0 and index != 0:
            time.sleep(28)
        
        url = row.WebLink
        awarding_body = row.AwardingBody
        county = row.County
        x_coord = row.X_Coordinates
        y_coord = row.Y_Coordinates

        # Acquire the bid attributes
        active_bids, total_bids, yes_or_no = opening_webdriver(
            url,
            awarding_body,
            county,
            x_coord,
            y_coord
        )

        if active_bids:

            # Allocate them into Google Sheets
            google_sheets_allocation(active_bids)

        # Record an account of this planetbids site webscrap
        planetbids_site_record = [
            url,
            awarding_body,
            county,
            x_coord,
            y_coord,
            total_bids,
            todays_date
        ]
        planetbid_site_summary(planetbids_site_record)
            

        print(f"Bid {index}\nActive Bids: {active_bids}\nTotal Bids: {total_bids}\nWorked? {yes_or_no}\n")


def active_bids_reading():

    SERVICE_ACCOUNT_FILE = "wesonder-4e2319ab4c38.json"
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)

    # Google Sheet ID and range
    SPREADSHEET_ID = '197FCnOxTIa_rnXTc_0oapI53jkrPNrP7JA_n94fjUxI'
    RANGE = 'Sheet1!A:M' 

    # Show bids
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE
    ).execute()

    rows = result.get('values', [])
    
    return rows







def refining_planetbids_sites(data):
    SERVICE_ACCOUNT_FILE = "wesonder-4e2319ab4c38.json"
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)

    # Google Sheet ID and range
    SPREADSHEET_ID = '1Wu3WiKnYlJ_tp-TdfKxA9OjWqrQK0BZfVlXDNe2Ikik'
    range_to_update = 'Sheet3!A1'
    body = {
        "values":data
    } 

    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=range_to_update,
        valueInputOption="RAW",  # Input data as-is without formatting
        body=body
    ).execute()



def remove_repeating_sites(planetbids_sites_list):
        
    new_list = []
    unique_urls = []
    
    for index, bid in enumerate(planetbids_sites_list, start=0):
        
        if bid[0] not in unique_urls:
            unique_urls.append(bid[0])
            new_list.append(bid)


    refining_planetbids_sites(new_list)


# Obsolote
def removing_repeating_sites_csv(csv_file):

    df = pd.read_csv(csv_file)
    df_unique = df.drop_duplicates(subset="WebLink",keep="first")
    df_unique.to_csv('absolute_planetbids_sites.csv', index=False)
    


# 2 - Allocation of NAICS Segregation into Google Sheets
def naics_allocation(list_of_attributes):
    
    SERVICE_ACCOUNT_FILE = "wesonder-4e2319ab4c38.json"
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)

    # Google Sheet ID and range
    SPREADSHEET_ID = '197FCnOxTIa_rnXTc_0oapI53jkrPNrP7JA_n94fjUxI'
    RANGE = 'Sheet2!A:P' 

    # Prepare the data to append 
    body = {
        'values': list_of_attributes
    }

    # Append the data to the Google Sheet
    sheet = service.spreadsheets()
    response = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE,
        valueInputOption="RAW",
        body=body
    ).execute()



# 2 - Actually webscraping the site to obtain all the attributes of it
def actually_webscraping_individual_bid(url):

    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)

    try:
        
        # Wait until the body of bids appears before acquiring the page source
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME,'h3'))
        )
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        
        detail_wrapper = soup.find('div',class_="bid-detail-wrapper")
        div_within = detail_wrapper.find('div',class_="ember-view")
        titles = div_within.find_all('div',class_="bid-detail-item-title")
        definitions = div_within.find_all('div',class_="bid-detail-item-value")

        naics_codes_involved = []

        for title, definition in zip(titles, definitions):
            title_string = re.sub(r'\s+', ' ', title.text.strip())
            if title_string == "Categories":
                lines = [text.strip() for text in definition.stripped_strings]
                naics_codes_involved.extend(lines)
            else:
                pass

        driver.quit()

        return naics_codes_involved

    except Exception as exe:
        driver.quit()
        return []



# 2 - Webscraping each individual bid to segregate them based on NAICS codes
def naics_segregation(list_of_active_bids):

    list_of_active_bids = list_of_active_bids[1:]
    bids = [bid for bid in list_of_active_bids]
    urls_to_webscrap = [bid[0] for bid in list_of_active_bids]
    
    for index, url in enumerate(urls_to_webscrap[:]):

        if index % 4 == 0 and index != 0:
            time.sleep(30)

        naics_codes = actually_webscraping_individual_bid(url)

        if naics_codes:
            
            # The first new column is a string containing all of the categories with complete names and codes
            naics_categories_complete = ";".join(naics_codes)

            # The second new column is a string containing solely the naics codes
            naics_codes_only_list = [thing.split(' - ')[0] for thing in naics_codes]
            naics_codes_only_string = ";".join(naics_codes_only_list)

            # The third and final column is a string containing solely the naics names
            naics_names_only_list = [thing.split(' - ')[1] for thing in naics_codes]
            naics_names_only_string = ";".join(naics_names_only_list)

            bids[index].append(naics_categories_complete)
            bids[index].append(naics_codes_only_string)
            bids[index].append(naics_names_only_string)

            list_of_attributes = [bids[index]]

            naics_allocation(list_of_attributes)
        
        print(f"Iteration {index}\nNAICS Codes: {naics_codes}")


# 3 - We need to acquire a list with the active bids segregated by NAICS for 3 (retrieve the missing ones)
def naics_segregated_bids():

    SERVICE_ACCOUNT_FILE = "wesonder-4e2319ab4c38.json"
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)

    # Google Sheet ID and range
    SPREADSHEET_ID = '197FCnOxTIa_rnXTc_0oapI53jkrPNrP7JA_n94fjUxI'
    RANGE = 'Sheet3!A:M' 

    # Show bids
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE
    ).execute()

    rows = result.get('values', [])
    
    return rows



# 4 - A list containing all Planetbids Sites and their latest webscraping date
def planetbids_sites_google_sheets():

    SERVICE_ACCOUNT_FILE = "wesonder-4e2319ab4c38.json"
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)

    # Google Sheet ID and range
    SPREADSHEET_ID = '1Wu3WiKnYlJ_tp-TdfKxA9OjWqrQK0BZfVlXDNe2Ikik'
    RANGE = 'Sheet1!A:G' 

    # Show bids
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE
    ).execute()

    rows = result.get('values', [])
    
    return rows



# 4 - For when the Planetbids site had 0 active bids
def zero_bids_attach(data):
    
    SERVICE_ACCOUNT_FILE = "wesonder-4e2319ab4c38.json"
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)

    # Google Sheet ID and range
    SPREADSHEET_ID = '1Wu3WiKnYlJ_tp-TdfKxA9OjWqrQK0BZfVlXDNe2Ikik'
    range_to_update = 'Sheet2!A1'
    body = {
        "values":data
    } 

    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=range_to_update,
        valueInputOption="RAW",  # Input data as-is without formatting
        body=body
    ).execute()
    


# 4 - Assigning a webscraping date to Planetbids Sites with Zero bids
def active_bids_arrangement_no_bids(planetbids_sites, date_today, four_days_after):

    # Assign the date for the empty planetbids site

    data_transfer = []

    for index, bid in enumerate(planetbids_sites, start=1):
        if bid[6] == date_today and bid[5] == "0":
            bid.append(four_days_after)
            data_transfer.append(bid)
            print(index)

        else:
            bid.append("")
            data_transfer.append(bid)

    zero_bids_attach(data_transfer)





'''
Function Inputs: These shall always remain active (non-commented)
'''
# Active bids - Read - 2
active_bids_read = active_bids_reading()

planetbids_sites_original = 'https://storage.googleapis.com/wesonder_databases/Planetbids/absolute_planetbids_sites.csv'
date_today = str(date.today().strftime("%m/%d/%Y"))
four_days_after = str((datetime.now()+timedelta(days=4)).strftime("%m/%d/%Y"))
yesterday_date = str((datetime.now()-timedelta(days=1)).strftime("%m/%d/%Y"))

# NAICS segregated active bids - Read - 3
naics_segregation_bids = naics_segregated_bids()

# Planetbids Sites - Read - 4
planetbids_sites_read = planetbids_sites_google_sheets()




'''
Functional Approaches
'''
# Initial and Main Planetbids Webscraping - 1
#planetbids_iterations(planetbids_sites_original, date_today)


# NAICS Webscraping - 2
#naics_segregation(active_bids_read)

# NAICS Follow-up - 3
#naics_segregation(naics_segregation_bids)

# Webscraping Schedule Algorithm - 4
active_bids_arrangement_no_bids(planetbids_sites_read, date_today, four_days_after)






'''
Obsolote Functions
'''
# Cleaning Planetbids Repated Sites - Obsolote
#remove_repeating_sites(planetbids_sites_read)


# Cleaning Original Planetbids Sites CSV
#csv_file = "refined_planetbids_sites.csv"
#removing_repeating_sites_csv(csv_file)


# Planetbids Webscraping Schedule - Zero Active Bids Scenario
#active_bids_arrangement_no_bids(planetbids_sites_read, date_today, four_days_after)


# Planetbids Webscraping Schedule - Other Bids
#active_bids_arrangement_other_bids(planetbids_sites_read, active_bids_read)
















'''
Time Statistics
'''
end_time = time.time()
elapsed_time = end_time - start_time
elapsed_hours = round((elapsed_time / 60 / 60), 3)
print(f'Total Hours to Execute: {elapsed_hours}')
import pandas as pd
import time
import sys
import re
from bs4 import BeautifulSoup
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build  # type: ignore
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
    RANGE = 'Sheet1!A:L' 

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

    




# Outset and Identificators
planetbids_sites = 'https://storage.googleapis.com/wesonder_databases/Planetbids/refined_planetbids_sites.csv'
df_pb = pd.read_csv(planetbids_sites)
i = 1

for index, row in enumerate(df_pb.iloc[i:i+1].itertuples(index=False), start=i):

    if index % 5 == 0 and index != 0:
        time.sleep(26)
    
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
        

    print(f"Bid {index}\nActive Bids: {active_bids}\nTotal Bids: {total_bids}\nWorked? {yes_or_no}\n")




# Calculate elapsed time
end_time = time.time()
elapsed_time = end_time - start_time
elapsed_hours = round((elapsed_time / 60 / 60), 2)
print(f'Total Hours to Execute: {elapsed_hours}')

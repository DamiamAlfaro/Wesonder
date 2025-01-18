import pandas as pd
import time
import re
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

start_time = time.time()

def site_html_webscrap(url):

    try:
        # Initialize Chrome WebDriver
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run Chrome in headless mode
        options.add_argument('--disable-gpu')  # Disable GPU acceleration (required for headless mode on Windows)
        options.add_argument('--disable-extensions')  # Disable extensions for faster loading
        options.add_argument('--no-sandbox')  # Security sandbox can be disabled (usually for non-production use)
        options.add_argument('--disable-dev-shm-usage')  # Avoid shared memory issues
        options.add_argument('--window-size=1920,1080')  # Set viewport size explicitly
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36')  # Mimic a real browser user-agent
        options.add_argument('--start-maximized')  # Start the browser maximized (simulating a normal environment)
        driver = webdriver.Chrome(options=options)
        driver.get(url)

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

        return naics_codes_involved

    except Exception as exe:
        return []



# The csv is from Google Cloud, which shall be uploaded manually before executing this program.
active_bids_csv = 'https://storage.googleapis.com/wesonder_databases/Planetbids/planetbids_active_bids.csv'

# Resulting csv files from this program
new_active_bids_csv = 'refined_planetbids_active_bids.csv'
faulty_new_active_bids_csv = 'faulty_planetbids_active_bids.csv'
df = pd.read_csv(active_bids_csv)
total_rows = len(df)

i = 0


for index, row in df.iloc[i:].iterrows():

    allegedab = row['AllegedAwardingBody']
    weblink = row['WebLink']
    county = row['County']
    x_coord = row['X_Coordinates']
    y_coord = row['Y_Coordinates']
    bid_url = row['BidUrl']
    bid_awarding_body = row['BidAwardingBody']
    bid_posted_date = row['BidPostedDate']
    bid_title = row['BidTitle']
    bid_invitation_id = row['BidInvitationID']
    bid_due_date = row['BidDueDate']
    bid_status = row['BidStatus']
    bid_submission_method = row['BidSubmissionMethod']

    print(f'Row #{index} - BidUrl: {bid_url} - Progress: {round((index/total_rows)*100,2)}%')

    # A list of NAICS categories that the bid pertains to.
    categories_list = site_html_webscrap(bid_url) 

    if categories_list:

        # The first new column is a string containing all of the categories with complete names and codes
        naics_categories_complete = ";".join(categories_list)

        # The second new column is a string containing solely the naics codes
        naics_codes_only_list = [thing.split(' - ')[0] for thing in categories_list]
        naics_codes_only_string = ";".join(naics_codes_only_list)

        # The third and final column is a string containing solely the naics names
        naics_names_only_list = [thing.split(' - ')[1] for thing in categories_list]
        naics_names_only_string = ";".join(naics_names_only_list)

        # Now, we allocate these three new values of each bid link into the respective new three columns
        new_data = pd.DataFrame({
            "AllegedAwardingBody": [allegedab],
            "WebLink": [weblink],
            "County": [county],
            "X_Coordinates": [x_coord],
            "Y_Coordinates": [y_coord],
            "BidUrl": [bid_url],
            "BidAwardingBody": [bid_awarding_body],
            "BidPostedDate": [bid_posted_date],
            "BidTitle": [bid_title],
            "BidInvitationID": [bid_invitation_id],
            "BidDueDate": [bid_due_date],
            "BidStatus": [bid_status],
            "BidSubmissionMethod": [bid_submission_method],
            "NAICS_Complete": [naics_categories_complete],
            "NAICS_Codes": [naics_codes_only_string],
            "NAICS_Names": [naics_names_only_string]
        })


        if not os.path.isfile(new_active_bids_csv):
            new_data.to_csv(new_active_bids_csv, index=False, header=True, mode='w')

        else:
            new_data.to_csv(new_active_bids_csv, index=False, header=False, mode='a')

    else:

        faulty_data = pd.DataFrame({
            "AllegedAwardingBody": [allegedab],
            "WebLink": [weblink],
            "County": [county],
            "X_Coordinates": [x_coord],
            "Y_Coordinates": [y_coord],
            "BidUrl": [bid_url],
            "BidAwardingBody": [bid_awarding_body],
            "BidPostedDate": [bid_posted_date],
            "BidTitle": [bid_title],
            "BidInvitationID": [bid_invitation_id],
            "BidDueDate": [bid_due_date],
            "BidStatus": [bid_status],
            "BidSubmissionMethod": [bid_submission_method]
        })

        if not os.path.isfile(faulty_new_active_bids_csv):
            faulty_data.to_csv(faulty_new_active_bids_csv, index=False, header=True, mode='w')

        else:
            faulty_data.to_csv(faulty_new_active_bids_csv, index=False, header=False, mode='a')


end_time = time.time()
elapsed_seconds = end_time-start_time
elapsed_minutes = round(elapsed_seconds/60,2)
elapsed_hours = round(elapsed_minutes/60,2)
print(f'Total seconds to execute main.py:\nSeconds = {elapsed_seconds}\nMinutes = {elapsed_minutes}\nHours = {elapsed_hours}')

import pandas as pd
import time
import re
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

initial_time = time.time()
total_active_bids = 0

def allocate_csv(ab, weblink, county, x_coord, y_coord, active_bids_list):
    
    file_name = 'planetbids_active_bids.csv'

    df = pd.DataFrame({
        "AllegedAwardingBody":[ab],
        "WebLink":[weblink],
        "County":[county],
        "X_Coordinates":[x_coord],
        "Y_Coordinates":[y_coord],
        "BidUrl":[active_bids_list[0]],
        "BidAwardingBody":[active_bids_list[1]],
        "BidPostedDate":[active_bids_list[2]],
        "BidTitle":[active_bids_list[3]],
        "BidInvitationID":[active_bids_list[4]],
        "BidDueDate":[active_bids_list[5]],
        "BidStatus":[active_bids_list[6]],
        "BidSubmissionMethod":[active_bids_list[7]]
    })

    if not os.path.isfile(file_name):
        df.to_csv(file_name, index=False, header=True, mode='w')

    else:
        df.to_csv(file_name, index=False, header=False, mode='a')



def site_html_webscrap(url):

    global total_active_bids

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

    # Wait until the body of bids appears before acquiring the page source
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME,'tbody'))
    )
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # SiteAwardingBody
    site_awarding_body = soup.find('h4').text
    
    # Find the <tbody> where all bids are located, followed by <td>
    tbody = soup.find('tbody')
    all_tr = tbody.find_all('tr')
    active_bids = []

    # Iterate through each <tr> tag (each <tr> reprents a bid, regardless of status)
    for tr_tag in all_tr:
        all_td = tr_tag.find_all('td')
        tr_attribute_number = tr_tag.get('rowattribute')

        for td_tag in all_td:
            if td_tag.get('title') == 'Bidding':

                total_active_bids += 1

                # Acquire the link for the bid itself
                bid_url = f"{url.replace('bo-search','bo-detail')}/{tr_attribute_number}"

                # Acquire the rest of the bid attributes
                posted_date = all_td[0].text
                bid_title = all_td[1].text
                invitation_id = all_td[2].text
                due_date = all_td[3].text
                status = all_td[5].text
                submission_method = all_td[6].text

                active_bid_attributes_ugly = [
                    bid_url,
                    site_awarding_body,
                    posted_date,
                    bid_title,
                    invitation_id,
                    due_date,
                    status,
                    submission_method
                ]
                

                active_bids_attributes_pretty = [
                    re.sub(r'\s+', ' ', string.strip()) for string in active_bid_attributes_ugly
                ]

                active_bids.append(active_bids_attributes_pretty)

    # Finish the selenium session and return the active bids of that url
    driver.quit()   
    return active_bids


    


# Load URLs from Google Cloud Storage
planetbids_sites_csv = 'https://storage.googleapis.com/wesonder_databases/Planetbids/refined_planetbids_sites.csv'
df = pd.read_csv(planetbids_sites_csv)
i = 0

for index, row in df.iloc[i:i+10].iterrows():  # Adjust the number of rows as needed
    awarding_body = row['AwardingBody']
    weblink = row['WebLink']
    county = row['County']
    x_coord = row['X_Coordinates']
    y_coord = row['Y_Coordinates']

    try:
        active_bids = site_html_webscrap(weblink)  # Return a list with all active bids

        # Allocate the active bid list into csv
        for active_bid in active_bids:
            allocate_csv(
                awarding_body,
                weblink,
                county,
                x_coord,
                y_coord,
                active_bid
            )

        
        print(
            f"Bid Site #{index} Complete\nURL: {weblink}\nAwarding Body: {awarding_body}\nTotal Bids: {len(active_bids)}"
            )

    except Exception as exe:

        print(
            f"Bid Site #{index} Incomplete\nURL: {weblink}\nAwarding Body: {awarding_body}"
        )
        print(exe)
        break


print(f'\nTotal Active Bids: {total_active_bids}')
end_time = time.time()
elapsed_time = end_time-initial_time
print(f'Total Seconds to Execute main.py: {elapsed_time}')

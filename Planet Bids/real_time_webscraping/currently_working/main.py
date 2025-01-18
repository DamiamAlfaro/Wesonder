import pandas as pd
import time
import sys
import requests
import re
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


start_time = time.time()


# Accessing Planetbids Urls
def opening_webdriver(url):

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

    except Exception as exe:
        print(exe)
        functionality_id = "No"
        sys.exit(1)



    # Finish the selenium session and return the active bids of that url
    driver.quit()   
    return active_bids, len(active_bids), functionality_id


# Iterating through the csv file containing all the urls
def planetbids_iteration(csv_file):

    df_pb = pd.read_csv(csv_file)
    i = 0


    for index, row in enumerate(df_pb.iloc[i:i+50].itertuples(index=False), start=i):
        url = row.WebLink
        awarding_body = row.AwardingBody
        county = row.County
        x_coord = row.X_Coordinates
        y_coord = row.Y_Coordinates

        active_bids, total_bids, yes_or_no = opening_webdriver(url)

        print(f"Bid {index}\nActive Bids: {active_bids}\nTotal Bids: {total_bids}\nWorked? {yes_or_no}\n")



# Planetbids csv
planetbids_sites = 'https://storage.googleapis.com/wesonder_databases/Planetbids/refined_planetbids_sites.csv'

# Iterate through planetbids with newly acquired proxies
planetbids_iteration(planetbids_sites)


# Calculate elapsed time
end_time = time.time()
elapsed_time = end_time - start_time
elapsed_hours = round((elapsed_time / 60 / 60), 2)
print(f'Total Hours to Execute: {elapsed_hours}')

import pandas as pd
import time
import sys
import re
import os
from bs4 import BeautifulSoup
from google.oauth2.service_account import Credentials # type: ignore
from googleapiclient.discovery import build  # type: ignore
from datetime import date, datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Memento Mori
start_time = time.time()


# [1.1] Expropriation of active bids and putting
# together the attributes of each of the
# active bids expropriated.
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




# [1.0] Begins webscraping
def planetbids_iterations(csv_file, todays_date):
    df_pb = pd.read_csv(csv_file)
    i = 1

    # Progressively append the bids
    # to a list in order to turn them
    # into a DataFrame at the end.
    bids = []

    for index, row in enumerate(df_pb.iloc[i:3].itertuples(index=False), start=i):

        if index % 5 == 0 and index != 0:
            time.sleep(28)
        
        url = row.WebLink
        awarding_body = row.AwardingBody
        county = row.County
        x_coord = row.X_Coordinates
        y_coord = row.Y_Coordinates

        # [1.1] Acquire the bid attributes, and stratify them 
        # by the desired headers of the csv resulting file.
        active_bids, total_bids, yes_or_no = opening_webdriver(
            url,
            awarding_body,
            county,
            x_coord,
            y_coord
        )

        # If there are any active bids, append their attributes to the csv file
        if active_bids:

            # [1.2] Allocating the expropriated attributes
            # into an organized csv file
            bids.extend(active_bids)

        # Keep a progress record
        print(f"Bid {index}\nActive Bids: {active_bids}\nTotal Bids: {total_bids}\nWorked? {yes_or_no}\n")

    # We will only create a file once the procedure
    # is completed, before that we will only use 
    # DataFrames
    return bids


# [2.2] Cleaning the categories strings
# derived from each one of the url
def cleansing_categories(naics_codes, bids, index):

    # The first new column is a string containing all of 
    # the categories with complete names and codes
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

    return [bids[index]]



# [2.1] - Actually webscraping the site to 
# obtain all the attributes of it
def actually_webscraping_individual_bid(url):

    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(1)

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



# [2.0] - Webscraping each individual bid to 
# segregate them based on NAICS.
def naics_segregation(list_of_active_bids):

    list_of_active_bids = list_of_active_bids[:]
    bids = [bid for bid in list_of_active_bids]
    urls_to_webscrap = [bid[0] for bid in list_of_active_bids]

    new_bids = []
    faulty_bids = []
    
    # Iterate through each url in order to obtain
    # the respective categories for each of the active
    # bids.
    for index, url in enumerate(urls_to_webscrap[:]):

        if index % 4 == 0 and index != 0:
            time.sleep(30)

        # [2.1] Acquiring the Categories from each individual
        # active bid expropriated from Step 1
        naics_codes = actually_webscraping_individual_bid(url)

        # If there are Categories available (sometimes there are not
        # for some weird reason)
        if naics_codes:
            
            # [2.2] Cleaning the categories strings
            list_of_attributes = cleansing_categories(naics_codes, bids, index)

            # A dataframe that will be concatenated with 
            # the dataframe above. This in order to increasingly
            # append new bids with their respective naics categories
            # in every single iteration
            new_bids.extend(list_of_attributes)

        # Some urls will not work
        else:
            faulty_bids.append(url)

        # Keeping a record
        print(f"Iteration {index}\nNAICS Codes: {naics_codes}")


    # Once we collect the urls that worked, we need
    # to do something about the ones that did not work.
    # This is the reason why the use of the code below.
    while len(faulty_bids[:]) != 0:

        # Repeat the same process from [2.1] and [2.2]
        # in order to apply the same functionality to
        # each of the faulty urls.
        for index, url in enumerate(faulty_bids[:]):

            naics_codes = actually_webscraping_individual_bid(url)
            
            if naics_codes:
                list_of_attributes = cleansing_categories(naics_codes, bids, index)
                new_bids.extend(list_of_attributes)
                faulty_bids.remove(url)

    # Once all of them are retrieved, return
    # them onto the next step
    return new_bids




'''
Functional Approaches: We are aiming towards a single action that will
be taking care of the entire program. We want to run the program once
without intervension and acquire the neat result within that single
instance. 
'''
planetbids_sites_original = 'https://storage.googleapis.com/wesonder_databases/Planetbids/absolute_planetbids_sites.csv'
date_today = str(date.today().strftime("%m/%d/%Y"))

# Step [1]: Expropriating the active bids from
# all planetbids sites, along with their attributes
# and allocation into a csv file.
active_bids = planetbids_iterations(planetbids_sites_original, date_today)

# Step [2]: Expropriating the Categories for each
# of the active bids in order to stratify them in
# the future Wesonder display. We are going to use
# the result of Step [1]
active_bids_with_categories = naics_segregation(active_bids)


# Step [3]: Allocate the final result into
# a csv file.
df = pd.DataFrame(active_bids_with_categories)
fields = [
    "bid_url",
    "awarding_body",
    "posted_date",
    "bid_title",
    "solicitation_number",
    "bid_due_date",
    "bid_due_time",
    "bid_status",
    "submission_method",
    "county",
    "x_coordinates",
    "y_coordinates",
    "naics_codes",
    "naics_numeric_codes",
    "naics_written_codes"
]
df.columns = fields
df.to_csv('finalized_planetbids_bids.csv', mode="w",index=False)




'''
Time Statistics
'''
end_time = time.time()
elapsed_time = end_time - start_time
elapsed_hours = round((elapsed_time / 60 / 60), 3)
print(f'Total Hours to Execute: {elapsed_hours}')

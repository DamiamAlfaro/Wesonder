import pandas as pd
import sys
from pandas.errors import EmptyDataError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time



'''
Let's only extract the links with planetbids related content
'''
def extracting_only_planetbids(csv_file):
    
    # Read the csv file using pandas
    df_bidding_sites = pd.read_csv(csv_file, low_memory=False)

    # Extract a column of the websites for planetbids only
    bidding_sites_list = []
    awarding_bodies = []
    planetbids_string = 'vendors.planetbids.com'
    for instance_planetbids,awarding_body in zip(df_bidding_sites.iloc[:,2], df_bidding_sites.iloc[:,0]):
        if planetbids_string in instance_planetbids:
            bidding_sites_list.append(instance_planetbids)
            awarding_bodies.append(awarding_body)


    # Crate the new dataframe and allocate it into a csv file
    df_new = pd.DataFrame({'AwardingBody':awarding_bodies,'WebLink':bidding_sites_list})
    df_new.to_csv('planetbids_sites.csv',index=False)


'''
A mechanism to scroll down over the table display of planetbids used in
planetbid_extraction.py back on August 2024
'''
def scroll_table_container(container, driver,scroll_pause_time=2):
    
    last_height = driver.execute_script("return arguments[0].scrollHeight", container)
    
    while True:
        # Scroll down by a small amount within the container
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", container)
        
        # Wait to load the new content
        time.sleep(scroll_pause_time)
        
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return arguments[0].scrollHeight", container)
        if new_height == last_height:
            break
        last_height = new_height

    result_message = "Round Completed"
    return result_message



'''
This function will embellish strings and allocate them into a csv file for further analysis and research
'''
def string_embellishment_and_allocation(list_of_lists_of_strings):
    
    # Remove the fax numbers, we don't need them, we aren't in the 90s
    pass



'''
The actual web crawling
'''
def webscraping_planetbids(url, awarding_body, external_count: int):

    # Load the webdriver
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)

    # COunt in case the program halts (shall be modify accordingly to the terminal output when halt occurred)
    count = 0
    print(f"Current {awarding_body} Count: {count}")

    # Position yourself within the Planetbids and scroll down over the table containing all bids
    try:
        bid_display_table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'table-overflow-container'))
        )
    
    except:
        print(f"There is something wrong with the site for {awarding_body}")
        sys.exit(1)

    # Scrolls all the way to the bottom of the planet bids display
    scroll_table_container(bid_display_table,driver)

    # Pinpoint the amount of bids in the website for future reference index number
    bids = bid_display_table.find_elements(By.TAG_NAME, 'tr')
    
    # The tr element of the table display to click on
    bid_target = bids[2+count]
    driver.execute_script("arguments[0].scrollIntoView();", bid_target)
    driver.execute_script("arguments[0].click();", bid_target)

    # Bid Title for future usage
    bid_title_element = WebDriverWait(driver,5).until(
        EC.presence_of_element_located((By.CLASS_NAME,'bid-detail-title'))
    )
    bid_title_text = bid_title_element.text
    
    
    # Pinpoint the initial element for the main welcome page
    bid_description = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'bid-detail-wrapper'))
    )

    # Extract the text infomration of the bid of the site for future data analysis
    bid_information_rows = []
    rows_of_infomration = bid_description.find_elements(By.CLASS_NAME,"row")
    for text_row in rows_of_infomration[2:]:
        bid_information_rows.append(text_row.text)

    # The general information of the project; string to be addded later    
    bid_text_information = "|".join(bid_information_rows)

    # Now pinpoint the headers in order to jump/click into the 'Prospective Bidders' tab
    bid_header_tabs = WebDriverWait(driver,5).until(
        EC.presence_of_element_located((By.ID,'detail-navigation'))
    )

    # Click on the Prospective Bidders tab
    try:
        prospective_bidders_tab = WebDriverWait(bid_header_tabs,5).until(
            EC.presence_of_element_located((By.CLASS_NAME,'bidPBs'))
        )
        prospective_bidders_tab.click()
        time.sleep(1)
    except:
        print(f"Something is wrong with the Prospective Bidders tab of {awarding_body}")

    # Extract the datum for each attribute of each prospective bidder (email, address, etc.)
    table_element = driver.find_element(By.TAG_NAME, 'table')
    table_body_element = table_element.find_element(By.TAG_NAME,'tbody')
    table_invidiual_elements = table_body_element.find_elements(By.TAG_NAME,'tr')

    # A list that contains plenty of more lists which each corresponde to an entity's set of attributes
    all_entities = []

    for prospective_bidder_attribute in table_invidiual_elements:

        # Where the entity's attribute are found
        entity_in_question = []

        # Pinpoint every individual td within the tr. By default, the first one is the unique on when it is used singular
        td_element = prospective_bidder_attribute.find_element(By.TAG_NAME,'td')
        information_field = td_element.find_element(By.TAG_NAME,'div')
        singular_attributes = information_field.find_elements(By.TAG_NAME,'div')

        # The name is separated
        entity_name = information_field.find_element(By.CLASS_NAME,'table-address-vendorname')
        entity_in_question.append(entity_name.text)
        
        # Iterate through each singular attribute to extract it
        for attribute in singular_attributes:
            entity_in_question.append(attribute.text)
        
        # Each entity's list should contain 5 attributes: name, address, contact, phone, and email. Or if Fax is included, the length is 6
        all_entities.append(entity_in_question)

    # Append the rest of the important strings (project general information, project name, and awarding body)
    other_important_strings = [bid_text_information, bid_title_text, awarding_body]

    # String embellishment and csv allocation function
    string_embellishment_and_allocation(all_entities, other_important_strings)
    
    # Go back to the bid table display
    driver.back()
    driver.back()
    count += 1
    time.sleep(1)
        











        
    
    






    



'''
Load the file with all planetbids and iterate through each
'''
def reading_csv_with_planetbids(csv_file):

    # Convert it into a Pandas DataFrame
    df_main = pd.read_csv(csv_file)

    # Iterate through the file
    for index, row in df_main.head(1).iterrows():
        
        # Links Row
        link = row['WebLink']
        awarding_body = row['AwardingBody']

        webscraping_planetbids(link, awarding_body, 0)















if __name__ == "__main__":
    
    # Bidding Sites csv file
    bidding_sites_data_csv = "bidding_sites_data.csv"

    # Planetbids Sites csv file
    planetbids_sites = "planetbids_sites.csv"

    reading_csv_with_planetbids(planetbids_sites)

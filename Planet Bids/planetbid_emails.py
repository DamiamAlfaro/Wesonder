import pandas as pd # type: ignore
import sys
from pandas.errors import EmptyDataError# type: ignore
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.common.keys import Keys # type: ignore
from selenium.webdriver.support.ui import WebDriverWait# type: ignore
from selenium.webdriver.support import expected_conditions as EC  # type: ignore
from selenium.common.exceptions import TimeoutException# type: ignore
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
def string_embellishment_and_allocation(list_of_lists_of_strings, other_strings):
    
    # Variables from the first list
    names = []
    street_addresses = []
    cities = []
    states = []
    zip_codes = []
    complete_addresses = []
    contacts = []
    phone_numbers = []
    emails = []

    # Iteration through first list
    for first_list in list_of_lists_of_strings:

        # Remove the fax numbers, we don't need them, we aren't in the 90s
        if len(first_list) == 6:
            first_list.pop(4)
        
        # Identify attributes
        company_name = first_list[0]
        company_address = first_list[1]
        company_contact = first_list[2]
        company_phone = first_list[3]
        company_email = first_list[4]

        # Add the company name
        names.append(company_name.upper())

        # Categorize by Street Address, City, State, Zip Code, and Complete Address. Do it by breaking down the address string into "\n"
        address_split = company_address.split("\n")
        if len(address_split) == 3:
            street_address = f"{address_split[0]} {address_split[1]}"
        else:
            street_address = f"{address_split[0]}"
        
        # Split the last part of address_split (which is always the city, state, and zip code, regardless of Suite # or not)
        second_address_split = address_split[-1].split(" ")
        city = second_address_split[0][:-1] # remove the "," from the end
        state = second_address_split[1]
        zip_code = second_address_split[2]
        complete_address = f"{street_address}, {city} {state}, {zip_code}"

        # Add the location attributes
        street_addresses.append(street_address)
        cities.append(city)
        states.append(state)
        zip_codes.append(zip_code)
        complete_addresses.append(complete_address)

        # Add the contact
        contact_split = company_contact.split(" ")
        contacts.append(contact_split[1])

        # Add the phone number
        phone_split = company_phone.split(" ")
        phone_numbers.append(phone_split[1])

        # Add the emails
        emails.append(company_email)

    
    # Variables from the second list quantitavely correlating to the length of other attributes
    project_name = [other_strings[0] for _ in range(len(names))]
    awarding_bodies = [other_strings[1] for _ in range(len(names))]

    # Creating a dataframe and exporting as csv
    data = {
    "EntityNames": names,
    "StreetAddres": street_addresses,
    "City": cities,
    "State": states,
    "ZipCode": zip_codes,
    "CompleteAddresses": complete_addresses,
    "Contacts": contacts,
    "PhoneNumbers": phone_numbers,
    "Emails": emails,
    "ProjectName": project_name,
    "AwardingBody": awarding_bodies
    }

    df = pd.DataFrame(data)
    df.to_csv("testing.csv",index=False)



        
        
            






    



'''

The actual web crawling
'''
def webscraping_planetbids(url, awarding_body, internal_count):

    # Load the webdriver
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)

    # COunt in case the program halts (shall be modify accordingly to the terminal output when halt occurred)
    print(f"Current {awarding_body} Count: {internal_count}")

    # Identifies if the total number of bids in the municipality increased
    total_bids = driver.find_element(By.CLASS_NAME,"bids-table-filter-message")
    total_bids_text_splitted = total_bids.text.split(" ")
    really_total_bids = int(total_bids_text_splitted[1])
    
    for individual_bid in range(2,really_total_bids+1):

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
        bid_target = bids[individual_bid]

        # Positional awareness
        current_iteration_bid_table = bid_target.text
        print(f"Currently ({individual_bid}) at: {current_iteration_bid_table}")

        
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
        bid_text_information = "|".join(bid_information_rows) # (REJECTED)

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
            print(f"Something is wrong with the Prospective Bidders tab of {current_iteration_bid_table}")
            driver.back()
            continue
            

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
        other_important_strings = [bid_title_text, awarding_body]

        # String embellishment and csv allocation function
        string_embellishment_and_allocation(all_entities, other_important_strings)
        
        # Go back to the bid table display
        driver.back()
        driver.back()
        time.sleep(2)

    
        











        
    
    






    



'''
Load the file with all planetbids and iterate through each
'''
def reading_csv_with_planetbids(csv_file):

    # Convert it into a Pandas DataFrame
    df_main = pd.read_csv(csv_file)

    # Current Count
    count = 0

    # Iterate through the file
    for index, row in df_main[count:].iterrows():
        
        # Links Row
        link = row['WebLink']
        awarding_body = row['AwardingBody']

        webscraping_planetbids(link, awarding_body, index)















if __name__ == "__main__":
    
    # Bidding Sites csv file
    bidding_sites_data_csv = "bidding_sites_data.csv"
    #extracting_only_planetbids(bidding_sites_data_csv)

    # Planetbids Sites csv file
    planetbids_sites = "planetbids_sites.csv"

    reading_csv_with_planetbids(planetbids_sites)

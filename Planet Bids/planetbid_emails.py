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
import re
import os



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
The function that appends to the csv file and creates a new one when there is none
'''
def recording_to_csv(dataframe, csv_file, current_iteration):
    
    # Acquire the directory list of csvfiles
    current_directory = os.listdir()
    
    # Check if the csv file is within the directory
    if csv_file in current_directory:
        
        # If it is, append to the csv file
        dataframe.to_csv(csv_file, mode='a', index=False, header=False)
        print(f"Iteration {current_iteration} appended")

    # If it isn't, then create a new csv file with its title
    else:
        dataframe.to_csv(csv_file, index=False)
        print(f"Iteration {current_iteration} created")





'''
This function will embellish strings and allocate them into a csv file for further analysis and research
'''
def string_embellishment_and_allocation(list_of_lists_of_strings, other_strings, current_iteration):
    
    # Variables from the first list
    names = []
    street_addresses = []
    cities = []
    states = []
    zip_codes = []
    complete_addresses = []
    complete_addresses_nz = []
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
        refined_address_split = address_split[-1].split(",")
        second_address_split = refined_address_split[-1].split(" ")
        
        # Some cities might have more than one word as a name, we need to secure those instances as well, but for now, we know that zip code and state are at the end
        zip_code = second_address_split[-1]
        state = " ".join(second_address_split[1:-1])

        # Convert the state word into the abbreviation
        us_states = [
            "Alabama", "Alaska", "Arizona", "Arkansas", "California",
            "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
            "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
            "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland",
            "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri",
            "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
            "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
            "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
            "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
            "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
        ]

        states_abbreviations = [
            "AL", "AK", "AZ", "AR", "CA",
            "CO", "CT", "DE", "FL", "GA",
            "HI", "ID", "IL", "IN", "IA",
            "KS", "KY", "LA", "ME", "MD",
            "MA", "MI", "MN", "MS", "MO",
            "MT", "NE", "NV", "NH", "NJ",
            "NM", "NY", "NC", "ND", "OH",
            "OK", "OR", "PA", "RI", "SC",
            "SD", "TN", "TX", "UT", "VT",
            "VA", "WA", "WV", "WI", "WY"
        ]

        if state in us_states:
            state = states_abbreviations[us_states.index(state)]
        else:
            pass

        # Now, the rest of the strings within the list are going to be the city no matter the number of remaining strings
        city = refined_address_split[0]

        # Create the complete address for future Google Maps Geolocation acquisition
        complete_address = f"{street_address}, {city}, {state} {zip_code}"
        complete_address_nz = f"{street_address}, {city}, {state}"

        # Add the location attributes
        street_addresses.append(street_address)
        cities.append(city)
        states.append(state)
        zip_codes.append(zip_code)
        complete_addresses.append(complete_address)
        complete_addresses_nz.append(complete_address_nz)

        # Add the contact
        contact_split = company_contact.split(" ")
        contact = " ".join(contact_split[1:])
        contacts.append(contact)

        # Add the phone number
        phone_split = company_phone.split(" ")
        phone_numbers.append(phone_split[1])

        # Add the emails
        emails.append(company_email)

    
    # Variables from the second list quantitavely correlating to the length of other attributes
    project_name = [other_strings[0] for _ in range(len(names))]
    awarding_bodies = [other_strings[1] for _ in range(len(names))]
    bid_all_information = [other_strings[2] for _ in range(len(names))]

    # Creating a dataframe and exporting as csv
    data = {
    "EntityNames": names,
    "StreetAddres": street_addresses,
    "City": cities,
    "State": states,
    "ZipCode": zip_codes,
    "CompleteAddresses": complete_addresses,
    "CompleteAddressNoZip":complete_addresses_nz,
    "Contacts": contacts,
    "PhoneNumbers": phone_numbers,
    "Emails": emails,
    "ProjectName": project_name,
    "AwardingBody": awarding_bodies,
    "BidInformation": bid_all_information
    }

    # Return the df as a variable for the next function
    df = pd.DataFrame(data)
    
    # Convert to csv, either append or create new csv
    csv_title_file = f"{re.sub(r'[^a-zA-Z0-9]', '_', awarding_bodies[0].lower())}.csv"
    recording_to_csv(df,csv_title_file, current_iteration)





def webscraping_planetbids_rowattributes(url, awarding_body, index_number, link_id):

    # Load the webdriver
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)

    # Try to get the table with all bids
    try:
        bid_display_table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'table-overflow-container'))
        )
        
    except:
        print(f"There is something wrong with the site for {awarding_body}")
        return [awarding_body, url]

    # Scroll through the table
    scroll_table_container(bid_display_table,driver)

    # The respective urls with unique rowattribute ids
    rowattribute_id_urls = []

    # Find the rowattribute id's to search them later
    bid_row_attributes = driver.find_elements(By.XPATH,'//tr[@rowattribute]')
    for bid_row_attribute_number in bid_row_attributes:
        bid_url_id = bid_row_attribute_number.get_attribute('rowattribute')

        # Create a link with the rowattribute id number
        new_url = f"https://vendors.planetbids.com/portal/{link_id}/bo/bo-detail/{bid_url_id}"
        rowattribute_id_urls.append(new_url)

    # Assimilate the length of the list of unique rowattribute id urls, same goes for awarding bodies
    main_links = [url for _ in range(len(rowattribute_id_urls))]
    awarding_body_repetition = [awarding_body for _ in range(len(rowattribute_id_urls))]

    # Create and return a dataframe with the columns desired
    df = pd.DataFrame({
        "AwardingBody":awarding_body_repetition,
        "AwardingBodyPBLink":main_links,
        "UniqueBidPBLink":rowattribute_id_urls
        })

    return df



        
'''
Store the rowattribute dataframe into a csv file
'''
def csv_rowattribute_storage(dataframe, awarding_body):
    
    # Allocate to csv
    csv_drop_location = '/Users/damiamalfaro/Desktop/Europe/testing_wesonder/Planetbids/individual_sites/'
    csv_file_name = f"{re.sub(r'[^a-zA-Z0-9]', '_', awarding_body.lower())}.csv"
    dataframe.to_csv(csv_drop_location + csv_file_name,index=False)
        


'''
Store the link and awarding body into a csv file if faulty
'''
def faulty_links(awarding_body, link):

    # Allocate to csv
    csv_drop_location = '/Users/damiamalfaro/Desktop/Europe/testing_wesonder/Planetbids/faulty_individual_sites/'
    csv_file_name = f"{re.sub(r'[^a-zA-Z0-9]', '_', awarding_body.lower())}.csv"

    # Create a new dataframe to store the faulty links with their awarding bodies
    dataframe = pd.DataFrame({"AwardingBody":[awarding_body],"FaultyLink":[link]})
    dataframe.to_csv(csv_drop_location + csv_file_name,index=False)
    

    



'''
OUTSET: Load the file with all planetbids and iterate through each
'''
def reading_csv_with_planetbids(csv_file):

    # Convert it into a Pandas DataFrame
    df_main = pd.read_csv(csv_file)

    # Current Count
    count = 536

    # Iterate through the file
    for index, row in df_main[count:].iterrows():
        
        # Links Row
        link = row['WebLink']
        awarding_body = row['AwardingBody']

        # Link ID: use for identification in the future
        link_id = link.split("/")[4]

        # Acknowledge the count
        print(f"Current Count: {count}\nAwarding Body: {awarding_body}")

        # Start iteration
        bid_url_ids = webscraping_planetbids_rowattributes(link, awarding_body, index, link_id)

        # Check if the link is faulty
        if isinstance(bid_url_ids,list):
            faulty_links(awarding_body, link)

        else:
            csv_rowattribute_storage(bid_url_ids, awarding_body)

        # Update the count
        count += 1















if __name__ == "__main__":

    # Planetbids Sites csv file
    planetbids_sites = "/Users/damiamalfaro/Desktop/Europe/testing_wesonder/Planetbids/planetbids_email_extracion/aaa_planetbids_sites.csv"

    reading_csv_with_planetbids(planetbids_sites)

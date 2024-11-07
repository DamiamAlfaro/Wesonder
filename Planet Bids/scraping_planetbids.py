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
import glob



'''
The function that appends to the csv file and creates a new one when there is none
'''
def recording_to_csv(dataframe, csv_file, current_iteration, folder_number):
    
    # Acquire the directory list of csvfiles
    current_directory = f'planetbids_correlation{folder_number}/'
    instance_check = os.listdir(current_directory)
    
    # Check if the csv file is within the directory
    if csv_file in instance_check:
        
        # If it is, append to the csv file
        dataframe.to_csv(current_directory+csv_file, mode='a', index=False, header=False)
        print(f"[Iteration {current_iteration} appended]\n")

    # If it isn't, then create a new csv file with its title
    else:
        dataframe.to_csv(current_directory+csv_file, index=False)
        print(f"[Iteration {current_iteration} created]\n")




'''
JA: This function will embellish strings and allocate them into a csv file for further analysis and research
'''
def string_embellishment_and_allocation(list_of_lists_of_strings, other_strings, current_iteration, folder_number):
    
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
    bid_particular_link = [other_strings[3] for _ in range(len(names))]

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
    "BidInformation": bid_all_information,
    "BidUrl": bid_particular_link
    }

    # Return the df as a variable for the next function
    df = pd.DataFrame(data)
    
    # Convert to csv, either append or create new csv
    csv_title_file = f"{re.sub(r'[^a-zA-Z0-9]', '_', awarding_bodies[0].lower())}.csv"
    recording_to_csv(df,csv_title_file, current_iteration, folder_number)



'''
Actually webscrap each attribute from the planetbids link
'''
def planetbids_webscraping(url, main_index, current_index, awarding_body, folder_number):

    # Initiate the webdriver
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(4)

    # Bid Title for future usage
    try:
        bid_title_element = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CLASS_NAME,'bid-detail-title'))
        )
        bid_title_text = bid_title_element.text
    except:
        bid_title_element = f'Bid{current_index}{awarding_body}'
    
    
    # Pinpoint the initial element for the main welcome page
    try:
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

    except:
        bid_description = 'none'    

    # Click on the Prospective Bidders tab
    try:
        prospective_bidders_tab = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH,"//li[@class='bidPBs']"))
            )
        prospective_bidders_tab.click()
        time.sleep(2)

    except:
        print(f"Something is wrong with the Prospective Bidders tab of {file} #{current_index} in {main_index}")
                
        

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
    other_important_strings = [bid_title_text, awarding_body, bid_text_information, url]

    # String embellishment and csv allocation function
    string_embellishment_and_allocation(all_entities, other_important_strings, current_index, folder_number)


'''
Now, let's extract the contractor attributes from planetbids, especifically from the links
of the csv file.
'''
def scraping_each_pb_site(csv_file, main_index, folder_number):
    
    # Import as dataframe
    df = pd.read_csv(csv_file)

    # Current iteration within the file
    count = 11
    
    # Iterate through each of the individual project links
    for index, row in df.iloc[count:].iterrows():

        print(f'File: {csv_file}\nFile Number: {main_index}\nCurrent Iteration: {index}\nPercentage Completed: {round(index/len(df),3)}')
        
        # Variables from csv file
        awarding_body = row['AwardingBody']
        individual_project_url = row['UniqueBidPBLink']

        # Make sure it works
        try:
            planetbids_webscraping(individual_project_url,main_index, index, awarding_body, folder_number)

        # Since it is difficult to stop, let's give it a quick push and make it longer to stop
        except:
            time.sleep(8)
            continue


        













if __name__ == "__main__":

    # Iterate through each csv file
    treasure_location = 'accurate/'

    '''
    Folder total = 1417
    Current Iteration Session 1: 5 (0-472)
    Current Iteration Session 2: 473 (473-944)
    Current Iteration Session 3: 945 (945-1417)
    '''
    treasure_files = os.listdir(treasure_location)
    
    # Counts vary on the file being executed
    count = 126
    halt_count = 143
    folder_number = 1 # Based on the session

    # Iterate through each csv
    for file in range(count, len(treasure_files)):
        scraping_each_pb_site(f'{treasure_location}{treasure_files[file]}', file, folder_number)
        print(f'{treasure_files[file]} Completed\nOverall Completed: {round(file/len(treasure_files),3)}')
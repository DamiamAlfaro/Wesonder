import pandas as pd
import requests
import time
import os
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




'''
Step 1: We are going to cleanase the file of contractors. We need to remove the contractors
and leave the awarding bodies only.
'''
def dir_entities_file_cleansing(csv_file):

    # A normal removal, nothing much...

    df = pd.read_csv(csv_file,low_memory=False)
    df_cleansed = df[df['EntityType'] == 'Awarding Body\nType']
    df_cleansed.to_csv('awarding_body_entities.csv',index=False)




'''
Allocating the attributes within a csv file.
'''
def allocation_into_csv_file(list_of_attributes):

    file_name = 'bidnet_direct_awarding_bodies.csv'

    df = pd.DataFrame({
        "EntityName": [list_of_attributes[0]],
        "EntityType": [list_of_attributes[1]],
        "EntityEmail": [list_of_attributes[2]],
        "EntityWebsite": [list_of_attributes[3]],
        "EntityAddress1": [list_of_attributes[4]],
        "EntityAddress2": [list_of_attributes[5]],
        "EntityCity": [list_of_attributes[6]],
        "EntityState": [list_of_attributes[7]],
        "EntityZip": [list_of_attributes[8]],
        "EntityCSLB": [list_of_attributes[9]],
        "EntityLegalName": [list_of_attributes[10]],
        "EntityPhone": [list_of_attributes[11]],
        "EntityIDNum": [list_of_attributes[12]],
        "EntityPresident": [list_of_attributes[13]],
        "EntityPWCR": [list_of_attributes[14]],
        "EntityRegistrationDate": [list_of_attributes[15]],
        "EntityRegistrationEndDate": [list_of_attributes[16]],
        "EntityDBA": [list_of_attributes[17]],
        "EntityCounty": [list_of_attributes[18]],
        "Link": [list_of_attributes[19]]
    })

    if not os.path.isfile(file_name):
        df.to_csv(file_name, index=False, header=True, mode='w')

    else:
        df.to_csv(file_name, index=False, header=False, mode='a')
    






'''
Actual google search
'''
def bidnet_direct_google_search(string_name):
    
    # Using the string name, we will search for the respective bidnet direct site.
     
    try:
        driver = webdriver.Chrome()
        searchable_string = f'bidnet direct {string_name}'
        driver.get("https://google.co.in/search?q=" + searchable_string)
        time.sleep(4)
    
        google_results = WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.ID,"search")))
        google_result_page = google_results.find_elements(By.XPATH,"//a[@jsname='UWckNb']")
        google_result_links = []        
        for a_tag in google_result_page:
            link_itself = a_tag.get_attribute("href")
            if 'bidnetdirect.com/' in link_itself:
                google_result_links.append(link_itself)

        driver.quit()

        return google_result_links
    
    except:

        return ['none']




'''
Step 2: Using a similar functionality as with the planetbids google search, we will search individually
for each of the awarding body's name, along with the word 'bidnet direct' in google, which will result
in possible bidnet direct links associated with the awarding body in question.
'''
def bidnet_direct_instances_allocation(csv_file,count):
    
    # The first step is, of course, to access the dataframe column containing all of the awarding bodies
    # names, using such names, we will conduct google searches, and then acquire all of the links of the
    # search that have bidnet direct in them, however, we have to be careful here, some of the bidnet direct
    # url links in the google result are of individual bids, not of the main page of a awarding body bidnet
    # direct bid site. We need to find such pattern. After that, we will allocate each of the findings within
    # a csv file using the mode='a' functionality in order to avoide losing progress.

    df = pd.read_csv(csv_file, low_memory=False)
    total_rows = len(df)

    for index, row in df.iloc[count:].iterrows():
        
        entity_name = row['EntityName']
        entity_type = row['EntityType']
        entity_email = row['EntityEmail']
        entity_website = row['EntityWebsite']
        entity_address1 = row['EntityAddress1']
        entity_address2 = row['EntityAddress2']
        entity_city = row['EntityCity']
        entity_state = row['EntityState']
        entity_zip = row['EntityZip']
        entity_cslb = row['EntityCSLB']
        entity_legal_name = row['EntityLegalName']
        entity_phone = row['EntityPhone']
        entity_id_num = row['EntityIDNum']
        entity_president = row['EntityPresident']
        entity_pwcr = row['EntityPWCR']
        entity_registration_date = row['EntityRegistrationDate']
        entity_registration_end_date = row['EntityRegistrationEndDate']
        entity_dba = row['EntityDBA']
        entity_county = row['EntityCounty']
        link = bidnet_direct_google_search(entity_name)[0]

        list_of_attributes = [
            entity_name,
            entity_type,
            entity_email,
            entity_website,
            entity_address1,
            entity_address2,
            entity_city,
            entity_state,
            entity_zip,
            entity_cslb,
            entity_legal_name,
            entity_phone,
            entity_id_num,
            entity_president,
            entity_pwcr,
            entity_registration_date,
            entity_registration_end_date,
            entity_dba,
            entity_county,
            link
        ]
        

        allocation_into_csv_file(list_of_attributes)
        print(f'Iteration #{index}\nPercentage Completed: {round((index/total_rows)*100,2)}%')
        print(f'Awarding Body: {entity_name}\nLink: {link}\n')











if __name__ == "__main__":
    
    # The goal of this program is to acquire a database, similar to the one for planetbids, of all of the 
    # awarding bodies and their respective bidnet direct websites. This will expand our real-time bid
    # display stockpile by including not only the planetbids bids, but also the bidnet direct bids.
    
    dir_entities_file = 'dir_entities_refined.csv' # Step 1
    awarding_bodies_file = 'awarding_body_entities.csv' # Step 2

    step = int(input('Step: '))

    match step:

        case 1:

            # Step 1 - Awarding Bodies: The DIR entities website still has contractors in it, we need 
            # to remove them and leave solely the awarding bodies. Why? We need to use their names to 
            # search for the respective bidnet direct site for each awarding body.

            dir_entities_file_cleansing(dir_entities_file)

        case 2:

            # Step 2 - Google Search: Using each value under the awarding bodies, we will do google 
            # searches to find each awarding body's bidnet direct affiliation. I realized that there
            # isn't many bidnet direct affiliations, by any will help. What matters here is the fact
            # that we are including bidnet direct as a source of bids, thereby expanding our repertoire
            # of real-time bids.

            count = int(input('Count: '))
            bidnet_direct_instances_allocation(awarding_bodies_file, count)






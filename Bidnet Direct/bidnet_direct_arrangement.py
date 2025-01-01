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




'''
Function within Step 3: County Search, here it is intendent
'''
def county_finder_based_on_municipality(place):
    
    driver = webdriver.Chrome()



'''
Step 3: First and foremost, we need to make a study of the current links, what are the current patterns for
each, if there are any common outliers, and how the functional ones differentiate from the rest. Only after
that we ought to use such pattern study to approach the most optimal solution out of this function.
'''
def awarding_bodies_bidnet_direct_sites(csv_file):
    
    # First we need to analyze the differences, discrepancies from each of the urls. Of course, we will 
    # isolate the functional ones for further study after we deal with the chaos of the remaining bidnet
    # direct urls. Solve them and sort them properly, then we can initiate the webscraping for each functional
    # singular ones.


    df = pd.read_csv(csv_file,low_memory=False)
    url_list = df['Link'].values.tolist()
    unique_url_list = list(set(url_list))


    # After the study, we've come with the following conclusions:

    # 1) Every url with 'solicitations/' will be a source of a foreign link. Let me explain: these types of urls
    # are solicitations, single bid webpages, and they list the source of the bid, where it was originally published,
    # which might serve as good information nonetheless, just that, for information sake.

    # 2) There are infiltrated links from other states, which might be useful but not for this version of WESONDER.
    # In order to deal with these infiltrators, we are going to check if the state in lowercase letters are found
    # within their respective urls, as they tend to do.

    # 3) Basically, the urls that apply are the ones containing 'california', that's it. Pretty simple I know, but
    # at least we were able to segregate them. We assigned a singular csv file for all of the functional bidnet 
    # directs in California.

    # 4) [DISCARDED] We will need a function for the allocation of counties, we have some functional urls that do not have
    # any county assign to them, we need to find their county before proceeding. I got the idea of using the google
    # search using the word 'in which county is {place} ca'. We can try that first, then try another if it doesn't
    # work out; for this we will utilze the google search functionality from bidnet direct and planetbids programs.
    # There is a total of 83 functional urls, that is, 83 rows should be the ones iterated for every real-time
    # acquisition of bidnet direct California bids. Now we need to repeat this within the itterrows loop in order
    # to change the dataframe directly.

    # 5) We will approach this problem more theorically, we want to create a mechanism, or call it algorithm that will
    # allocate a useful link, and all of the possible counties the link was correlated to based on the algorithm result.
    # Basically we want to have two list within one, the main list will have the length of the total unique_urls (83 as
    # of now), the first sublist will contain the unique url, and the second sublist will contain a list of strings 
    # containing the possible counties based on a collection of matches between all of the useful links of all awarding
    # bodies with a useful link on their respective Link column.


    useful_urls = [] 
    urls_with_foreign_urls = []

    for link in unique_url_list:
        if 'solicitations/' in link:
            urls_with_foreign_urls.append(link)
        elif 'california' in link:
            useful_urls.append(link)

        else:
            pass

    print(len(useful_urls))
    print(len(urls_with_foreign_urls))




    all_useful_url_instances = []
    unique_urls = []
    respective_counties = []
    for index, row in df.iterrows():

        url_string = row['Link']
        county_in_question = row['EntityCounty']

        if url_string in useful_urls:
            all_useful_url_instances.append([url_string,county_in_question])


        if url_string in useful_urls and url_string not in unique_urls:

            if pd.isnull(county_in_question):
                pass

            unique_urls.append(url_string)
            respective_counties.append(county_in_question)
            
    print(len(all_useful_url_instances))
    print(len(unique_urls))
        





        



    











if __name__ == "__main__":
    
    # The goal of this program is to acquire a database, similar to the one for planetbids, of all of the 
    # awarding bodies and their respective bidnet direct websites. This will expand our real-time bid
    # display stockpile by including not only the planetbids bids, but also the bidnet direct bids.
    
    dir_entities_file = 'dir_entities_refined.csv' # Step 1 Input 
    awarding_bodies_file = 'awarding_body_entities.csv' # Step 2 Input - Step 1 Output
    bidnet_direct_awarding_bodies = 'bidnet_direct_awarding_bodies.csv' # Step 3 Input - Step 2 Output

    step = int(input('Step: '))

    match step:

        case 1:

            # Step 1 - Awarding Bodies: The DIR entities website still has contractors in it, we need 
            # to remove them and leave solely the awarding bodies. Why? We need to use their names to 
            # search for the respective bidnet direct site for each awarding body.

            # Files Input:
            # 1) dir_entities_refined.csv

            # Files Output:
            # 1) awarding_body_entities.csv


            dir_entities_file_cleansing(dir_entities_file)

        case 2:

            # Step 2 - Google Search: Using each value under the awarding bodies, we will do google 
            # searches to find each awarding body's bidnet direct affiliation. I realized that there
            # isn't many bidnet direct affiliations, by any will help. What matters here is the fact
            # that we are including bidnet direct as a source of bids, thereby expanding our repertoire
            # of real-time bids.

            # Files Input:
            # 1) awarding_body_entities.csv

            # Files Output:
            # 2) bidnet_direct_awarding_bodies.csv

            count = int(input('Count: '))
            bidnet_direct_instances_allocation(awarding_bodies_file, count)

        case 3:

            # Step 3 - Bidnet Direct URLs: We've collected the respective google results for each awarding
            # body bidnet direct website connection, we have them on a file. There seems to be multiple types
            # of links, a great diversity of them, but they seem 'species' of links, some of them appear
            # similar than others, just the same attributes within them change (numbers and ids). Let's analyze
            # those patterns and see if there comes something, besides such patterns, there seems to be a
            # great deal of accurate ones, we will also segregate those for later concatenation. The name of
            # the study is going to be displayed in the function and its respective description above.

            # Files Input: 
            # 1) bidnet_direct_awarding_bodies.csv

            awarding_bodies_bidnet_direct_sites(bidnet_direct_awarding_bodies)


            






import pandas as pd
import sys
import requests
import numpy as np
import re
import time
import os
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
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
Part of Step 3: Using the following function we will store the planetbids bid attributes into a csv file
in order to access it later. The question is, how should the arrangement of columns be
within the file?
'''
def allocate_attributes_within_csv(attributes_list):
    
    # Just a simple allocation into the csv file. The headers of the file are the 
    # following: AwardingBody, WebLink, County, X_Coordinates, and Y_Coordinates.
    # Adjust comment/variable name below accordingly:
    
    file_name = 'functional_bidnet_direct_sites.csv'

    df = pd.DataFrame({
        "BidNetDirectUrl":[attributes_list[0]],
        "County":[attributes_list[1]],
        "X_Coordinates":[attributes_list[2]],
        "Y_Coordinates":[attributes_list[3]]
    })

    if not os.path.isfile(file_name):
        df.to_csv(file_name, index=False, header=True, mode='w')

    else:
        df.to_csv(file_name, index=False, header=False, mode='a')




'''
Part of Step 3: Using Nominatim, we will try to find the addresses that were not found in the
first attempt, we can copy the same structure as the function above in order to
allow this function to be used within an iteration.
'''
def obtaining_new_geolocations_attempt2(address_string):
    
    # This is the second attempt to find an address using Nominatim. We will
    # be using the same methodology as with attempt 1; the output of this
    # function will either be a pair of zeros, or the geolocation
    # coordinates for each of the addressess.
    
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.geocode(address_string, timeout=8)

    if location:
        lat = location.latitude
        lon = location.longitude
        return lat, lon
    else:
        lat = 0
        lon = 0
        return lat, lon




'''
Part of Step 3: Using this function, we will extract the geolocation of each of the counties found on the function
below, after that, we will store the data into a csv file by the dragged variables which will 
serve as additional datums.
'''
def county_geolocation_acquisition(county, url):
    
    # The first step is to use the function above to locate the county geolocation, after that we
    # need to take the newly found geolocation, along with the other attributes into a csv file
    # in order to continoulsy build the newly refined planetbids_sites.csv file that will contain
    # the counties, and the geolocations of each county.

    county_string = f'{county} County, California'
    geolocations = obtaining_new_geolocations_attempt2(county_string)
    x_coordinate = geolocations[0]
    y_coordinate = geolocations[1]
    list_of_attributes = [url, county, x_coordinate, y_coordinate]

    allocate_attributes_within_csv(list_of_attributes)

    print(f'URL: {url}\nCounty: {county}\nGeolocations: ({x_coordinate},{y_coordinate})')



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


    # 6) We are going to create a file for the urls_with_foreign_urls in order to analyse it later on. We don't really need
    # its content, but it will interesting to get additional publishing sites, it might not hurt to do a case study on
    # those as well. In order to keep them and before they put down the bidnet direct sites, we will allocate the foreign
    # urls into a csv file via webscraping. But that will be another function, first let's allocate them within a separate 
    # csv file.

    df_foreign = pd.DataFrame({
        "ForeignBidnetDirectURLs":urls_with_foreign_urls,
    })
    df_foreign.to_csv('additional_bidnet_direct_singular_sites.csv',index=False)
    

    all_useful_url_instances = []
    unique_urls = []
    respective_counties = []
    for index, row in df.iterrows():

        url_string = row['Link']
        county_in_question = row['EntityCounty']

        if url_string in useful_urls:
            all_useful_url_instances.append([url_string,county_in_question])


        if url_string in useful_urls and url_string not in unique_urls:

            unique_urls.append(url_string)
            respective_counties.append(county_in_question)
            

    counties_based_on_index = [[] for _ in range(len(unique_urls))]
    another_unique_url_list = []

    for instance in all_useful_url_instances:
        if instance[0] in unique_urls and instance[1] not in counties_based_on_index[unique_urls.index(instance[0])]:
            counties_based_on_index[unique_urls.index(instance[0])].append(instance[1])
            if instance[0] not in another_unique_url_list:
                another_unique_url_list.append(instance[0])
    
    
    single_county_list = []
    for county_list in counties_based_on_index:
        if pd.isna(county_list[0]) and len(county_list) > 1:
            single_county_list.append(county_list[1])
        else:
            single_county_list.append(county_list[0])


    # 7) I am just going to allocate each county manually, then utilize the county geolocator finder from
    # the planetbids program in order to allocate a respective geolocation to each functional bidnet direct
    # url webpage just to be able to map it later on. The code above is cool, experimental, but we need results
    # fast here, so I will cut some time from theory and allocate it into practice. In order to acquire the
    # functional_bidnet_direct_sites_undone.csv file just make the lists above a data frame.

    functional_bidnet_direct_file_undone = 'functional_bidnet_direct_sites_undone.csv'
    df_sites = pd.read_csv(functional_bidnet_direct_file_undone)

    for index, row in df_sites.iterrows():

        county = row['County']
        url = row['BidNetDirectUrl']

        county_geolocation_acquisition(county, url)




'''
Part of Step 4: A mere integration into a csv file, nothing more, nothing less...
'''
def bidnet_direct_bids_into_csv(list_of_attributes):
    
    # Just a simple allocation into the csv file. The headers of the file are the 
    # following: AwardingBody, URL, County, X_Coordinates, Y_Coordinates, SolicitationNumber,
    # SolicitationName, OpeningDate, ClosingDate, SolicitationURL, and ClosingTime.
    # Adjust comment/variable name below accordingly:
    
    file_name = 'real_time_bidnet_direct_bids.csv'

    df = pd.DataFrame({
        "AwardingBody":[list_of_attributes[0]],
        "URL":[list_of_attributes[1]],
        "County":[list_of_attributes[2]],
        "X_Coordinates":[list_of_attributes[3]],
        "Y_Coordinates":[list_of_attributes[4]],
        "SolicitationNumber":[list_of_attributes[5]],
        "SolicitationName":[list_of_attributes[6]],
        "OpeningDate":[list_of_attributes[7]],
        "ClosingDate":[list_of_attributes[8]],
        "SolicitationURL":[list_of_attributes[9]],
        "ClosingTime":[list_of_attributes[10]],
    })

    if not os.path.isfile(file_name):
        df.to_csv(file_name, index=False, header=True, mode='w')

    else:
        df.to_csv(file_name, index=False, header=False, mode='a')



'''
Part of Step 4: For neat and organization purposes, we will write an additional function of the acquisition
of individual bidnet direct bid times from the respective href value of each of the bids from the main
bid table of each functional bidnet url.
'''
def bidnet_direct_bid_time_acquisition(url):
    
    # Similar to the function below, we will use beautifulsoup to acquire the bid time from the webpage
    # provided from the iteration below. We need to give it a few seconds as timeout in order to avoid
    # any discrepancies or response errors. In the result, we have 'PM PST', which will be remain adjoint
    # to the time in case we need it later, otherwise we can just do a time conversion, no big deal. 

    response = requests.get(url, timeout=4)
    soup = BeautifulSoup(response.content,'html.parser')

    main_box = soup.find('div',class_='dateLabels')
    div_within_main_box = main_box.find_all('div',class_='mets-field')
    closing_time_element = div_within_main_box[2].find('div',class_='mets-field-body')
    closing_time = " ".join(closing_time_element.text.replace('\t','').replace('\n','').split(' ')[1:])
    
    return closing_time




'''
Part of Step 4: The attempt to webscrap using Beautifulsoup. Which I like it more since we cease sessions
and instead scrape the data right away, without opening the browser, which makes it quite fast and useful.
In comparison with Selenium that it takes up to 10 seconds for each session to extract the data. But, let's
try it first.
'''
def the_actual_bidnet_direct_webscraping(url, county, x_coord, y_coord):


    # First we will try Beautifulsoup, a webscraping library I enjoy more than selenium due to its efficiency,
    # speed, and reliability. The issue with this library is that we cannot do javascript functionalities such 
    # as clicks, presses, typing, etc, solely webscraping. 


    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')


    # This is a crucial step: in the following code, we will iterate through the every single attribute of the
    # weblink and use stratification methodologies to acquire the respective variable of the bid we are looking
    # for. Recall that stratification methodology involves the usage of <html> tags and elements layers, every
    # single datum in the web can be acquired if you know the proper layers and <html> tags that surrond the 
    # datum in question. We will get all four crucial variables from each bid, all attributes will be allocated 
    # into a list solicitation_attributes_list:
    
    # 1) Solicitation Name and Number: Solicitation Number and Name.
    # 2) Solicitation Dates: Opening and Closing Dates.
    # 3) Solicitation URLs: The href value of each Solicitation.
    # 4) Solicitation Due Time: This cannot be acquired withuth (3) Solicitation URL.

    # We will also place two Except statements, the first one, AttributeError will be assigned for the respective
    # scenarios where no bids are published from the bidnet direct site. The second one, Exception, will be 
    # assigned for the rest of scenarios, you know, unforeseen problems. Within each iteration, we will allocate
    # the six attributes to a csv file continously, with the append mode.

    try:
        awarding_body_name_element = soup.find('div',class_='buyerOrganizationName').text.replace('\t','').replace('\n','')
        awarding_body_name = awarding_body_name_element.replace('Bid Opportunities','')

    except:
        awarding_body_name = 'none'

    try:
        solicitation_table = soup.find('table',class_='sol-table')
        tbody = solicitation_table.find('tbody')
        solicitiations = tbody.find_all('tr')
        
        for each_solicitation in solicitiations[:-1]:

            print('-------------------------------------------------------')

            solicitation_attributes_list = [awarding_body_name, url, county, x_coord, y_coord]
            print(f'Awarding Body: {awarding_body_name}\nURL: {url}\nCounty: {county}')

            solicitation_attributes_element = each_solicitation.find('div',class_='sol-info-container')
            solicitation_number_element = solicitation_attributes_element.find('div',class_='sol-num')
            solicitation_number = solicitation_number_element.text.replace('\t','').replace('\n','')
            solicitation_attributes_list.append(solicitation_number)
            print(f'Solicitation Number: {solicitation_number}')

            solicitation_name_element = solicitation_attributes_element.find('div',class_='sol-title')
            solicitation_name = solicitation_name_element.text.replace('\t','').replace('\n','')
            solicitation_attributes_list.append(solicitation_name)
            print(f'Solicitation Name: {solicitation_name}')

            dates_attributes = each_solicitation.find('span',class_='dates-col')
            opening_date_element = dates_attributes.find('span',class_='sol-publication-date')
            opening_date = opening_date_element.find('span',class_='date-value').text
            solicitation_attributes_list.append(opening_date)
            print(f'Opening Date: {opening_date}')

            closing_date_element = dates_attributes.find('span',class_='sol-closing-date')
            closing_date = closing_date_element.find('span',class_='date-value').text
            solicitation_attributes_list.append(closing_date)
            print(f'Closing Date: {closing_date}')

            solicitation_link_element = solicitation_name_element.find('a').get('href')
            solicitation_link = f'https://www.bidnetdirect.com{solicitation_link_element}'
            solicitation_attributes_list.append(solicitation_link)
            print(f'Solicitation Link: {solicitation_link}')
            
            closing_time = bidnet_direct_bid_time_acquisition(solicitation_link)
            solicitation_attributes_list.append(closing_time)
            print(f'Solicitation Due Time: {closing_time}')

            bidnet_direct_bids_into_csv(solicitation_attributes_list)

            


    except AttributeError as exe:
        solicitation_attributes_list = [
            awarding_body_name, url,county,
            x_coord,y_coord,'none',
            'none','none','none',
            'none','none','none'
        ]
        print(f'Awarding Body: {awarding_body_name}\nURL: {url}\nCounty: {county}\nFAULTY')
        bidnet_direct_bids_into_csv(solicitation_attributes_list)
    
    except Exception as exe:
        print(f'ANOTHER MATTER\n\n{exe}')
        sys.exit(1)

    










'''
Step 4: The real work begins. Let's webscrap based on the links from the functional file, and acquire the
same attributes of each page accordingly.
'''
def bidnet_direct_real_time_webscraping(csv_file):
    
    # The first step is to of course, assign a selenium session... Perhaps Beautifulsoup could work here,
    # bidnet direct seem to be non-javascript, but I might be wrong, so let's try both of them out. Of course
    # in the course of attempts, we will figure out the variables we want to extract from each session.

    df = pd.read_csv(csv_file)
    total_rows = len(df)

    for index, row in df.iterrows():
        
        url = row['BidNetDirectUrl']
        county = row['County']
        x_coordinate = row['X_Coordinates']
        y_coordinate = row['Y_Coordinates']

        the_actual_bidnet_direct_webscraping(url, county, x_coordinate, y_coordinate)

        print(f'\nIteration #{index} - Percentage Completed: {round((index/total_rows)*100,2)}%\n\n\n')
        









if __name__ == "__main__":
    
    # The goal of this program is to acquire a database, similar to the one for planetbids, of all of the 
    # awarding bodies and their respective bidnet direct websites. This will expand our real-time bid
    # display stockpile by including not only the planetbids bids, but also the bidnet direct bids.
    
    dir_entities_file = 'dir_entities_refined.csv' # Step 1 Input 
    awarding_bodies_file = 'awarding_body_entities.csv' # Step 2 Input - Step 1 Output
    bidnet_direct_awarding_bodies = 'bidnet_direct_awarding_bodies.csv' # Step 3 Input - Step 2 Output
    funtional_bidnet_direct_sites = 'functional_bidnet_direct_sites.csv' # Step 4 Input - Step 3 Output

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

            # Files Output:
            # 1) functional_bidnet_direct_sites_undone.csv
            # 2) functional_bidnet_direct_sites.csv
            # 3) additional_bidnet_direct_singular_sites.csv

            awarding_bodies_bidnet_direct_sites(bidnet_direct_awarding_bodies)

        case 4:

            # Step 4 - Real Time Webscraping: Using the functional bidnet direct sites we will iterate through
            # each and acquire the information regarding every single active bid, just how we did with the real
            # time display of planetbids. We are going to have an allocated csv for the real-time display 
            # accordingly.

            # Files Input:
            # 1) functional_bidnet_direct_sites.csv

            bidnet_direct_real_time_webscraping(funtional_bidnet_direct_sites)




            






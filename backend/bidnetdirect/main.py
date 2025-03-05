import pandas as pd
import time
import requests
from google.oauth2.service_account import Credentials # type: ignore
from googleapiclient.discovery import build  # type: ignore
from bs4 import BeautifulSoup



start_time = time.time()


'''
Part of Step 4: A mere integration into a csv file, nothing more, nothing less...
'''
def bidnet_direct_bids_into_google_sheets(list_of_attributes):
    
    df = pd.DataFrame(list_of_attributes)
    df.columns = [
        'AwardingBody',
        'AwardingBodyLink',
        'County',
        'X_Coordinates',
        'Y_Coordinates',
        'SolicitationNumber',
        'BidTitle',
        'PostedDate',
        'DueDate',
        'BidLink',
        'DueTime'
    ]
    df.to_csv('finalized_bidnetdirect_bids.csv',index=False)



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
    ultimate_list = []


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

            ultimate_list.append(solicitation_attributes_list)

    except AttributeError:
        pass
    
    
    return ultimate_list
    


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
    all_bids_list = []

    for index, row in df.iterrows():
        
        url = row['BidNetDirectUrl']
        county = row['County']
        x_coordinate = row['X_Coordinates']
        y_coordinate = row['Y_Coordinates']

        bid_list = the_actual_bidnet_direct_webscraping(url, county, x_coordinate, y_coordinate)
        all_bids_list.extend(bid_list)

        print(f'\nIteration #{index} - Percentage Completed: {round((index/total_rows)*100,2)}%\n\n\n')
        
    
    bidnet_direct_bids_into_google_sheets(all_bids_list)
    

# The goal of this program is to acquire a database, similar to the one for planetbids, of all of the 
# awarding bodies and their respective bidnet direct websites. This will expand our real-time bid
# display stockpile by including not only the planetbids bids, but also the bidnet direct bids.


bidnet_direct_csv = 'https://storage.googleapis.com/wesonder_databases/bidnet_direct/functional_bidnet_direct_sites.csv'


# Step 4 - Real Time Webscraping: Using the functional bidnet direct sites we will iterate through
# each and acquire the information regarding every single active bid, just how we did with the real
# time display of planetbids. We are going to have an allocated csv for the real-time display 
# accordingly.

# Files Input:
# 1) functional_bidnet_direct_sites.csv

# Files Output:
# 1) real_time_bidnet_direct_bids.csv


bidnet_direct_real_time_webscraping(bidnet_direct_csv)







            

end_time = time.time()
elapsed_seconds = end_time-start_time
elapsed_minutes = round(elapsed_seconds/60,2)
elapsed_hours = round(elapsed_minutes/60,2)
print(f'\nTotal Seconds to Execute main.py:\nSeconds = {elapsed_seconds}\nMinutes = {elapsed_minutes}\nHours = {elapsed_hours}')


import pandas as pd
import numpy as np
import os
import time
import concurrent.futures
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selectolax.parser import HTMLParser

count_faulty = 0
count_correct = 0

'''
Part of Step 4: If the Multi-Browser Functionality does not work, we want to know why, and check the 
links that did not work out for some reason. We already know the links that do not work for certain, 
so every other link must work, no matter what.
'''
def faulty_multi_browser_to_csv(url):

    # The headers for the csv file are the following: AwardingBody, PlanetbidsABLink, County,
    # X_Coordinates, and Y_Coordinates. This is only for future refinement purposes.

    file_name = 'faulty_planetbids_links.csv'
        
    df = pd.DataFrame({
        "FaultyUrl": [url],
    })

    if not os.path.isfile(file_name):
        df.to_csv(file_name, index=False, header=True, mode='w')

    else:
        df.to_csv(file_name, index=False, header=False, mode='a')




'''
Part of Step 4: As usual, we will allocate the attributes of each bid into a csv file for 
later usage.
'''
def multi_browser_to_csv(list_of_attributes):

    '''
    # The headers for the csv file are the following: AwardingBody, PlanetbidsABLink, County,
    # X_Coordinates, Y_Coordinates, DatePosted, BidName, SolicitationNumber, DueDate, DueTime,
    # SubmissionMethod, and BidUrl.
    '''

    file_name = 'testing_real_time_planetbids_bids.csv'
        
    df = pd.DataFrame({
        "AwardingBody": [list_of_attributes[0]],
        "PlanetbidsUrl": [list_of_attributes[1]],
        "County": [list_of_attributes[2]],
        "X_Coordinates": [list_of_attributes[3]],
        "Y_Coordinates": [list_of_attributes[4]],
        "ActiveBidLink": [list_of_attributes[5]],
        "DatePosted": [list_of_attributes[6]],
        "BidName": [list_of_attributes[7]],
        "SolicitationNumber": [list_of_attributes[8]],
        "DueDate": [list_of_attributes[9]],
        "DueTime": [list_of_attributes[10]],
        "SubmissionMethod": [list_of_attributes[11]],
    })

    if not os.path.isfile(file_name):
        df.to_csv(file_name, index=False, header=True, mode='w')

    else:
        df.to_csv(file_name, index=False, header=False, mode='a')



'''
Part of Step 4: This is going to be the testing area, where we try different webscraping functionalities
and choose what best fit us, our time, and our resources. New methodologies in order to grow mon ami.
'''
def enhanced_webscraping_html(url):

    '''
    Testing area... Apparently it is better if we parse the html content into strings, rather than
    opening the selenium session itself. The Selenium Grid functionality is quite fast, which is 
    why we are going to implement a WebDriverWait step below in order to secure position within
    the webdriver session is completed once we find the <tbody> element, which is where all bids
    are located.
    '''

    global count_faulty, count_correct

    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(command_executor="http://localhost:4444", options=options)
    time.sleep(1)
    driver.get(url)
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME,'tbody'))
        )
        count_correct += 1
        print(
            f'#{count_correct} - Working: {url}'
        )
    
    except:
        count_faulty += 1
        print(f'#{count_faulty} - Faulty: {url}')
        driver.quit()
        faulty_multi_browser_to_csv(url)
        return None
    
    
    html = driver.page_source
    driver.quit()
    return html,url




'''
Part of Step 4: Apparently parsing the html content yields better strings when it comes to webscraping
with selenium, let's try that.
'''
def html_parsing(function_input):

    '''
    Like I said, testing area. We are going to assimilate the functionality from Step 1, we are
    going to find those Selenium Attributes within the html code, and allocate them into a csv file
    accordingly, nothing is going to change, except for the way we webscrap the code, the storage
    mechanism will remain.
    '''

    html_content = function_input[0]
    data = HTMLParser(html_content)

    current_planetbids_url = function_input[1]
    unique_planetbids_site_id_number = str(current_planetbids_url).split('/')[4]

    tbody = data.css_first('tbody')
    tr_elements = tbody.css('tr')
    total_active_bids = 0

    list_of_attributes_main = []

    for individual_tr_element in range(len(tr_elements)):

        '''
        For every active bid that we find, we are going to split its text form string
        by empty spaces in order to acquire each information attribute about the bid.
        We can calculate the dates ourselves later, right now we just need the important
        attributes such as solicitation number, due date, due time, date posted, its link,
        and its submission format. We will need to break down the <tr> elements into 
        individual <td> elements and assign each index to a value. Like I said, stratification
        process. 

        List of attributes order:
        1) PlanetbidsActiveBidLink
        2) DatePosted
        3) BidName
        4) SolicitationNumber
        5) DueDate
        6) DueTime
        7) SubmissionMethod
        8) AwardingBodyPlanetbidsLink

        The following variable is the string containing all attributes of the bid within the bid tabulation. This
        will be our main variable to extract all of the attributes from.
        '''
        
        individual_tr_element_string = tr_elements[individual_tr_element].text(strip=True)

        # If the word 'Bidding' is found within the bid string, then we can extract all of the attributes of the
        # active bid.

        if 'Bidding' in individual_tr_element_string:

            list_of_attributes = []

            # Not really a variable, but it is good to display the number of bid we are dealing with
            total_active_bids += 1
            print(f"\nBid #{individual_tr_element}")

            # 1) PlanetbidsActiveBidLink
            link_rowattribute = tr_elements[individual_tr_element].attributes.get('rowattribute')
            planetbids_bid_link = f'https://vendors.planetbids.com/portal/{unique_planetbids_site_id_number}/bo/bo-detail/{link_rowattribute}'
            print(f'Active Bid URL: {planetbids_bid_link}')

            # 2) DatePosted, the td_elements variable is similar to the individual_tr_element_string because it contains 
            # multiple useful information segregated by html elements and/or css classes.
            td_elements = tr_elements[individual_tr_element].css('td')
            date_posted = td_elements[0].text(strip=True)
            print(f'Date Posted {date_posted}')

            # 3) BidName
            bid_name = td_elements[1].text(strip=True)
            print(f'Bid Name: {bid_name}')

            # 4) SolicitationNumber
            solicitation_number = td_elements[2].text(strip=True)
            print(f'Solicitation #: {solicitation_number}')

            # 5) DueDate
            due_date = td_elements[3].text(strip=True).split(" ")[0]
            print(f'Due Date: {due_date}')

            # 6) DueTime
            due_time = td_elements[3].text(strip=True).split(" ")[1]
            print(f'Due Time: {due_time}')

            # 7) SubmissionMethod
            submission_method = td_elements[6].text(strip=True)
            print(f'Submission Method: {submission_method}')

            list_of_attributes = [
                planetbids_bid_link,
                date_posted,
                bid_name,
                solicitation_number,
                due_date,
                due_time,
                submission_method,
            ]

            list_of_attributes_main.extend(list_of_attributes)


    return list_of_attributes_main





'''
Step 4: We are going to use webscrap technologies, especifically Selenium Grid and Selenium remote
webdriver sessions, as well as docker to optimize the intake of information from the web.
'''
def enhanced_planetbids_webscraping(csv_file, count):
    
    
    # The same area where we iterate...


    df = pd.read_csv(csv_file)
    urls = df['WebLink'].values.tolist()[count:1000]
    remaining_attributes = df[['AwardingBody','WebLink','County','X_Coordinates','Y_Coordinates']]

    '''
    The following attributes have to be included somehow:

        1) AwardingBody
        2) County
        3) X_Coordinates
        4) Y_Coordinates
    '''
        
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(enhanced_webscraping_html,urls))

    for res in range(len(results)):
        extra_attributes = remaining_attributes.loc[res].values.tolist()
        
        '''
        # The following two lists are going to be appended to the respective csv file in question.
        # Perhaps we can even build (if we have time) a way to see if there were faulty planetbids
        # urls, we need to check the effectiveness of this Multi-Browser functionality.
        '''

        extra_attributes_converted = [float(x) if isinstance(x, (np.float64, float)) else x for x in extra_attributes]
        webscraping_values = html_parsing(results[res])

        extra_attributes_converted.extend(webscraping_values)

        if len(extra_attributes_converted) > 5:
            multi_browser_to_csv(extra_attributes_converted)
            print(extra_attributes_converted)

        else:
            print(f'{extra_attributes_converted[0]} has 0 active bids\n')
            print(extra_attributes_converted)


        print('=====================================')






if __name__ == "__main__":

    '''
    I want to run some statistics here, if we are going to utilize this Multi-Browser funtionality
    which is faulty, and not due to our set up (at least that's what we want to believe), but 
    because of the functionality of planetbids, apparently after a few concurrent sessions, the
    sites do not work anymore, then startworking once again. I cannot figure why that is...
    '''
    
    start_time = time.time()

    planetbids_sites_csv = "refined_planetbids_sites.csv"
    print('\nWEB SCRAPER\n')
    count = int(input('Count: '))
    enhanced_planetbids_webscraping(planetbids_sites_csv, count)

    end_time = time.time()

    total_execution_time = end_time - start_time
    print(f'\nTook {round(total_execution_time,2)} seconds to execute this code\n')

























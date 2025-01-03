import pandas as pd
import time
import os
import selenium
import sys
import numpy as np
import concurrent.futures
from selectolax.parser import HTMLParser
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
from geopy.geocoders import Nominatim




'''
If the Multi-Browser Functionality does not work, we want to know why, and check the links that did not
work out for some reason. We already know the links that do not work for certain, so every other link
must work, no matter what.
'''
def planetbids_bids_faulty_real_time_extraction(list_of_attributes):

    # The headers for the csv file are the following: AwardingBody, PlanetbidsABLink, County,
    # X_Coordinates, and Y_Coordinates. This is only for future refinement purposes.

    file_name = 'faulty_real_time_planetbids_bids.csv'
        
    df = pd.DataFrame({
        "AwardingBody": [list_of_attributes[0]],
        "PlanetbidsABLink": [list_of_attributes[1]],
        "County": [list_of_attributes[2]],
        "X_Coordinates": [list_of_attributes[3]],
        "Y_Coordinates": [list_of_attributes[4]],
    })

    if not os.path.isfile(file_name):
        df.to_csv(file_name, index=False, header=True, mode='w')

    else:
        df.to_csv(file_name, index=False, header=False, mode='a')




'''
As usual, we will allocate the attributes of each bid into a csv file for later usage.
'''
def planetbids_bid_attributes_into_csv(list_of_attributes):

    # The headers for the csv file are the following: AwardingBody, PlanetbidsABLink, County,
    # X_Coordinates, Y_Coordinates, DatePosted, BidName, SolicitationNumber, DueDate, DueTime,
    # SubmissionMethod, and BidUrl.

    file_name = 'testing_real_time_planetbids_bids.csv'
        
    df = pd.DataFrame({
        "AwardingBody": [list_of_attributes[0]],
        "PlanetbidsABLink": [list_of_attributes[1]],
        "County": [list_of_attributes[2]],
        "X_Coordinates": [list_of_attributes[3]],
        "Y_Coordinates": [list_of_attributes[4]],
        "DatePosted": [list_of_attributes[5]],
        "BidName": [list_of_attributes[6]],
        "SolicitationNumber": [list_of_attributes[7]],
        "DueDate": [list_of_attributes[8]],
        "DueTime": [list_of_attributes[9]],
        "SubmissionMethod": [list_of_attributes[10]],
        "BidUrl": [list_of_attributes[11]]
    })

    if not os.path.isfile(file_name):
        df.to_csv(file_name, index=False, header=True, mode='w')

    else:
        df.to_csv(file_name, index=False, header=False, mode='a')




'''
Part of Step 1: The following function is to webscrap the active projects from each planetbids
sites in order to display them later. The goals with the following function is
to 1) get the name of the town/city/county associated with the weblink, and
2) acquire the data information for the active bids within the weblink in question.

Step 1 Refinement: We will utilize multiple browsers, if the selenium session decides to fail
with one of the browesers we will jump to the next one and attempt the execution with that
one.
'''
def planetbids_active_bids_webscraping(url, awarding_body, county, x_coord, y_coord):


    # We will utilize the stratification functionality: we will enter several layes of
    # html elements in order to acquire the desired datum from each of the tabulations
    # of each planetbids site. Also, don't forget the title indicating the location. You
    # know what, let's start with that. Additionally, we need to breakdown the url in order
    # to acquire the unique url link for that particular bid page. This will facilitate 
    # the acquisition of bid links.

    # Refinement: We experiment with this new hypothesis of Multi-Browser Webscraping in order to
    # remove as much possibility for a browser to fail as possible. If this works properly, we plan
    # to also implement the Multi-Session Webscraping functionality as well, to make this progress 
    # faster, but first it has to work and increase accuracy, otherwise I cannot extend it via 
    # Multi-Session Webscrapong.


    browsers = [
        ("Chrome", lambda: webdriver.Chrome()),
        ("Edge", lambda: webdriver.Edge()),
        ("Firefox", lambda: webdriver.Firefox())
        
    ]

    driver = None

    for browser_name, browser_constructor in browsers:
        try:
            driver = browser_constructor()
            driver.get(url)
            time.sleep(5)


            unique_planetbids_site_id_number = str(url).split('/')[4]
            site_title = driver.find_element(By.TAG_NAME,'h4').text

            tbody = driver.find_element(By.TAG_NAME,'tbody')
            tr_elements = tbody.find_elements(By.TAG_NAME,'tr')
            total_active_bids = 0

            for individual_tr_element in range(len(tr_elements)):


                # For every active bid that we find, we are going to split its text form string
                # by empty spaces in order to acquire each information attribute about the bid.
                # We can calculate the dates ourselves later, right now we just need the important
                # attributes such as solicitation number, due date, due time, date posted, its link,
                # and its submission format. We will need to break down the <tr> elements into 
                # individual <td> elements and assign each index to a value. Like I said, stratification
                # process. 

                # List of attributes order:
                # 1) AwardingBody
                # 2) PlanetbidsABLink
                # 3) County
                # 4) X_Coordinates
                # 5) Y_Coordinates
                # 6) DatePosted
                # 7) BidName
                # 8) SolicitationNumber
                # 9) DueDate
                # 10) DueTime
                # 11) SubmissionMethod
                # 12) BidUrl


                individual_tr_element_string = tr_elements[individual_tr_element].text

                if 'Bidding' in individual_tr_element_string:

                    total_active_bids += 1
                    
                    print(f"\nBid #{individual_tr_element}")

                    list_of_attributes = [awarding_body, url, county, x_coord, y_coord]

                    link_rowattribute = tr_elements[individual_tr_element].get_attribute('rowattribute')
                    planetbids_bid_link = f'https://vendors.planetbids.com/portal/{unique_planetbids_site_id_number}/bo/bo-detail/{link_rowattribute}'

                    td_elements = tr_elements[individual_tr_element].find_elements(By.TAG_NAME,'td')
                    date_posted = td_elements[0].text
                    list_of_attributes.append(date_posted)
                    print(f"Date Posted: {date_posted}")

                    bid_name = td_elements[1].text
                    list_of_attributes.append(bid_name)
                    print(f"Bid Name: {bid_name}")

                    solicitation_number = td_elements[2].text
                    list_of_attributes.append(solicitation_number)
                    print(f"Solicitation Number: {solicitation_number}")

                    due_date = td_elements[3].text.split(" ")[0]
                    list_of_attributes.append(due_date)
                    print(f"Due Date: {due_date}")

                    due_time = td_elements[3].text.split(" ")[1]
                    list_of_attributes.append(due_time)
                    print(f"Due Time: {due_time}")

                    submission_method = td_elements[6].text
                    list_of_attributes.append(submission_method)
                    print(f"Submission Method: {submission_method}")

                    list_of_attributes.append(planetbids_bid_link)
                    print(f'Bid Link: {planetbids_bid_link}')

                    planetbids_bid_attributes_into_csv(list_of_attributes)

                else:
                    pass

            print(f'\n{awarding_body} Total Active Bids = {total_active_bids}')
            break
    
        except Exception as exe:
            print(f"Error with {browser_name}: {exe}")
            if driver:
                driver.quit()
            continue 

    if driver:
        driver.quit()
        print(f"Finished scraping with {browser_name}.")

    else:
        print("All browser attempts failed.")
        attributes_of_faulty_link = [url, awarding_body, county, x_coord, y_coord]
        planetbids_bids_faulty_real_time_extraction(attributes_of_faulty_link)





'''
Iteration through the planetbids csv file, among other options that include
acquisition of "real-time" planetbids active projects, geolocations of the city
title from planetbids, and csv allocation of such active projects and geolocations
for further display using PHP and Javascript.
'''
def planetbids_sites_iteration(csv_file, count):

    # The first action here is to iterate through each of the planetbids web links,
    # for each we will have a different function associated with it.

    df = pd.read_csv(csv_file,low_memory=False)
    total_rows = len(df)

    for index, row in df.iloc[count:].iterrows():
        
        awarding_body = row['AwardingBody']
        weblink = row['WebLink']
        county = row['County']
        x_coord = row['X_Coordinates']
        y_coord = row['Y_Coordinates']

        planetbids_active_bids_webscraping(
            url=weblink, 
            awarding_body=awarding_body, 
            county=county, 
            x_coord=x_coord, 
            y_coord=y_coord
        )

        print(f'Iteration #{index} just Completed - Percentage: {round((index/total_rows)*100,2)}%\n')
        print('-------------------------------------------------------')

        
        
        






'''
Using the following function we will store the planetbids bid attributes into a csv file
in order to access it later. The question is, how should the arrangement of columns be
within the file?
'''
def allocate_attributes_within_csv(attributes_list):
    
    # Just a simple allocation into the csv file. The headers of the file are the 
    # following: AwardingBody, WebLink, County, X_Coordinates, and Y_Coordinates.
    # Adjust comment/variable name below accordingly:
    
    #file_name = 'refined_planetbids_sites.csv'
    file_name = 'regurgitation_refined_planetbids_sites.csv'

    df = pd.DataFrame({
        "AwardingBody":[attributes_list[0]],
        "WebLink":[attributes_list[1]],
        "County":[attributes_list[2]],
        "X_Coordinates":[attributes_list[3]],
        "Y_Coordinates":[attributes_list[4]]
    })

    if not os.path.isfile(file_name):
        df.to_csv(file_name, index=False, header=True, mode='w')

    else:
        df.to_csv(file_name, index=False, header=False, mode='a')





'''
Using Nominatim, we will try to find the addresses that were not found in the
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
Using this function, we will extract the geolocation of each of the counties found on the function
below, after that, we will store the data into a csv file by the dragged variables which will 
serve as additional datums.
'''
def county_geolocation_acquisition(county, url, awarding_body):
    
    # The first step is to use the function above to locate the county geolocation, after that we
    # need to take the newly found geolocation, along with the other attributes into a csv file
    # in order to continoulsy build the newly refined planetbids_sites.csv file that will contain
    # the counties, and the geolocations of each county.

    county_string = f'{county} County, California'
    geolocations = obtaining_new_geolocations_attempt2(county_string)
    x_coordinate = geolocations[0]
    y_coordinate = geolocations[1]
    list_of_attributes = [awarding_body, url, county, x_coordinate, y_coordinate]

    allocate_attributes_within_csv(list_of_attributes)

    print(f'Awarding Body: {awarding_body}\nCounty: {county}\nGeolocations: ({x_coordinate},{y_coordinate})')



    









'''
The following function is a mechanism to open each url of a planetbid website based on a given
url, redirect the selenium driver (planetbids is built in javascript, which restricts the use
of Beautifulsoup) to the first bid within the front page bids tabulation, and acquire the value of
the County part of the bid. We will convert that value into a string, and use it for the rest of
our functions.
'''
def acquiring_county_of_bid(url, awarding_body):
    
    # Here we will utilize a similar functionaly of the function above, but in this case we will
    # also access the first bid within the front page bid tabulation, and search for the value in
    # the 'County' part of the bid description, after that, we will use another function to create
    # a string with the county in it in order to acquire the geolocation of the county, then, using
    # an additional function we will store all of the values into a csv file for each iteration in
    # order to forbid progress from being lost.


    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)
    tbody = driver.find_element(By.TAG_NAME,'tbody')
    tr_elements = tbody.find_elements(By.TAG_NAME,'tr')
    tr_elements[0].click()
    time.sleep(3)

    ember_views = driver.find_elements(By.XPATH,"//div[@class='ember-view']")
    for ember_view in ember_views:
        row_class = ember_view.find_element(By.CLASS_NAME,'row')
        
        if row_class.text.split('\n'):
            if 'County' == row_class.text.split('\n')[0]:
                county = row_class.text.split('\n')[1]
            else:
                pass
        else:
            county = 'none'

    county_geolocation_acquisition(county,url,awarding_body)

    driver.quit()


            
        

'''
If a link doesn't work, I want to know why, and perhaps attempt its webscraping extraction
differently. This is why I will dedicate a function to all the faulty planetbids websites
in order to include them differently, either it works, or it works.
'''
def faulty_county_of_bid(url,awarding_body):
    
    # Just a simple allocation into the csv file. The headers of the file are the 
    # following: AwardingBody, WebLink, County, X_Coordinates, and Y_Coordinates.
    # Adjust comment/variable name below accordingly:
    
    #file_name = 'faulty_planetbids_sites.csv'
    file_name = 'regurgitation_faulty_planetbids_sites.csv'

    df = pd.DataFrame({
        "WebLink":[url],
        "AwardingBody":[awarding_body]
    })

    if not os.path.isfile(file_name):
        df.to_csv(file_name, index=False, header=True, mode='w')

    else:
        df.to_csv(file_name, index=False, header=False, mode='a')





'''
Change of plans ladies and gentlemen, we will modify the initial planetbids_sites.csv file by
adding the County column next to each of the sites. Apparently the title of the awarding body in
question was not enough to figure out the location of each bid. I am assuming that the county is
enough to obtain a geolocation, right? Let's test that hypothesis first.
'''
def planetbids_site_county_and_geolocation(planetbids_sites, count):
    
    # First, we will iterate through each of the planetbids sites, in each of them, we will collect
    # the county from the first bid within the bid tabulation of each site. I understand that this 
    # process will be time consuming, but that's why we have a different laptop for webscraping.
    # After acquiring the county, we will create a string with the county in it to find the 
    # respective geolocation simultenously. This is risky as it might break down and start the iteration
    # again, however, that is why we will be storing and appending the results in a new csv file after
    # each iteration in order to not lose progress. That's also why the reasoning behind the count
    # variable within the inputs of this function.

    df = pd.read_csv(planetbids_sites, low_memory=False)
    total_rows = len(df)

    for index, row in df.iloc[count:].iterrows():

        url = row['WebLink']
        awarding_body = row['AwardingBody']
        try:
            print(f'\nIteration #{index}\nPercentage Completed: {round((index/total_rows)*100,2)}%')
            acquiring_county_of_bid(url, awarding_body)
            
        except:
            print(f'\nSomething occurred at {index} - {awarding_body}\n')
            faulty_county_of_bid(url, awarding_body)




'''
Part of Step 4: If the Multi-Browser Functionality does not work, we want to know why, and check the 
links that did not work out for some reason. We already know the links that do not work for certain, 
so every other link must work, no matter what.
'''
def faulty_multi_browser_to_csv(list_of_attributes):

    # The headers for the csv file are the following: AwardingBody, PlanetbidsABLink, County,
    # X_Coordinates, and Y_Coordinates. This is only for future refinement purposes.

    file_name = 'faulty_real_time_planetbids_bids.csv'
        
    df = pd.DataFrame({
        "AwardingBody": [list_of_attributes[0]],
        "PlanetbidsABLink": [list_of_attributes[1]],
        "County": [list_of_attributes[2]],
        "X_Coordinates": [list_of_attributes[3]],
        "Y_Coordinates": [list_of_attributes[4]],
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

    # The headers for the csv file are the following: AwardingBody, PlanetbidsABLink, County,
    # X_Coordinates, Y_Coordinates, DatePosted, BidName, SolicitationNumber, DueDate, DueTime,
    # SubmissionMethod, and BidUrl.

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


    # Testing area... Apparently it is better if we parse the html content into strings, rather than
    # opening the selenium session itself. The Selenium Grid functionality is quite fast, which is 
    # why we are going to implement a WebDriverWait step below in order to secure position within
    # the webdriver session is completed once we find the <tbody> element, which is where all bids
    # are located.

    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(command_executor="http://localhost:4444", options=options)
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME,'tbody'))
        )
    
    except:
        print('nope')
        driver.quit()
        return None
    
    html = driver.page_source
    driver.quit()
    return html,url




'''
Part of Step 4: Apparently parsing the html content yields better strings when it comes to webscraping
with selenium, let's try that.
'''
def html_parsing(function_input):

    
    # Like I said, testing area. We are going to assimilate the functionality from Step 1, we are
    # going to find those Selenium Attributes within the html code, and allocate them into a csv file
    # accordingly, nothing is going to change, except for the way we webscrap the code, the storage
    # mechanism will remain.

    html_content = function_input[0]
    data = HTMLParser(html_content)

    current_planetbids_url = function_input[1]
    unique_planetbids_site_id_number = str(current_planetbids_url).split('/')[4]

    tbody = data.css_first('tbody')
    tr_elements = tbody.css('tr')
    total_active_bids = 0

    list_of_attributes_main = []

    for individual_tr_element in range(len(tr_elements)):


        # For every active bid that we find, we are going to split its text form string
        # by empty spaces in order to acquire each information attribute about the bid.
        # We can calculate the dates ourselves later, right now we just need the important
        # attributes such as solicitation number, due date, due time, date posted, its link,
        # and its submission format. We will need to break down the <tr> elements into 
        # individual <td> elements and assign each index to a value. Like I said, stratification
        # process. 

        # List of attributes order:
        # 1) PlanetbidsActiveBidLink
        # 2) DatePosted
        # 3) BidName
        # 4) SolicitationNumber
        # 5) DueDate
        # 6) DueTime
        # 7) SubmissionMethod
        # 8) AwardingBodyPlanetbidsLink

        # The following variable is the string containing all attributes of the bid within the bid tabulation. This
        # will be our main variable to extract all of the attributes from.

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
    urls = df['WebLink'].values.tolist()[count:4]
    remaining_attributes = df[['AwardingBody','WebLink','County','X_Coordinates','Y_Coordinates']]

    # The following attributes have to be included somehow:

        # 1) AwardingBody
        # 2) County
        # 3) X_Coordinates
        # 4) Y_Coordinates

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(enhanced_webscraping_html,urls))

    for res in range(len(results)):
        extra_attributes = remaining_attributes.loc[res].values.tolist()
        
        # The following two lists are going to be appended to the respective csv file in question.
        # Perhaps we can even build (if we have time) a way to see if there were faulty planetbids
        # urls, we need to check the effectiveness of this Multi-Browser functionality.
        
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
    
    # The goal of this program is to build a rudimentary "real-time" planetbids update of 
    # projects being active currently. I.e. we will build a webscraping of just the projects 
    # being actively bidding, then we will use that date information to display them in our
    # website. From there, practice will reveal the proper appraoch to remove the quotations
    # from "real-time" since right now is not technically real time, but delayed. We will 
    # also use an additional file to check if a location is found within the title of the
    # owner inside the planetbids site.

    planetbids_sites_csv_file = 'planetbids_sites.csv' # Step 1 Input
    active_bids_planetbids = 'real_time_planetbids_bids.csv' # Step 4 Input - Step 1 Output
    refined_planetbids_sites = 'refined_planetbids_sites.csv' # Step 3 & 1 Input - Step 2 Output
    faulty_planetbids_sites = 'faulty_planetbids_sites.csv' # Step 3 Input - Step 2 Output
    
    start_time = time.time()

    step = int(input('Step: ')) 

    match step:

        case 1:


            # Step 1 - Real Time Bids: The one and only step to do here is to iterate through each of the planetbids sites,
            # scroll a few scrolls down in order to acquire all of the active bids, collect their
            # date information, acquire the geolocation of the respective city on planetbids 
            # displayed on their title (yes, only the city, we cannot have the exact address.), and
            # store it into a csv file with geolocations in order to be quickly displayed. The 
            # following function will have several more functions in usage as well.

            # Files Input (Refinement):
            # 1) refined_planetbids_sites.csv

            # Files Output:
            # 1) real_time_planetbids_bids.csv


            count = int(input('Count: '))
            planetbids_sites_iteration(refined_planetbids_sites, count)


        case 2:


            # Step 2 - Department Locations: We changed our minds, instead of using the title webpage string as
            # an indicator for location of the real time planetbids bid, we will first iterate through all of 
            # the planetbids sites, use any of the bids (whether open or closed) to find out about the county 
            # where the website is located, apparently (and I might be mistaken) the County section for every
            # bid is the same, so let's test that hypothesis with this step.

            # Files Input:
            # 1) planetbids_sites.csv 

            # Files Output:
            # 1) refined_planetbids_sites.csv
            # 2) faulty_planetbids_sites.csv


            count = int(input('Count: '))
            planetbids_site_county_and_geolocation(planetbids_sites_csv_file, count, step)


        case 3:


            # Step 3 - Regurgitation Iteration: One of the output files from the function above is a two-column
            # csv file containing the planetbids urls that were faulty in the previous session, let's try to 
            # iterate through them once more. Just make sure you change the respective files based on whether
            # the operation is a regurgitation or not.

            # Files Input:
            # 1) The regurgitation of faulty_planetbids_sites.csv

            # Files Output:
            # 1) The regurgitation of faulty_planetbids_sites.csv from the previous step.
            # 2) The regurgitation of faulty_planetbids_sites.csv from the previous step.
            
            count = int(input('Count: '))
            planetbids_site_county_and_geolocation(faulty_planetbids_sites, count)

        case 4:

            
            # Step 4 - Enhanced Webscraping: We are going to utilize different webscraping techniques in order to
            # try to enhance, optimize, and hasten webscraping with multiple selenium sessions. This might decrease
            # our amount of time it takes to approach different webscraping techniques, and who knows, it might
            # lead to a new way of doing things.

            # Files Input:
            # 1) refined_planetbids_sites.csv


            count = int(input('Count: '))
            enhanced_planetbids_webscraping(refined_planetbids_sites, count)





    # I just want to check the statistics later on, perhaps we can even build something here
    # to see how our code speed improves, worsens, or remains the same over time. Or even get 
    # the statistics of the proportional results between lines of code and execution time. We
    # will see...

    end_time = time.time()

    total_execution_time = end_time - start_time
    print(f'\nTook {round(total_execution_time,2)} seconds to execute this code\n')
        

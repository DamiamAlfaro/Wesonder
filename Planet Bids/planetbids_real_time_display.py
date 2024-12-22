import pandas as pd
import time
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




'''
We will utilize the file containing all California places to correlate the title
of the owner within each planetbids site with a county in California which we will
later use to display by allocating a general geolocation to each of the 57 counties
in the state. 
'''
def location_check(title_string):

    # One thing that we need to secure is that the title_string has to be in the same
    # string format as the california places. In this case, the csv file contains
    # the respective places in Title form.

    title_string = str(title_string).title()
    california_places = 'california_places.csv'
    df_cali_places = pd.read_csv(california_places,low_memory=False)
    towns_municipalities_cities = list(df_cali_places['Location'])
    counties = list(df_cali_places['County'])
    combined_places = list(zip(towns_municipalities_cities, counties))




'''
As usual, we will allocate the attributes of each bid into a csv file for later usage.
'''
def attributes_into_csv(list_of_attributes):

    # The headers for the csv file are the following: DatePosted, BidName, SolicitationNumber,
    # DueDate, DueTime, SubmissionMethod, BidPlanetbidsLink, AwardingBody, and WebPageTitle.

    df = pd.DataFrame({
        "DatePosted":[list_of_attributes[0]],
        "BidName":[list_of_attributes[1]],
        "SolicitationNumber":[list_of_attributes[2]],
        "DueDate":[list_of_attributes[3]],
        "DueTime":[list_of_attributes[4]],
        "SubmissionMethod":[list_of_attributes[5]],
        "BidPlanetbidsLink":[list_of_attributes[6]],
        "AwardingBody":[list_of_attributes[7]],
        "WebPageTitle":[list_of_attributes[8]]
    })

    df.to_csv('real_time_planetbids_bids.csv',index=False,header=False, mode='a')




'''
The following function is to webscrap the active projects from each planetbids
sites in order to display them later. The goals with the following function is
to 1) get the name of the town/city/county associated with the weblink, and
2) acquire the data information for the active bids within the weblink in question.
'''
def planetbids_active_bids_webscraping(url, awarding_body):
    
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)

    # We will utilize the stratification functionality: we will enter several layes of
    # html elements in order to acquire the desired datum from each of the tabulations
    # of each planetbids site. Also, don't forget the title indicating the location. You
    # know what, let's start with that. Additionally, we need to breakdown the url in order
    # to acquire the unique url link for that particular bid page. This will facilitate 
    # the acquisition of bid links.

    unique_planetbids_site_id_number = str(url).split('/')[4]
    site_title = driver.find_element(By.TAG_NAME,'h4').text
    
    
    #location_check(site_title)

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

        individual_tr_element_string = tr_elements[individual_tr_element].text

        if 'Bidding' in individual_tr_element_string:

            total_active_bids += 1
            
            print(f"Bid #{individual_tr_element}")

            list_of_attributes = []

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

            list_of_attributes.append(awarding_body)
            print(f'Awarding Body: {awarding_body}')

            list_of_attributes.append(site_title)
            print(f'Bid Title: {site_title}\n')



            attributes_into_csv(list_of_attributes)

            

        else:
            pass

    print(f'\n{awarding_body} Total Active Bids = {total_active_bids}')




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


    for index, row in df.iloc[count:].iterrows():
        
        awarding_body = row['AwardingBody']
        weblink = row['WebLink']
        print(f'Current Iteration: {index}')

        try:
            planetbids_active_bids_webscraping(weblink, awarding_body)
            percentage_completed = round((index/len(df)) * 100, 2)
            print(f'\nPercentage Completed: {percentage_completed}%\n')

        except:
            print(f'\n{awarding_body}: None\n')
        







if __name__ == "__main__":
    
    # The goal of this program is to build a rudimentary "real-time" planetbids update of 
    # projects being active currently. I.e. we will build a webscraping of just the projects 
    # being actively bidding, then we will use that date information to display them in our
    # website. From there, practice will reveal the proper appraoch to remove the quotations
    # from "real-time" since right now is not technically real time, but delayed. We will 
    # also use an additional file to check if a location is found within the title of the
    # owner inside the planetbids site.


    try: 
        planetbids_sites_csv_file = 'planetbids_sites.csv'
        

        step = int(input('Step: ')) # 545

        match step:

            case 1:

                # The one and only step to do here is to iterate through each of the planetbids sites,
                # scroll a few scrolls down in order to acquire all of the active bids, collect their
                # date information, acquire the geolocation of the respective city on planetbids 
                # displayed on their title (yes, only the city, we cannot have the exact address.), and
                # store it into a csv file with geolocations in order to be quickly displayed. The 
                # following function will have several more functions in usage as well.

                count = int(input('Count: '))
                planetbids_sites_iteration(planetbids_sites_csv_file, count)

    except:
        print("Gone")












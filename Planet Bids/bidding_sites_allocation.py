import sys
import pandas as pd
import os
import re
import numpy as np
from pandas.errors import EmptyDataError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time








'''
Here we will create a dataframe for each city that contains
three headers: City, BiddingSite, BiddingSiteLink
'''
def municipality_bidding_site_dataframe(name_of_city, links_list):

    # BiddingSite Column
    bidding_sites = []

    # BiddingSiteLink Column
    bidding_site_links = []
    
    '''
    Using the links list, separate the links and pinpoint the
    BiddingSite and add it to the respective lists for eventual 
    DataFrame addition.
    '''
    for link in links_list:
        link_list_position = links_list.index(link)
        slash_instance = link.index("/",8,len(link))
        bidding_site = link[8:slash_instance]
    
        # Check if the bidding site is already added, but skip for Planetbids
        if "planetbids" not in bidding_site and bidding_site not in bidding_sites:
            bidding_sites.append(bidding_site)
            bidding_site_links.append(link)
        
        # Do the case for Planetbids
        elif "planetbids" in bidding_site:
            pb_site_id_number = link[38:43]
            pb_reconstructed_link = f"https://vendors.planetbids.com/portal/{pb_site_id_number}/bo/bo-search"
            if pb_reconstructed_link not in bidding_site_links:
                bidding_sites.append(bidding_site)
                bidding_site_links.append(pb_reconstructed_link)

    # Check if the links and bidding site are the same length. Why? Because the dataframe requires equal column size.
    length_check = len(bidding_sites) == len(bidding_site_links)
    print(len(bidding_sites))
    if length_check == True:

        # Municipalities Column
        municipality_name = [name_of_city for instances in range(len(bidding_sites))] 
        print(municipality_name)
        

            







    '''
    Create the dataframe with City, BiddingSite, and BiddingSiteLink
    '''
    df = pd.DataFrame()
    





'''
This function is only to search, extract, and allocate in file.
'''
def municipalities_bidding_platforms_search(df):

    '''
    Focus on the CITY Column only
    '''
    df_cities = df.iloc[:,0]

    '''
    Start the Google Session
    '''
    test = df_cities[0]
    
    # Open the WebDriver
    driver = webdriver.Chrome()

    # Create a searchable string with only changeable city
    searchable_string = f"{test} bids"

    # Search for that string
    driver.get("https://google.co.in/search?q=" + searchable_string)
    time.sleep(3)

    '''
    Extract the websites (not links) that appear in the search
    '''    
    try:
        # Secure position within the search results
        google_results = WebDriverWait(driver,3).until(
                EC.presence_of_element_located((By.ID,"search")))

        # Extract all links for deconstruction
        google_result_page = google_results.find_elements(By.XPATH,"//a[@jsname='UWckNb']")

        # Deconstruct the links and extract their hrefs
        google_result_links = [a_tag.get_attribute("href") for a_tag in google_result_page]
        

    except:
        print("failure with extraction of links")


    '''
    Create the Bidding Site Dataframe for the respective city
    '''
    municipality_bidding_site_dataframe(test,google_result_links)





    return "\nexecuted\n"
















if __name__ == "__main__":
    
    # Retrieve the municipalities file
    awarding_bodies_file = "../data/dir_entities_refined.csv"
    df = pd.read_csv(awarding_bodies_file)

    
    # Search for the Municipality's bidding site
    print(municipalities_bidding_platforms_search(df))

    




















































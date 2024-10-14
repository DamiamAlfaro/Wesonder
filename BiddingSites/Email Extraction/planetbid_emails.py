import pandas as pd
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
The actual web crawling
'''
def webscraping_planetbids():
    pass


















if __name__ == "__main__":
    
    # Bidding Sites csv file
    bidding_sites_data_csv = "bidding_sites_data.csv"

    extracting_only_planetbids(bidding_sites_data_csv)


import pandas as pd
import os
import requests # type: ignore
from bs4 import BeautifulSoup
import time
from playwright.sync_api import sync_playwright # type: ignore







# Webscrap data from the invidiual link
def webscrap_individual_link(url):

    # Cook the stew
    url = f'{url}#bidPBs'

    # with sync_playwright() as session:
    #     browser = session.chromium.launch(headless=True)
    #     page = browser.new_page()
    
    # Set up session

    # Find the respective variables to scrap
    
    


# Iterates through a singular csv file
def reading_individual_csv_file(individual_csv_file):
    
    # Read the file
    df = pd.read_csv(individual_csv_file)
    
    # Count
    count = 0

    # Iterate through the file
    for index, row in df.iloc[count:].head(1).iterrows():
        
        # Set variables
        awarding_body = row['AwardingBody']
        awarding_bpdy_link = row['AwardingBodyPBLink']
        project_link = row['UniqueBidPBLink']

        # Access the information from via webscraping
        webscrap_individual_link(project_link)





'''
We will be downloading the files, and iterate through its folder
in order to extract each of the links
'''
if __name__ == "__main__":

    with sync_playwright() as p:
        p.install()  # This will download the required browser binaries

    '''
    Folder total = 1417
    Current Iteration Session 1: 5 (0-1417) - Total Files
    '''

    # Folder name
    folder_with_files = 'accurate/'

    # Folder access
    folder_location = os.listdir(folder_with_files)

    # Count
    count = 0
    
    # Iteration through the folder access
    for file in range(count, len(folder_location)):

        # Assign the name of the file
        file_name = f"{folder_with_files}{folder_location[file]}"
        
        # Iterate through the file
        reading_individual_csv_file(file_name)

    








import pandas as pd # type: ignore
import time
import sys
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore


'''
Locate the CSI codes first since we are not going to iterate through all of them,
just the ones that actually require manufacturers.
'''
def webscraping_costcodes(url):

    # Initiate the driver
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)

    # Locate the CSI Divisions
    divisions = driver.find_elements(By.CLASS_NAME, 'p1')

    # Single page approach: retrieving the link url of elements, and webscraping them in a separate webdriver session
    division_links = []
    
    # Iterate through each division and extract each division link from it
    for division in divisions:

        division_a_tag = division.find_element(By.TAG_NAME,'a')

        url_link = division_a_tag.get_attribute('href')
        division_links.append(url_link)

    driver.quit()

    # Jump to the next function
    return division_links


'''
Webscrap the data for each manufacturer
'''
def webscraping_manufacturers_data(url):
    pass























if __name__ == "__main__":

    # The main url link
    url = 'https://www.arcat.com/content-type/product'

    # Pinpoint a list with all main divisions from the website for further analysis
    division_links = webscraping_costcodes(url)

    for i in division_links:
        print(i)
          
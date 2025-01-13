import pandas as pd
import time
import re
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC


start_time = time.time()


def entering_the_site(url_site):

    # The first step is to remove the annoying pop-up display as soon as one enters the website,
    # which I assume is implemented to prevent bot attacks, which I mean, we are talking about the
    # U.S. Government, they aren't that smart...

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run Chrome in headless mode
    options.add_argument('--disable-gpu')  # Disable GPU acceleration (required for headless mode on Windows)
    options.add_argument('--disable-extensions')  # Disable extensions for faster loading
    options.add_argument('--no-sandbox')  # Security sandbox can be disabled (usually for non-production use)
    options.add_argument('--disable-dev-shm-usage')  # Avoid shared memory issues
    options.add_argument('--window-size=1920,1080')  # Set viewport size explicitly
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36')  # Mimic a real browser user-agent
    options.add_argument('--start-maximized')  # Start the browser maximized (simulating a normal environment)
    driver = webdriver.Chrome(options=options)
    driver.get(url_site)
    time.sleep(2)

    close_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'close-btn'))
    )
    close_button.click()
    time.sleep(2)

    dropdown_menu = driver.find_element(By.ID,"bottomPagination-select")
    select = Select(dropdown_menu)
    options = select.options
    select.select_by_index(len(options) - 1)
    time.sleep(2)

    return driver


def bid_page_source(url):

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run Chrome in headless mode
    options.add_argument('--disable-gpu')  # Disable GPU acceleration (required for headless mode on Windows)
    options.add_argument('--disable-extensions')  # Disable extensions for faster loading
    options.add_argument('--no-sandbox')  # Security sandbox can be disabled (usually for non-production use)
    options.add_argument('--disable-dev-shm-usage')  # Avoid shared memory issues
    options.add_argument('--window-size=1920,1080')  # Set viewport size explicitly
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36')  # Mimic a real browser user-agent
    options.add_argument('--start-maximized')  # Start the browser maximized (simulating a normal environment)
    driver = webdriver.Chrome(options=options)
    
    driver.get(url)
    
    # Remove the anti-both mechanism
    close_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'close-btn'))
    )
    close_button.click()
    time.sleep(2)

    # Bid Title
    bid_title = driver.find_element(By.TAG_NAME,'h1').text
    print(bid_title)
    
    


    


# # Outset: URL for general NAICS code 23 in California
# sam_url = 'https://sam.gov/search/?index=opp&page=1&pageSize=25&sort=-modifiedDate&sfm%5BsimpleSearch%5D%5BkeywordRadio%5D=ALL&sfm%5BsimpleSearch%5D%5BkeywordEditorTextarea%5D=&sfm%5Bstatus%5D%5Bis_active%5D=true&sfm%5Bstatus%5D%5Bis_inactive%5D=false&sfm%5BserviceClassificationWrapper%5D%5Bnaics%5D%5B0%5D%5Bkey%5D=23&sfm%5BserviceClassificationWrapper%5D%5Bnaics%5D%5B0%5D%5Bvalue%5D=23%20-%20Construction&sfm%5BplaceOfPerformance%5D%5Bstate%5D%5B0%5D%5Bkey%5D=CA&sfm%5BplaceOfPerformance%5D%5Bstate%5D%5B0%5D%5Bvalue%5D=CA%20-%20California'

# # Remove the anti-bot mechanism (pathetic...) and increase results displayed
# driver = entering_the_site(sam_url)

# # Now start webscraping the links to each individual bid
# page_source = driver.page_source
# soup = BeautifulSoup(page_source, 'html.parser')
# individual_links = soup.find_all('h3',class_='margin-y-0')
# individual_links = [link.find('a').get('href') for link in individual_links]
# individual_links = [f'https://sam.gov{link}' for link in individual_links]
# driver.quit()

# Once acquired, webscrap each of them
df = pd.read_csv('sam_gov_bids.csv')
individual_links = df['SamGovUrls']

for sam_bid in individual_links[:1]:

    page_source = bid_page_source(sam_bid)
    










end_time = time.time()
elapsed_seconds = end_time-start_time
elapsed_minutes = round(elapsed_seconds/60,2)
elapsed_hours = round(elapsed_minutes/60,2)
print(f'\nTotal Seconds to Execute main.py:\nSeconds = {elapsed_seconds}\nMinutes = {elapsed_minutes}\nHours = {elapsed_hours}')

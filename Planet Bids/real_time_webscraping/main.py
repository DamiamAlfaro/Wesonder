import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def site_html_webscrap(url):
    # Set Chrome options for headless mode
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize Chrome WebDriver
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # SiteAwardingBody
    site_awarding_body = soup.find('h4')

    # Find the <tbody> where all bids are located, followed by <td>
    tbody = soup.find('tbody')
    all_tr = tbody.find_all('tr')
    active_bids = []

    # Iterate through each <tr> tag (each <tr> reprents a bid, regardless of status)
    for tr_tag in all_tr:
        all_td = tr_tag.find_all('td')
        for td_tag in all_td:
            if td_tag.get('title') == 'Bidding':
                print(tr_tag.text)
                active_bids.append(tr_tag)



    time.sleep(2)
    driver.quit()


# Load URLs from Google Cloud Storage
planetbids_sites_csv = 'https://storage.googleapis.com/wesonder_databases/Planetbids/refined_planetbids_sites.csv'
df = pd.read_csv(planetbids_sites_csv)

i = 1

for index, row in df.iloc[i:i+1].head(1).iterrows():  # Adjust the number of rows as needed
    awarding_body = row['AwardingBody']
    weblink = row['WebLink']
    county = row['County']
    x_coord = row['X_Coordinates']
    y_coord = row['Y_Coordinates']

    print(weblink)
    site_html_webscrap(weblink)  # Scrape the website


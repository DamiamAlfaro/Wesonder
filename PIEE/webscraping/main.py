import pandas as pd
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

initial_time = time.time()

piee_url = 'https://piee.eb.mil/sol/xhtml/unauth/index.xhtml'

# The following is copied from other programs where we use Headless Selenium sessions
# options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Run Chrome in headless mode
# options.add_argument('--disable-gpu')  # Disable GPU acceleration (required for headless mode on Windows)
# options.add_argument('--disable-extensions')  # Disable extensions for faster loading
# options.add_argument('--no-sandbox')  # Security sandbox can be disabled (usually for non-production use)
# options.add_argument('--disable-dev-shm-usage')  # Avoid shared memory issues
# options.add_argument('--window-size=1920,1080')  # Set viewport size explicitly
# options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36')  # Mimic a real browser user-agent
# options.add_argument('--start-maximized')  # Start the browser maximized (simulating a normal environment)
# driver = webdriver.Chrome(options=options)

driver = webdriver.Chrome()
driver.get(piee_url)
time.sleep(2)

# Locate the Search button in the navbar
piee_navbar = driver.find_element(By.CSS_SELECTOR,"ul.navbar-nav")
navbar_items = piee_navbar.find_elements(By.TAG_NAME,"li")
search_button = navbar_items[0]
search_button.click()
time.sleep(4)

# Once in the PIEE Search Page, we need to send the desired values to the input boxes of our choice
# that will display all of the bids that meet our criteria











































import pandas as pd
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

initial_time = time.time()
piee_url = 'https://piee.eb.mil/sol/xhtml/unauth/index.xhtml'
driver = webdriver.Chrome()
driver.get(piee_url)
time.sleep(2)

# Locate the Search button in the navbar
piee_navbar = driver.find_element(By.CSS_SELECTOR,"ul.navbar-nav")
navbar_items = piee_navbar.find_elements(By.TAG_NAME,"li")
search_button = navbar_items[0]
search_button.click()
time.sleep(2)

# Once in the PIEE Search Page, we need to send the desired values to the input boxes of our choice
# that will display all of the bids that meet our criteria. Locate the desired input sections

# First input
naics_input = driver.find_element(By.ID, "naics")
naics_input.send_keys("236220")

# Second input
dropdown = Select(driver.find_element(By.ID, "status"))
dropdown.select_by_value("O")
time.sleep(2)

# Search results
search_link = driver.find_element(By.ID, "search")
search_link.click()
time.sleep(2)

# Locate the total bids and iterate through each
total_bids_result = int(driver.find_element(By.TAG_NAME,'h3').text.split(' ')[2][1:])


splitted_current_bids = driver.find_element(By.ID,'DataTables_Table_0_info').text.split(" ")
x = int(splitted_current_bids[1])
y = int(splitted_current_bids[3])
total_displayed_bids = y - (x-1)

bid_turn = 0
current_page = 1

while bid_turn != total_displayed_bids:

    # Re-locate table and bids
    bid_table = driver.find_element(By.TAG_NAME, 'tbody')
    all_bids = bid_table.find_elements(By.TAG_NAME, 'tr')

    # Locate the current bid link
    td_element = all_bids[bid_turn].find_elements(By.TAG_NAME, 'td')
    link_to_new_page = td_element[0].find_element(By.TAG_NAME, 'a')

    # Scroll to the link and ensure it's clickable
    driver.execute_script("arguments[0].scrollIntoView();", link_to_new_page)

    try:
        # Wait until the link is clickable and then click
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.TAG_NAME, 'a'))
        )
        link_to_new_page.click()
        bid_title = driver.find_element(By.TAG_NAME,'h4').text
        print(bid_title)
    except Exception as e:
        print(f"Error clicking link at bid_turn {bid_turn}: {e}")
        bid_turn += 1
        continue

    # Wait and go back
    time.sleep(2)

    # Click the previous button to return
    previous_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "previous"))
    )
    previous_button.click()
    time.sleep(2)

    # Increment bid_turn
    print(bid_turn)
    bid_turn += 1
    

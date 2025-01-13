import pandas as pd
import math
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

start_time = time.time()

global_bid_turn = 0

def iterating_through_first_results(driver):
    splitted_current_bids = driver.find_element(By.ID,'DataTables_Table_0_info').text.split(" ")
    x = int(splitted_current_bids[1])
    y = int(splitted_current_bids[3])
    total_displayed_bids = y - (x-1)

    bid_turn = 0
    bid_titles = []
    global global_bid_turn


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
            bid_titles.append(bid_title)
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
        bid_turn += 1
        global_bid_turn += 1
        print(f'Current Bid #{global_bid_turn}: {bid_titles[bid_turn-1]}')
    

# The function we will use after the first 20 results, fucking poor website design...
def switching_pages(driver_session, current_pages_id):
    
    # Locate the next page button and go to it
    next_page_bar = driver_session.find_element(By.CLASS_NAME,'pagination')
    next_page_button = next_page_bar.find_elements(By.CLASS_NAME,'paginate_button')[2+current_pages_id].find_element(By.TAG_NAME,'a')
    driver_session.execute_script("arguments[0].scrollIntoView(true);", next_page_button)
    time.sleep(2)
    next_page_button.click()
    time.sleep(2)


def iterating_through_other_results(driver, current_pages_id):
    splitted_current_bids = driver.find_element(By.ID,'DataTables_Table_0_info').text.split(" ")
    x = int(splitted_current_bids[1])
    y = int(splitted_current_bids[3])
    total_displayed_bids = y - (x-1)

    bid_turn = 0
    bid_titles = []
    global global_bid_turn

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
            bid_titles.append(bid_title)
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

        switching_pages(driver, current_pages_id)

        # Increment bid_turn
        bid_turn += 1
        global_bid_turn += 1
        print(f'Current Bid #{global_bid_turn}: {bid_titles[bid_turn-1]}')










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
total_pages = math.ceil(total_bids_result/20)
current_pages = 1

# First 20 results iteration
iterating_through_first_results(driver)


# Iterates through the 20 results of the current page
while current_pages != total_pages:

    # Assign the current_pages page
    current_pages_id = current_pages - 1

    # Switching to next pages
    switching_pages(driver, current_pages_id)
    iterating_through_other_results(driver, current_pages_id)

    current_pages += 1
    


end_time = time.time()
elapsed_seconds = end_time-start_time
elapsed_minutes = round(elapsed_seconds/60,2)
elapsed_hours = round(elapsed_minutes/60,2)
print(f'Total Seconds to Execute main.py:\nSeconds = {elapsed_seconds}\nMinutes = {elapsed_minutes}\nHours = {elapsed_hours}')

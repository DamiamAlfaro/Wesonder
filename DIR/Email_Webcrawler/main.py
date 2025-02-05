import pandas as pd
import time
import sys
import os
import csv
import re
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



start_time = time.time()




def dir_emails_extraction(url):
    # Begin the opening with Selenium
    driver = webdriver.Chrome()
    collected_emails = []  # Store emails here

    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "panel-title"))
        )

        # Finding the target within the tabulation display
        tabulation_of_entities = driver.find_element(By.TAG_NAME, "table")
        trbody_tag = tabulation_of_entities.find_element(By.TAG_NAME, "tbody")
        entity_targets = trbody_tag.find_elements(By.TAG_NAME, "tr")

        # Iterate through each entity
        for entity in range(1, len(entity_targets) + 1):
            entity_xpath = f'//tbody/tr[{entity}]'

            try:
                entity_located = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, entity_xpath))
                )
                driver.execute_script("arguments[0].scrollIntoView();", entity_located)
                entity_located.click()

                # Wait until the name or email field is present
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, "sp_formfield_name"))
                )

                # Extract entity attributes
                name = driver.find_element(By.ID, "sp_formfield_name").get_attribute("value")
                email = driver.find_element(By.ID, "sp_formfield_email").get_attribute("value")

                if name == "":
                    name = "none"
                elif email == "":
                    email = "none"

                collected_emails.append([name, email])

                # Back to the previous page
                driver.back()
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.TAG_NAME, "table"))
                )

            except:
                print(f"Timeout while processing entity {entity} at {url}")
                continue

    except Exception as e:
        print(f"Error occurred at {url}: {e}")
        sys.exit(1)

    finally:
        driver.quit()  # Ensure the browser is closed

    return collected_emails



# Allocate respectively to csv
def allocation_into_csv(list_of_lists):
    
    file_name = "dir_email_collection4.csv"
    file_exists = os.path.isfile(file_name)

    # Open the file in append mode ('a'), create if it doesn't exist
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)

        # Write header only if the file is new
        if not file_exists:
            writer.writerow(['Name', 'Email'])  # Add headers as needed

        # Write the data (list of lists)
        writer.writerows(list_of_lists)








# Outset
# for i in range(0, 5532): # 5532 as of 02/03/2025

#     dir_url = f"https://services.dir.ca.gov/gsp?id=dir_contractors&table=x_cdoi2_csm_portal_customer_account_lookup&view=public&sysparm_fixed_query=type%3D2&filter=type%3D2&spa=1&p={i}&o=crafts&d=asc"
#     emails = dir_emails_extraction(dir_url)
#     allocation_into_csv(emails)
#     print(i)
    
# After the events...
new_csv = "dir_emails_refined.csv"
df = pd.read_csv(new_csv, encoding='ISO-8859-1')
print(len(df))
df_refined = df[df["Email"] != 'none']
print(len(df_refined))
df_refined.to_csv('dir_emails_refined_2.csv',header=False,index=False)





'''
Time Statistics
'''
end_time = time.time()
elapsed_time = end_time - start_time
elapsed_hours = round((elapsed_time / 60 / 60), 3)
print(f'Total Hours to Execute: {elapsed_hours}')














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

# Retry attempt limit
MAX_RETRIES = 3


def entering_the_site(url_site):

    # The first step is to remove the annoying pop-up display as soon as one enters the website...
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


def bid_attributes(url, retries=0):

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run Chrome in headless mode
    options.add_argument('--disable-gpu')  # Disable GPU acceleration (required for headless mode on Windows)
    options.add_argument('--disable-extensions')  # Disable extensions for faster loading
    options.add_argument('--no-sandbox')  # Security sandbox can be disabled (usually for non-production use)
    options.add_argument('--disable-dev-shm-usage')  # Avoid shared memory issues
    options.add_argument('--window-size=1920,1080')  # Set viewport size explicitly
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36')  # Mimic a real browser user-agent
    options.add_argument('--start-maximized')  # Start the browser maximized (simulating a normal environment)
    
    try:
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

        # Grid with more items: Notice ID, Related Notice, and Government Departments
        attribute_grid = driver.find_element(By.CSS_SELECTOR, 'div.sam-ui.attached.grid')
        
        # Notice ID
        notice_id = attribute_grid.find_element(By.ID,"header-solicitation-number")
        notice_id = notice_id.find_element(By.CLASS_NAME,"description").text

        # Related Notice
        related_notice = attribute_grid.find_element(By.ID,"header-related-notice")
        try:
            related_notice = related_notice.find_element(By.CLASS_NAME,"description").text
        except:
            related_notice = "none"

        # Department(s)
        departments = attribute_grid.find_element(By.ID,"header-hierarchy-level")
        try:
            department_tiers = [tier.text for tier in departments.find_elements(By.CLASS_NAME, "header")]
            department_tiers = ";".join(department_tiers) if department_tiers else "none"
            
            department_names = [name.text for name in departments.find_elements(By.CLASS_NAME, "description")]
            department_names = ";".join(department_names) if department_names else "none" 
        except Exception as e:
            department_tiers = "none"
            department_names = "none"
        

        all_attributes = [
            bid_title,
            notice_id,
            related_notice,
            department_tiers,
            department_names
        ]

        # Original Set Aside
        original_set_aside = driver.find_element(By.ID,"classification-original-set-aside").text

        # Set Aside
        set_aside = driver.find_element(By.ID,"classification-original-set-aside").text

        # Product Service Code
        service_code = driver.find_element(By.ID,"classification-classification-code").text

        # NAICS Code
        naics_code = driver.find_element(By.ID,"classification-naics-code").text

        # Place of Performance
        location = driver.find_element(By.ID,"classification-pop").text

        # Cleansing the strings
        class_attributes = [
            original_set_aside,
            set_aside,
            service_code,
            naics_code,
            location
        ]

        class_attributes = [
            t.split(":")[1].replace("\n","").replace("\t","") for t in class_attributes
        ]

        all_attributes.extend(class_attributes)
        all_attributes.append(url)

        return all_attributes
    
    except Exception as e:
        if retries < MAX_RETRIES:
            print(f"Error processing {url}. Retrying... ({retries+1}/{MAX_RETRIES})")
            return bid_attributes(url, retries + 1)  # Retry logic
        else:
            print(f"Failed to process {url} after {MAX_RETRIES} retries.")
            return None  # Return None after max retries


def attributes_to_csv(list_of_attributess):

    file_name = "sam_gov_bids.csv"
    
    df = pd.DataFrame({
        "BidTitle":[list_of_attributess[0]],
        "NoticeID":[list_of_attributess[1]],
        "RelatedNotice":[list_of_attributess[2]],
        "DepartmentTiers":[list_of_attributess[3]],
        "DepartmentNames":[list_of_attributess[4]],
        "OriginalSetAside":[list_of_attributess[5]],
        "CurrentSetAside":[list_of_attributess[6]],
        "ServiceCodes":[list_of_attributess[7]],
        "NAICS":[list_of_attributess[8]],
        "Location":[list_of_attributess[9]],
        "BidUrl":[list_of_attributess[10]]
    })

    if not os.path.isfile(file_name):
        df.to_csv(file_name, index=False, header=True, mode='w')
    else:
        df.to_csv(file_name, index=False, header=False, mode='a')


# Outset: URL for general NAICS code 23 in California
sam_url = 'https://sam.gov/search/?index=opp&page=1&pageSize=25&sort=-modifiedDate&sfm%5BsimpleSearch%5D%5BkeywordRadio%5D=ALL&sfm%5BsimpleSearch%5D%5BkeywordEditorTextarea%5D=&sfm%5Bstatus%5D%5Bis_active%5D=true&sfm%5Bstatus%5D%5Bis_inactive%5D=false&sfm%5BserviceClassificationWrapper%5D%5Bnaics%5D%5B0%5D%5Bkey%5D=23&sfm%5BserviceClassificationWrapper%5D%5Bnaics%5D%5B0%5D%5Bvalue%5D=23%20-%20Construction&sfm%5BplaceOfPerformance%5D%5Bstate%5D%5B0%5D%5Bkey%5D=CA&sfm%5BplaceOfPerformance%5D%5Bstate%5D%5B0%5D%5Bvalue%5D=CA%20-%20California'

# Remove the anti-bot mechanism (pathetic...) and increase results displayed
driver = entering_the_site(sam_url)

# Now start webscraping the links to each individual bid
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')
individual_links = soup.find_all('h3',class_='margin-y-0')
individual_links = [link.find('a').get('href') for link in individual_links]
individual_links = [f'https://sam.gov{link}' for link in individual_links]
driver.quit()

# Retry queue to hold failed sessions
failed_sessions = []

# Once acquired, webscrap each of them
for sam_bid in individual_links[:]:
    attributes = bid_attributes(sam_bid)
    if attributes:
        print(f"Successful: {sam_bid}")
        attributes_to_csv(attributes)
    else:
        print(f"Failure: {sam_bid}")
        failed_sessions.append(sam_bid)  # Add failed session to retry queue

# Retry the failed sessions
retry_attempts = 0
while failed_sessions and retry_attempts < MAX_RETRIES:
    print(f"\nRetrying failed sessions... Attempt {retry_attempts + 1}/{MAX_RETRIES}")
    retry_queue = failed_sessions.copy()
    failed_sessions = []
    for sam_bid in retry_queue:
        attributes = bid_attributes(sam_bid)
        if attributes:
            attributes_to_csv(attributes)
        else:
            failed_sessions.append(sam_bid)  # Add back to failed sessions if still not successful

    retry_attempts += 1

# After all retries, print out the failed URLs
re_attempt = []
if failed_sessions:
    print("\nThe following URLs failed after maximum retries:")
    for failed_url in failed_sessions:
        print(failed_url)
        re_attempt.append(failed_url)

df = pd.DataFrame({"FailedURLs":re_attempt}).to_csv("failed_sam_gov_bids.csv",index=False)

end_time = time.time()
elapsed_seconds = end_time-start_time
elapsed_minutes = round(elapsed_seconds/60,2)
elapsed_hours = round(elapsed_minutes/60,2)
print(f'\nTotal Seconds to Execute main.py:\nSeconds = {elapsed_seconds}\nMinutes = {elapsed_minutes}\nHours = {elapsed_hours}')

import pandas as pd
import time
import re
import os
from multiprocessing import Pool, cpu_count, Manager
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

initial_time = time.time()
total_active_bids = 0

def allocate_csv(ab, weblink, county, x_coord, y_coord, active_bids_list):
    
    file_name = 'planetbids_active_bids.csv'

    df = pd.DataFrame({
        "AllegedAwardingBody":[ab],
        "WebLink":[weblink],
        "County":[county],
        "X_Coordinates":[x_coord],
        "Y_Coordinates":[y_coord],
        "BidUrl":[active_bids_list[0]],
        "BidAwardingBody":[active_bids_list[1]],
        "BidPostedDate":[active_bids_list[2]],
        "BidTitle":[active_bids_list[3]],
        "BidInvitationID":[active_bids_list[4]],
        "BidDueDate":[active_bids_list[5]],
        "BidStatus":[active_bids_list[6]],
        "BidSubmissionMethod":[active_bids_list[7]]
    })

    if not os.path.isfile(file_name):
        df.to_csv(file_name, index=False, header=True, mode='w')

    else:
        df.to_csv(file_name, index=False, header=False, mode='a')



def site_html_webscrap(url):

    global total_active_bids

    # Initialize Chrome WebDriver
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

    # Wait until the body of bids appears before acquiring the page source
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME,'tbody'))
    )
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # SiteAwardingBody
    site_awarding_body = soup.find('h4').text
    
    # Find the <tbody> where all bids are located, followed by <td>
    tbody = soup.find('tbody')
    all_tr = tbody.find_all('tr')
    active_bids = []

    # Iterate through each <tr> tag (each <tr> reprents a bid, regardless of status)
    for tr_tag in all_tr:
        all_td = tr_tag.find_all('td')
        tr_attribute_number = tr_tag.get('rowattribute')

        for td_tag in all_td:
            if td_tag.get('title') == 'Bidding':

                total_active_bids += 1

                # Acquire the link for the bid itself
                bid_url = f"{url.replace('bo-search','bo-detail')}/{tr_attribute_number}"

                # Acquire the rest of the bid attributes
                posted_date = all_td[0].text
                bid_title = all_td[1].text
                invitation_id = all_td[2].text
                due_date = all_td[3].text
                status = all_td[5].text
                submission_method = all_td[6].text

                active_bid_attributes_ugly = [
                    bid_url,
                    site_awarding_body,
                    posted_date,
                    bid_title,
                    invitation_id,
                    due_date,
                    status,
                    submission_method
                ]
                

                active_bids_attributes_pretty = [
                    re.sub(r'\s+', ' ', string.strip()) for string in active_bid_attributes_ugly
                ]

                active_bids.append(active_bids_attributes_pretty)

    # Finish the selenium session and return the active bids of that url
    driver.quit()   
    return active_bids


def process_bid_site(args):
    row, retry_queue = args
    awarding_body = row['AwardingBody']
    weblink = row['WebLink']
    county = row['County']
    x_coord = row['X_Coordinates']
    y_coord = row['Y_Coordinates']
    result = {"index": row.name, "success": False, "error": None, "row": row}

    try:
        active_bids = site_html_webscrap(weblink)
        
        for active_bid in active_bids:
            allocate_csv(
                awarding_body,
                weblink,
                county,
                x_coord,
                y_coord,
                active_bid
            )
        
        result["success"] = True
        print(
            f"BidSite #{row.name} Complete\nURL: {weblink}\nAwarding Body: {awarding_body}\nTotal Bids: {len(active_bids)}"
        )
    except Exception as exe:
        result["error"] = str(exe)
        retry_queue.put(row)  # Add failed attempt to retry queue
        print(
            f"BidSite #{row.name} Failed - Added to retry queue\nURL: {weblink}\nAwarding Body: {awarding_body}"
        )
        print(exe)
    
    return result

def process_retry_queue(retry_queue):
    """Process items in the retry queue."""
    retry_results = []
    print("\nProcessing retry queue...")
    
    while not retry_queue.empty():
        row = retry_queue.get()
        print(f"Retrying BidSite #{row.name}")
        
        # Create a new queue for any failures during retry
        with Manager() as manager:
            new_retry_queue = manager.Queue()
            result = process_bid_site((row, new_retry_queue))
            retry_results.append(result)
            
            # If the retry also failed, log it
            if not result["success"]:
                print(f"Retry failed for BidSite #{row.name} - Giving up")
    
    return retry_results

if __name__ == "__main__":
    start_time = time.time()
    
    planetbids_sites_csv = 'https://storage.googleapis.com/wesonder_databases/Planetbids/refined_planetbids_sites.csv'
    df = pd.read_csv(planetbids_sites_csv)
    i = 0

    num_processes = min(cpu_count(), 2)
    
    # Create a managed queue for retry attempts
    with Manager() as manager:
        retry_queue = manager.Queue()
        
        # Process initial batch
        rows = [row for _, row in df.iloc[i:i+100].iterrows()]
        with Pool(processes=num_processes) as pool:
            results = pool.map(process_bid_site, [(row, retry_queue) for row in rows], chunksize=1)
        
        # Process retry queue after initial batch is complete
        retry_results = process_retry_queue(retry_queue)
        
        # Combine results
        all_results = results + retry_results
        
        # Calculate statistics
        total_attempts = len(all_results)
        successful_attempts = sum(1 for r in all_results if r["success"])
        failed_attempts = total_attempts - successful_attempts
        
        print(f'\nFinal Statistics:')
        print(f'Total Active Bids: {total_active_bids}')
        print(f'Total Attempts: {total_attempts}')
        print(f'Successful Attempts: {successful_attempts}')
        print(f'Failed Attempts: {failed_attempts}')

        # Calculate elapsed time
        end_time = time.time()
        elapsed_time = end_time - start_time
        elapsed_hours = round((elapsed_time / 60 / 60), 2)
        print(f'Total Hours to Execute: {elapsed_hours}')

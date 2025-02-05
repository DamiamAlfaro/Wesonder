import pandas as pd
import time
import sys
import re
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Counting time
start_time = time.time()




'''
[1.1] We are going to use the following function to scroll to the bottom
''' 
def scroll_table_container(container, driver, scroll_pause_time=2):
    
    last_height = driver.execute_script("return arguments[0].scrollHeight", container)
    
    while True:
        # Scroll down by a small amount within the container
        driver.implicitly_wait(4)
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", container)
        driver.implicitly_wait(4)
        
        # Wait to load the new content
        time.sleep(scroll_pause_time)
        
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return arguments[0].scrollHeight", container)
        if new_height == last_height:
            break
        last_height = new_height

    result_message = "Round Completed"
    print(result_message)




'''
[1.0] First we need to acquire the indivudal href values from each individual bid from each PB site.
We are going to utilize a past mechanism to do so.
'''
def acquiring_bid_links(pb_url):

	# PB Site ID
	pb_site_id = pb_url.split("/")[4]

	# Start the driver
	driver = webdriver.Chrome()
	driver.get(pb_url)

	# Wait
	WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.TAG_NAME,"table"))
	)

	# Awarding Body
	awarding_body_name = driver.find_element(By.TAG_NAME,"h4").text

	# Allocate the table to scroll within
	table_to_scroll = driver.find_element(By.CLASS_NAME,"table-overflow-container")
	scroll_table_container(table_to_scroll, driver)

	# Once scrolled, collect all the rowattributes
	table = driver.find_element(By.XPATH, '//table[@role="table"]').find_element(By.TAG_NAME,"tbody")
	tr_elements = table.find_elements(By.TAG_NAME,"tr")
	pb_bidders_url = []

	for tr_element in tr_elements:

		bid_id = tr_element.get_attribute('rowattribute')
		bid_url = f"https://vendors.planetbids.com/portal/{pb_site_id}/bo/bo-detail/{bid_id}#bidPBs"
		pb_bidders_url.append(bid_url)

	driver.quit()

	return pb_bidders_url, awarding_body_name, pb_url
	



'''
[2.0] "It's a expropriation, slide over"...
'''
def data_expropriation(url):

	# Initiate the driver
	driver = webdriver.Chrome()
	driver.get(url)

	# Wait for its position
	WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.TAG_NAME,"table"))
	)

	# Locate the pool of players and expripriate its attributes
	table = driver.find_element(By.XPATH, '//table[@role="table"]').find_element(By.TAG_NAME,"tbody")
	players = table.find_elements(By.TAG_NAME,'tr')

	all_players = []

	for player in players:

		player_attributes = player.find_elements(By.TAG_NAME,"td")[0]
		player_name = player_attributes.find_element(By.CLASS_NAME,"table-address-vendorname").text
		player_email_address = player_attributes.find_elements(By.TAG_NAME,"div")[-1].text

		player_attributes = [player_name, player_email_address]
		all_players.append(player_attributes)

	return all_players











# [1] Sources
planetbids_sites_csv = "https://storage.googleapis.com/wesonder_databases/Planetbids/absolute_planetbids_sites.csv"
df = pd.read_csv(planetbids_sites_csv)


# [2] Sources
data_delivery_location_pb_urls = "/Users/damiamalfaro/Downloads/pb_prospective_bidders_sites.csv"
df_testing = pd.read_csv(data_delivery_location_pb_urls)


# Data delivery location
data_delivery_location_pb_data = "/Users/damiamalfaro/Downloads/pb_prospective_bidders_attributes.csv"


'''
[1]: Acquire Indidiual href values for all bids for all PB sites.
'''
for index, row in df.iloc[:].iterrows():

	if index % 5 == 0:
		time.sleep(30)

	prospective_bidders_url, awarding_body, single_pb_url = acquiring_bid_links(row["WebLink"])
	awarding_body_list = []
	awarding_body_list.extend([awarding_body] * len(prospective_bidders_url))
	pb_links = []
	pb_links.extend([single_pb_url] * len(prospective_bidders_url))

	resulting_df = pd.DataFrame({
		'AwardingBody':awarding_body_list,
		'ProspectiveBiddersURL':prospective_bidders_url,
		'RespectivePBURL':pb_links
		})

	resulting_df.to_csv(data_delivery_location_pb_urls, mode="a",index=False)

	total_percentage = round(((index / len(df)) * 100), 2)
	print(f"Bid Site {index} Completed - {total_percentage}%\n")



'''
# [2]: Acquire the respective data from each Prospective Bidder
'''
for index, row in df_testing.iloc[:].iterrows():

	if index % 5 == 0:
		time.sleep(30)

	try:
		pb_attributes = data_expropriation(row["ProspectiveBiddersURL"])
		all_pb_attributes = []
		all_pb_attributes.extend(pb_attributes)
		df_data = pd.DataFrame(all_pb_attributes)
		df_data.to_csv(data_delivery_location_pb_data, mode="a", index=False, header=False)


	except Exception as exe:
		print(exe)
		sys.exit(1)













'''
Time Statistics
'''
end_time = time.time()
elapsed_time = end_time - start_time
elapsed_hours = round((elapsed_time / 60 / 60), 3)
print(f'Total Hours to Execute: {elapsed_hours}')
import sys
import pandas as pd
import os
import re
import numpy as np
from pandas.errors import EmptyDataError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


# Entering and Web Scraping the DIR Website
def dir_extraction(url_number,positional_awareness_storage):
	# Designate correct URL
	dir_url = f"https://services.dir.ca.gov/gsp?id=dir_contractors&table=x_cdoi2_csm_portal_customer_account_lookup&view=public&sysparm_fixed_query=type%3D2&filter=&spa=1&p={url_number}&o=pwcr&d=asc"


	# Begin the opening with Selenium
	driver = webdriver.Chrome()
	driver.get(dir_url)
	intial_url = driver.current_url
	print(intial_url)
	time.sleep(10)

	# Assuring your position within "Contractors"
	title_of_interface = WebDriverWait(driver,10).until(
		EC.presence_of_element_located((By.CLASS_NAME,"panel-title"))
	)

	# Finding the target within the tabulation display; checkpoint 1
	tabulation_of_entities = driver.find_element(By.CLASS_NAME,"panel-body")

	# Checkpoint 2; <tbody> tag (where all <tr> are found)
	trbody_tag = tabulation_of_entities.find_element(By.TAG_NAME,"tbody")

	# Total Entities tabulated per webpage (used in the future to iterate through each)
	entity_targets = trbody_tag.find_elements(By.TAG_NAME,"tr") # Shall be 20 as 20 is the amount of contractors showed per page

	# Entity Attributes
	entity_attributes = []

	'''
	Watershed 1: Entity collection of display webpage
	'''
	try:
		# Positional awareness variable
		positional_awareness = 1

		# Iterate through each of the 20 available Entities per webpage display
		for entity in range(1,len(entity_targets)+1):

			# List with all the attributes below (always maintain organization)
			entity_collected_attributes = []

			# The index position of each attribute (based on the available 20 display)
			entity_xpath = f'//tbody/tr[{entity}]'

			# The clickable index position and action
			entity_located = WebDriverWait(driver,2).until(
				EC.element_to_be_clickable((By.XPATH,entity_xpath))
			)
			entity_located.click()
			time.sleep(1)

			# Iterate through each of the extractable attributes of the entity, which are listed below
			entity_extractable_attributes = [
			'sp_formfield_name',
			's2id_sp_formfield_type',
			'sp_formfield_email',
			'sp_formfield_website_link',
			'sp_formfield_address_1',
			'sp_formfield_address_2',
			'sp_formfield_city',
			'sp_formfield_state',
			'sp_formfield_zip',
			'sp_formfield_cslb',
			'sp_formfield_legal_name',
			'sp_formfield_business_phone',
			'sp_formfield_identification_number',
			'sp_formfield_president',
			'sp_formfield_pwcr',
			'sp_formfield_registration_start_date',
			'sp_formfield_registration_end_date',
			'sp_formfield_doing_business_as',
			]

			# Once immersed within the entity, extract the aforementioned attributes
			for entity_extractable_attribute in entity_extractable_attributes:

				# This looks odd but somehow the 's2id_sp_formfield_type' attribute is not extractable by .text functionality
				if entity_extractable_attribute == 's2id_sp_formfield_type':
					entity_attribute_v2 = driver.find_element(By.ID,entity_extractable_attribute)
					entity_attribute_text_v2 = entity_attribute_v2.text
					entity_collected_attributes.append(entity_attribute_text_v2)

				# The rest are though
				else:
					entity_attribute = driver.find_element(By.ID,entity_extractable_attribute)
					entity_attribute_text = entity_attribute.get_attribute('value')
					entity_collected_attributes.append(entity_attribute_text)

			# Check it worked by printing the attributes
			print(entity_collected_attributes)

			# Append the attributes to a bigger list
			entity_attributes.append(entity_collected_attributes)			

			# Go back and repeat with the next entity
			print(f'Current Iteration: {positional_awareness}')

			# Pinpoint the current position of the entity in proportion to the Storage Unit
			storage_unit_positional_awareness = (positional_awareness_storage * 20) - 20
			print(f'Current Data Base Position: {storage_unit_positional_awareness+positional_awareness}')

			positional_awareness += 1
			driver.back()
			time.sleep(1)

		'''
		Watershed 2: Allocation into CSV file
		'''
		try:
			df_allocation = pd.DataFrame(entity_attributes)
			df_allocation.to_csv(csv_file,mode='a',header=False,index=False)

		except Exception as exe_w2:
			print("\nBroken: Watershed 2\n")
			print(exe_w2)


		# Finish the extraction
		driver.quit()


	except Exception as exe_w1:
		print("\nBroken: Watershed 1\n")
		print(exe_w1)












if __name__ == '__main__':
	'''
	Watershed 3: Transitioning between Pages (20 entities per page), a total of 113900 entities available
	'''
	try:
		# Storage Unit
		csv_file = 'dir_entities.csv'
		df = pd.read_csv(csv_file)
		number_of_rows_used = df.shape[0]

		# Our given assets
		webpage_position = (int(number_of_rows_used) // 20) + 1

	except Exception as exe_w3:
		print("\nBroken: Watershed 3")
		print(exe_w3)

	# Last position 2 (this means in the second .click() of the Next Buttom, or 21-40)
	webpage_position_index = webpage_position
	while webpage_position_index != 5695:
		dir_extraction(webpage_position_index,webpage_position_index)
		csv_file_v2 = 'dir_entities.csv'
		df_v2 = pd.read_csv(csv_file)
		number_of_rows_used_v2 = df_v2.shape[0]
		webpage_position_index = (int(number_of_rows_used_v2) // 20) + 1











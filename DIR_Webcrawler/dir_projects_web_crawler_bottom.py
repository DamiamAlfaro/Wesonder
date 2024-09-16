import sys
import pandas as pd
import os
import re
import csv
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
def dir_project_extraction(positional_awareness_storage):
	# Designate correct URL
	dir_url = f"https://services.dir.ca.gov/gsp?id=dir_projects&table=x_cdoi2_csm_portal_project&spa=1&filter=&p={positional_awareness_storage}&o=description&d=asc"


	# Begin the opening with Selenium
	driver = webdriver.Chrome()
	driver.get(dir_url)
	intial_url = driver.current_url
	print(f"BOTTOM: {positional_awareness_storage}")
	time.sleep(4)

	# Assuring your position within "Contractors"
	title_of_interface = WebDriverWait(driver,10).until(
		EC.presence_of_element_located((By.CLASS_NAME,"panel-title.ng-binding"))
	)

	# Finding the target within the tabulation display; checkpoint 1
	tabulation_of_entities = driver.find_element(By.CLASS_NAME,"panel-body")

	# Checkpoint 2; <tbody> tag (where all <tr> are found)
	trbody_tag = tabulation_of_entities.find_element(By.TAG_NAME,"tbody")

	# Total Entities tabulated per webpage (used in the future to iterate through each)
	entity_targets = trbody_tag.find_elements(By.TAG_NAME,"tr") # Shall be 20 as 20 is the amount of contractors showed per page
	number_of_projects_showing = len(entity_targets)

	# Entity Attributes
	entity_attributes = []

	'''
	Watershed 1: Entity collection of display webpage
	'''
	try:
		# Positional awareness variable
		positional_awareness = 1

		# Iterate through each of the 20 available Entities per webpage display y=
		for entity in range(1,len(entity_targets)+1):

			# List with all the attributes below (always maintain organization)
			entity_collected_attributes = []

			# The index position of each attribute (based on the available 20 display)
			entity_xpath = f'//tbody/tr[{entity}]'

			# The clickable index position and action
			entity_located = WebDriverWait(driver,4).until(
				EC.element_to_be_clickable((By.XPATH,entity_xpath))
			)
			driver.execute_script("arguments[0].scrollIntoView();", entity_located)
			entity_located.click()
			time.sleep(2)

			# Iterate through each of the extractable attributes of the entity, which are listed below
			entity_extractable_attributes = [
			'sp_formfield_number',
			'sp_formfield_name',
			's2id_sp_formfield_awarding_body',
			'sp_formfield_contract_number',
			's2id_sp_formfield_type',
			's2id_sp_formfield_operate_lcp',
			's2id_sp_formfield_state',
			's2id_sp_formfield_stage',
			'sp_formfield_project_id',
			'sp_formfield_project_number',
			's2id_sp_formfield_associated_pla',
			'sp_formfield_job_site_address',
			'sp_formfield_sys_updated_on',
			'sp_formfield_sys_updated_by',
			'sp_formfield_sys_mod_count',
			'sp_formfield_description',
			'sp_formfield_estimated_end_date',
			'sp_formfield_estimated_start_date',
			'sp_formfield_contract_date',
			'sp_formfield_first_advertised_bid_date',
			'sp_formfield_start_date',
			'sp_formfield_end_date',
			'sp_formfield_award_date',
			'sp_formfield_street',
			'sp_formfield_street_2',
			'sp_formfield_city',
			'sp_formfield_address_state',
			'sp_formfield_total_cost',
			'sp_formfield_amount'
			]

			# Once immersed within the entity, extract the aforementioned attributes
			for entity_extractable_attribute in entity_extractable_attributes:

				# We fragmentize each of the extracatable attributes from the list in order to identify which rule applies to it
				keys_identifications = entity_extractable_attribute.split("_")

				# This looks odd but somehow the 's2id_sp_formfield_type' attribute is not extractable by .text functionality
				if keys_identifications[0] == 's2id':
					entity_attribute_v2 = driver.find_element(By.ID,entity_extractable_attribute)
					entity_attribute_text_v2 = entity_attribute_v2.text
					if "\n" in entity_attribute_text_v2:
						entity_collected_attributes.append("None")
					else:
						entity_collected_attributes.append(entity_attribute_text_v2)

				# The rest are though
				elif keys_identifications[0] == "sp":
					entity_attribute = driver.find_element(By.ID,entity_extractable_attribute)
					entity_attribute_text = entity_attribute.get_attribute('value')
					entity_collected_attributes.append(entity_attribute_text)


				else:
					continue
			

			# Check if everything is alright
			print(entity_collected_attributes)
			print(f'Data Frame Length {len(entity_collected_attributes)}')

			# Go back and repeat with the next entity
			print(f'Current Iteration: {positional_awareness}')

			# Pinpoint the current position of the entity in proportion to the Storage Unit
			storage_unit_positional_awareness = (positional_awareness_storage * 20) - 20
			print(f'Current Data Base Position: {storage_unit_positional_awareness+positional_awareness}')

			positional_awareness += 1

			# Append the attributes to a bigger list
			entity_attributes.append(entity_collected_attributes)

			# Continue iteration
			driver.back()
			time.sleep(1)


	except Exception as exe_w1:
		print("\nBroken: Watershed 1\n")
		print(exe_w1)


	# Finish the extraction
	driver.quit()
	return entity_attributes






if __name__ == '__main__':

	# Location of storage and math associated with it
	csv_file = 'dir_projects_bottom.csv'
	initial_tabulation = pd.read_csv(csv_file,low_memory=False)
	positional_location = 11084  

	while positional_location != 12500:

		# A list containing the 20 <tr> elements from a single page instance
		extraction = dir_project_extraction(positional_location) 
		df_acquired = pd.DataFrame(extraction)
		if len(df_acquired) > 10:
			df_acquired.to_csv(csv_file,index=False,header=False,mode='a')
			positional_location += 1
			print(f"Current Page {positional_location}")
		else:
			pass



	


	



















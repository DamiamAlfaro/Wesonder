import sys
import pandas as pd
import os
import re
import glob
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


'''
This is our first step: to update the CSLB publicly available database
in order to depart the series of actions from it. Why? Because CSLB 
stands for Contractor State License Board, which includes all certified
entites possessing a license in the State of California.
'''
def updating_cslb_subcontractors():
    cslb_download_webpage = "https://www.cslb.ca.gov/onlineservices/Dataportal/ListByClassification"
    driver = webdriver.Chrome()
    driver.get(cslb_download_webpage)
    time.sleep(4)
    
    # Now enter the section where you can download the Excel tabulations including the subcontractors
    drag_down_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME,"button"))
    )
    
    # Click the Drag Down Menu
    drag_down_button.click()
    
    # Pinpoint the options of the Drag Down Menu just clicked, we can do so by locating the <ul> element
    list_of_options_list_element = WebDriverWait(driver,10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME,"ul"))
    )
    
    
    # Print all of the options within the Drag Down Menu
    list_of_options = list_of_options_list_element[2].find_elements(By.TAG_NAME,"li")
    total_options_count = len(list_of_options)
    print(f"Total Licences = {total_options_count}")

    # Iterate through each license type and download each type singularly
    for license_tabulation in range(1,total_options_count+1):

        # Pinpoint the license name
        label_license = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//label[@for='ms-opt-{license_tabulation}']"))
        )
        print(label_license.text)

        # Remove the fallible one
        if label_license.text == "C-61 - Limited Specialty Classification":
            pass

        # Continue with the non-fallible
        else:
            
            # Click the Checkbox
            checkbox_license = WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.ID,f"ms-opt-{license_tabulation}"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", checkbox_license)
            checkbox_license.click()
    
            # Download button
            download_button = WebDriverWait(driver,10).until(
                EC.element_to_be_clickable((By.NAME,"ctl00$MainContent$btnSearch"))
            )

            # Donwload license sub
            download_button.click()
    		
            # Click on drag down menu
            drag_down_button.click()
    
    		# Unclick checkbox
            checkbox_license.click()
    
    		# Let it breath a little bit
            driver.implicitly_wait(4)

        # Visual separator
        print("--------")


'''
Here we are just combining the newly downloaded Excel files and removing any
duplicated subcontractor/contractor in order to make things cleaner.
'''
def clearing_newly_downloaded_cslb_subs():

	# We downloaded the Excel files into the Download folder, so we just need to access it
	downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
	for file_name in os.listdir(downloads_folder):
		print(file_name)

	# Specify the types of files you need
	file_list = glob.glob(os.path.join(downloads_folder,"*.xlsx"))

	# Where all files will be allocated
	excel_list = []

	# Iterate through the file list
	for filing_out in file_list:
	    excel_list.append(pd.read_excel(filing_out))

	# Put the files together
	excel_merged = pd.concat(excel_list,ignore_index=True)

	excel_merged_no_duplicates = excel_merged.drop_duplicates()

	# Transcribe all of them into a single excel. The result will be on the Desktop
	excel_merged_no_duplicates.to_excel("all_subcontractors.xlsx",index=False)

	# Turn the newly downloaded Excel file into a csv file
	newly_excel_cslb_file = "all_subcontractors.xlsx"
	df_excel = pd.read_excel(newly_excel_file)
	df_excel.to_csv("all_subcontractors.csv",index=False)


'''
This shall be executed once we understand the plans from the Bid in question. What do we
need for this bid?
'''
def subcontractor_categorization(csv_in_question):

	# Read the csv file
	df_cslb = pd.read_csv(csv_in_question)


	# Identify which counties you need
	needed_counties = ["San Diego","Los Angeles","San Bernardino","Orange","Riverside","Imperial"]

	# Identify which licenses you need
	needed_licenses = ["C13|C-13","C21|C-21","C22|C-22","C12|C-12","C8|C-8",
	"C32|C-32","D60|D-60","C45|C-45","C27|C-27","C34|C-34",
	"C10|C-10","C31|C-31"]

	# The new csv file that will include only the specified parameters aforementioned
	filtered_cslb_csv = pd.DataFrame()

	# Iterate to extract the needed subs, first within each county
	for sub_county in needed_counties:

		# Second for each license
		for sub_license in needed_licenses:

			# Iterate with the respective parameters
			filtered_cslb_df = df_cslb[df_cslb.iloc[:,2].str.contains("Corporation") &
			df_cslb.iloc[:,8].str.contains(sub_county) &
			df_cslb.iloc[:,12].str.contains(sub_license)]

			# Update the dataframe
			filtered_cslb_csv = pd.concat([filtered_cslb_csv,filtered_cslb_df])


	# Drop the duplicates from the iteration above
	filtered_cslb_csv.drop_duplicates(inplace=True)

	# Specify the new filetered csv file
	new_csv_fileted_cslb_file = "bid_subcontractors.csv"

	# Allocate it
	filtered_cslb_csv.to_csv(new_csv_fileted_cslb_file,index=False)


def searching_needed_subs(bid_needed_csv_file):

	# Read the csv in question
	df_bid_cslb_subs = pd.read_csv(bid_needed_csv_file)

	# Allocate the names (and other attributes) that will help you find the entitiy in the web
	name_in_question = df_bid_cslb_subs.iloc[:,3][0]
	print(name_in_question)

	# Search it in the web
	driver = webdriver.Chrome()
	driver.get("https://google.co.in/search?q=" + name_in_question)
	driver.implicitly_wait(5)


	








if __name__ == '__main__':
	# Step 1: Update the CSLB license
	#updating_cslb_subcontractors()

	# Step 2: Combine and remove separates in the newly downloaded CSLB subs
	#clearing_newly_downloaded_cslb_subs()

	# Step 3: Decide which subcontractors license and location is needeed for the bid (e.g. Electricians in the San Bernardino County)
	#new_csv_cslb_file = "all_subcontractors.csv"
	#print(subcontractor_categorization(new_csv_cslb_file))

	# Step 4: Search subcontractor in the newly extracted list and search their email on the web
	bid_needed_subs_csv_file = "bid_subcontractors.csv"
	searching_needed_subs(bid_needed_subs_csv_file)














import sys
import pandas as pd
import os
import re
import threading
import glob
import csv
import numpy as np
from queue import Queue
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
            time.sleep(1)

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


'''
Here we will look for the emails and any related information in the data bases we already possess.
'''
def existing_database_search(bid_needed_csv_file):
	pass


'''
This will be the most arduous function so far, in here we will categorize the
Google results and try to look for the email in any of them.
'''
def searching_needed_subs(bid_needed_csv_file):
	# Websites in which the entity can be found
	entity_location_websites = []

	# Emails extracted list after all operations below
	emails_extracted = []

	# Read the csv in question
	df_bid_cslb_subs = pd.read_csv(bid_needed_csv_file)

	# Allocate the names (and other attributes) that will help you find the entitiy in the web
	name_in_question = df_bid_cslb_subs.iloc[:,3][0]
	print(name_in_question)

	# Search it in the web
	driver = webdriver.Chrome()
	driver.get("https://google.co.in/search?q=" + name_in_question)
	driver.implicitly_wait(5)

	'''
	I. The sub has a website and a RHS (Right Hand Side) in the Google search
	'''
	try:
		rhs_found = WebDriverWait(driver,10).until(
			EC.presence_of_element_located((By.ID,"rhs"))
		)

		# If there is, let's check if there is an available website. First let's find the buttons available in the RHS
		try:
			rhs_buttons = driver.find_elements(By.TAG_NAME,"button")
			# If there are, search for the one that says "Website"
			website_button = []
			for rhs_button in rhs_buttons:
				if rhs_button.text == "Website":
					website_button.append(rhs_button)
				else:
					pass

			# Click the button
			website_button[0].click()

			# Now, once in, try to look for the mailto: element that includes an email
			try:
				mailto_element = driver.find_elements(By.XPATH,'//a[contains(@href,"mailto")]')
				for emails in mailto_element:
					emails_extracted.append(emails.text)
			except Exception as exe:
				print("No Email found")
				print(exe)

			# Furthermore, you can look through every tab within the website and look for any "mailto:"" elements
			try:
				# Sometimes the "Home" link is there, so we need to make sure we avoid it since we begin in it
				home_url = driver.current_url

				# First website where the entity could be found, i.e. the first Google search result
				entity_location_websites.append(home_url)

				# First, let's look for any <nav> elements, following by a search of <a href> within them
				nav_elements_in_website = WebDriverWait(driver,10).until(
					EC.presence_of_element_located((By.TAG_NAME,"nav"))
					)

				# For every navigation element, find the link associated within it
				a_elements = nav_elements_in_website.find_elements(By.TAG_NAME,"a")

				# Iterate through each link
				for following_link in range(len(a_elements)):

					# Reposition the <nav> and <a> element since they somehow become different before
					nav_elements_in_website = driver.find_element(By.TAG_NAME, 'nav')
					links = nav_elements_in_website.find_elements(By.TAG_NAME,'a')
					links[following_link].click()

					# If the "Home" is there, we need to skip it
					if driver.current_url == home_url:
						continue

					# If not, extract the "mailto:" email address
					else:
						# Go back
						time.sleep(1)

						# Attempt to find "mailto" addresses
						try:
							mailto_other_element = WebDriverWait(driver,10).until(
								EC.presence_of_all_elements_located((By.XPATH,'//a[contains(@href,"mailto")]'))
								)

							for new_mailto_element in mailto_other_element:
								emails_extracted.append(new_mailto_element.text)
						except:
							print("No Email found")


						driver.back()
						time.sleep(1)

				# Go back to the Google Search result
				driver.back()

				# Let it breathe mate
				time.sleep(3)


			except Exception as exe:
				print("No <nav> elements")
				print(exe)

		except Exception as exe:
			print("No RHS Buttons.")
			print(exe)


	except Exception as exe:
		print(exe)
		print("No RHS side.")

	'''
	II. The sub has a website and but doesn't have a RHS (Right Hand Side) in the Google search.
	Or perhaps it does include a RHS, but we still want to iterate through other websites to increase
	the likelyhood of finding email addresses and additional information.
	
	Look, I know we want to build for each website, but it is too diverse, and what's worse: not all
	websites have an available "mailto:", I'd say that we need to enter the top 10 websites on the
	Google search, search for "mailto:", and extract it. If the email does not belong to the respective 
	subcontractor, we can still do a DIR and Planetbids (both, results and prospective bidders).
	'''
	try:
		# The first step is to get the top 8 websites that appear in the Google search, first locate the element containing all links
		google_results = WebDriverWait(driver,10).until(
			EC.presence_of_element_located((By.ID,"search")))

		# Acquire the elements containing the links
		google_results_links = google_results.find_elements(By.TAG_NAME,"a")

		# Extract the actual urls from the links
		individual_links = [individual_link.get_attribute("href") for individual_link in google_results_links]

		# Before proceeding with entering every single Google search website, let's remove the first website we entered above from the list
		for website in individual_links:

			# Adding websites
			if entity_location_websites[0] not in website:
				entity_location_websites.append(website)

			# Removing the already visited website
			else:
				pass

		# Remove any duplicates that might've appeared
		entity_location_websites = list(set(entity_location_websites))

		# Where all the threads will be located
		linking_threads = []

		# Now, let's build something to iterate through each newly acquired website, while skipping the one we already visited
		try:

			# Allocate the Queue
			result_queue = Queue()

			# Iterate through each website from the Google search results and extract the "mailto:" element using multithrearding()
			for url_attempt in entity_location_websites:

				# Apply the multithrearding() function
				thread = threading.Thread(target=multithrearding,args=(url_attempt,result_queue))
				linking_threads.append(thread)
				thread.start()

			# Iterate
			for thread_link in linking_threads:
				thread_link.join()

			# Usable item
			resultings = []

			# Put the results into the usable list
			while not result_queue.empty():
				resultings.append(result_queue.get())

			# Extract the emails newly acquired from multithrearding()
			for email_acquired in resultings:
				if email_acquired[1][0] == "No Emails":
					pass
				else:
					emails_extracted.append(email_acquired[1][0])

			# Remove duplicates again
			emails_extracted = list(set(emails_extracted))

			# Remove debris
			emails_extracted = [item for item in emails_extracted if item]


		# Something happened
		except Exception as exe:
			print("UNEXPECTED")
			print(exe)

	except Exception as exe:
		print("No Website nor RHS")
		print(exe)


	# Returns a list of emails without duplicates
	return list(set(emails_extracted))




	








if __name__ == '__main__':
	# Function for multithreading
	def multithrearding(url,result_queue):		

		try:
			# Emails extracted
			new_emails_extracted = []

			# Open each webdriver session
			driver_1 = webdriver.Chrome()
			driver_1.get(url)


			# Create a function that takes the email (i.e. "mailto:" element) from the website specified in the url
			try:
				if "www.facebook.com/" in url:
					# Pinpoint the close button
					close_button = WebDriverWait(driver_1,10).until(
						EC.presence_of_element_located((By.XPATH, '//*[@aria-label="Close"]'))
						)

					# Close the Sign In Meny
					close_button.click()

					# Pinpoint the Intro Header from the Facebook page
					facebook_intro_list = driver_1.find_elements(By.TAG_NAME,"ul")

					# Split the text of the intro
					facebook_email_possible_location = facebook_intro_list[0].text.split("\n")

					# Search for the email item from the splited text
					for possible_email in facebook_email_possible_location:
						# Identify the first 'www' and the last 'com'
						if possible_email[:3].lower() != "www" and possible_email[-3:].lower() == "com":
							new_emails_extracted.append(possible_email)
						else:
							continue
					print(new_emails_extracted)
					result_queue.put([url,new_emails_extracted])


				else:
					# Pinpoint the element we are looking for
					mailto_new_element = WebDriverWait(driver_1,10).until(
						EC.presence_of_all_elements_located((By.XPATH,'//a[contains(@href,"mailto")]'))
						)

					# Acquire the emails from the "mailto:" element
					for new_email in mailto_new_element:
						new_emails_extracted.append(new_email.text)

					# Return the result
					print(new_emails_extracted)
					result_queue.put([url,new_emails_extracted])

			# No emails found in the Google Search link
			except TimeoutException:
				result_queue.put([url,["No Emails"]])

		# The result is still a list
		except Exception as exe:
			result_queue.put([url,[str(exe)]])

		# Exit the Google instance
		finally:
			driver_1.quit()


	# Step 1: Update the CSLB license
	#updating_cslb_subcontractors()

	# Step 2: Combine and remove separates in the newly downloaded CSLB subs
	#clearing_newly_downloaded_cslb_subs()

	# Step 3: Decide which subcontractors license and location is needeed for the bid (e.g. Electricians in the San Bernardino County)
	#new_csv_cslb_file = "all_subcontractors.csv"
	#print(subcontractor_categorization(new_csv_cslb_file))

	# Step 4: Check if the subcontractors are in the existing DIR and DVE data bases
	#existing_database_search()

	# Step 5: Search subcontractor in the newly extracted list and search their email on the web
	bid_needed_subs_csv_file = "bid_subcontractors.csv"
	print(searching_needed_subs(bid_needed_subs_csv_file))














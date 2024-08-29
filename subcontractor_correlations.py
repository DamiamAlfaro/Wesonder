import sys
import pandas as pd
import os
import re
import threading
import glob
import csv
import numpy as np
from queue import Queue
from itertools import permutations, combinations
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
We will utilize this function several times in order to look for the specified array of values
within the DIR Database. The reason why we are making it a function is because it is being utilized more
than once in the same functionality instance.
'''
def existing_database_search_dir_iteration(array_of_values,df_dir_tabulation): # The input is a list of company names

	# Index list containing all indexes where the subs can be found
	index_list_subs_needed = []

	# Names found
	sub_names_found = []

	# Iterate through the list of subs that we need
	for subcontractor_in_question in array_of_values:

		# Iterate through the DIR database to find the subs we need
		for possible_subcontractor_instance in df_dir_tabulation["EntityName"]:

			# If the sub we need is found, extract the index to print further information
			if subcontractor_in_question in possible_subcontractor_instance:

				# Retrieve the index
				sub_name_index = df_dir_tabulation.index[df_dir_tabulation["EntityName"].str.contains(subcontractor_in_question)].tolist()
				for index_in_question in sub_name_index:
					index_list_subs_needed.append(index_in_question) # Might be multiple indexes

					# Allocate the newly found sub name to the sub names found list for further analysis
					if subcontractor_in_question not in sub_names_found:
						sub_names_found.append(subcontractor_in_question)

	# Subs not found
	subs_not_found = [sub for sub in array_of_values if sub not in sub_names_found]

	# Returns an Array of indexes fo subscontractors, the subcontractors found (their index in the first return value), and the subs not found
	return index_list_subs_needed, sub_names_found, subs_not_found



'''
Here we will look for the emails and any related information in the data bases we already possess.
'''
def existing_database_search(bid_needed_csv_file,dir_database):
	# Define the Bid Needed Subs DataFrame
	df_dir_correlation = pd.read_csv(bid_needed_csv_file)

	# Define the DIR Tabulation database
	df_dir_tabulation = pd.read_csv(dir_database)

	# Convert the names column's values into Uppercase letters
	df_dir_tabulation["EntityName"] = df_dir_tabulation["EntityName"].str.upper()

	# Convert the names column's values into strings
	df_dir_tabulation["EntityName"] = df_dir_tabulation["EntityName"].astype(str)

	# Acquire the first four subs from the needed sub list for the bid in question
	testing_subs_needed = df_dir_correlation["BusinessName"][:6]

	search_dir_result_1 = existing_database_search_dir_iteration(testing_subs_needed,df_dir_tabulation)

	index_list_subs_needed = search_dir_result_1[0] # Row indexes of subs found

	sub_names_found = search_dir_result_1[1] # Subs found

	subs_not_found = search_dir_result_1[2] # Subs not found

	# See which of the names were not found
	print(f"Search 1 Found: {len(sub_names_found)} {sub_names_found}") # What has to be searched in google if not found in the second

	# Subs not found
	print(f"Search 1 Not Found: {len(subs_not_found)} {subs_not_found}")

	# Undesired company words: avoid duplicating searches with these words
	undesired_company_words = ["CO","CORPORATION", "INC", "INCORPORATED", "LLC", 
	"COMPANY", "MANUFACTURE", "LTD", "MFG", "ASSOCIATES", "ASSOC", "CORP"]

	# Names not found First Word
	sub_names_not_found_first_word = []

	# Now that we know which were not found, we need to build the combination iteration
	sub_names_splited = []

	# Iterate through each not-found name and split it
	for sub_notfound_name in subs_not_found:
		spliting_name = sub_notfound_name.split(" ")
		sub_names_splited.append(spliting_name)
		sub_names_not_found_first_word.append(spliting_name[0])

	# List of lists of permutations, i.e. the number of permutations per each of the Not Found 1
	permutations_inquiry = []

	# A list of all possible individual sub name permutations
	possible_subs_name_permutations = []

	# Iterate through each splited name and pinpoint the possible permutations
	for sub_splited_name in sub_names_splited:
		sub_name_permutation = combinations(sub_splited_name,2) # two word combinations

		# List of permutations for further list
		list_of_permutations = []

		# Extract the individual permutation
		for permutation in sub_name_permutation:

			# Unwanted words? "False" so far...
			unwanted_words_status = False

			# Check each individual words
			for permutation_word in permutation:

				# Determine if the permutation contains unwanted words
				if permutation_word in undesired_company_words:

					# Flip the switch
					unwanted_words_status = True
				else:
					continue

			# If the permutation does not contains unwanted, append it to desired list
			if unwanted_words_status == False:

				# Convert the set into a list
				new_search_combination = list(permutation)

				# Convert the list into a joined string separated by a space
				new_search_word = " ".join(new_search_combination)

				# Append the newly string into the desired list
				possible_subs_name_permutations.append(new_search_word)
				list_of_permutations.append(new_search_word)

			# Continue basically
			else:
				pass

		permutations_inquiry.append(list_of_permutations)

	# The list of names that have to be searched in google; desired output
	subs_not_found_search_need = []

	# We will use this to refence the original name if search is needed for it
	#subs_not_found_index = [index for index in range(len(subs_not_found))]

	# Reference only
	list_of_traitors = []

	for permutations_list,original_first_word in zip(permutations_inquiry,sub_names_not_found_first_word):

		traitor_identified = []
		
		for permutation_in_question in permutations_list:

			if original_first_word in permutation_in_question:
				pass
			else:
				index_of_no_name = permutations_list.index(permutation_in_question)
				permutation_no_name = permutation_in_question
				traitor_identified.append(permutation_no_name)
				traitor_identified.append(index_of_no_name)

		list_of_traitors.append(traitor_identified)

	#print(subs_not_found_index)
	for not_found_1_index, permutation_set in enumerate(permutations_inquiry):
		print("----------------")
		print(f"{not_found_1_index}: {permutation_set}")

	print("----------------")
	print(f"Not searchable: {list_of_traitors}")
	print("----------------")
	print(f"Original First words: {sub_names_not_found_first_word}")
	print("----------------")
	print(f"Round 2 Search: {possible_subs_name_permutations}")
	print("----------------")
	print(f"Desired output: {subs_not_found_search_need}")
	print("----------------")



	# Apply the searching function again with the new names to be searched
	search_dir_result_2 = existing_database_search_dir_iteration(possible_subs_name_permutations,df_dir_tabulation)

	# Second search: Array of indexes
	index_list_subs_needed_2 = search_dir_result_2[0]

	# Second search: Subs found 
	sub_names_found_2 = search_dir_result_2[1]
	print(f"Search 2 Found: {len(sub_names_found_2)} {sub_names_found_2}")

	# Second search: Subs not found
	subs_not_found_2 = search_dir_result_2[2]
	print("----------------")
	print(f"Search 2 Not Found: {len(subs_not_found_2)} {subs_not_found_2}")
	print("----------------")

	# Appending the new indexes to the existing index lists
	for index_2 in index_list_subs_needed_2:
		index_list_subs_needed.append(index_2)


	# Remove duplicates from the index list
	index_list_subs_needed = list(set(index_list_subs_needed))

	# The new output containing the subcontractors' name with their email
	sub_information_output = pd.DataFrame()

	# Lists for the new data frame
	sub_names = []
	sub_emails = []

	# Allocate parameters into a list for future dataframe
	for index in index_list_subs_needed:
		sub_names.append(df_dir_tabulation.iloc[:,0][index]) # Name
		sub_emails.append(df_dir_tabulation.iloc[:,2][index]) # Email

	# Append the list and make them the columns of the new dataframe
	sub_information_output["SubNames"] = sub_names
	sub_information_output["SubEmails"] = sub_emails

	# Drop any duplicates
	sub_information_output.drop_duplicates(inplace=True)

	return sub_information_output, subs_not_found_search_need


'''
This function is needed for multithreading (use multiple webdriver instance
at once) in the function below.
'''
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


'''
A function to iterate through every <a> in the <nav> of a website
'''
def a_tags_in_nav_tags(url_in_question,output_queue):

	# Extracted emails
	extracted_emails_a_tag_nav = []

	# Enter the Chrome window
	driver_2 = webdriver.Chrome()
	driver_2.get(url_in_question)

	try:
		mailto_element_nav = driver_2.find_elements(By.XPATH,'//a[contains(@href,"mailto")]')
		for email_nav in mailto_element_nav:
			extracted_emails_a_tag_nav.append(email_nav.text)
	except:
		print("No Emails")

	output_queue.put(extracted_emails_a_tag_nav)


'''
This will be the most arduous function so far, in here we will categorize the
Google results and try to look for the email in any of them.
'''
def searching_needed_subs(list_with_remaining_sub_names):
	# Websites in which the entity can be found
	entity_location_websites = []

	# Emails extracted list after all operations below
	emails_extracted = []

	# Allocate the names (and other attributes) that will help you find the entitiy in the web
	for remaining_name in list_with_remaining_sub_names:
		print(remaining_name)

		# Search it in the web
		driver = webdriver.Chrome()
		driver.get("https://google.co.in/search?q=" + remaining_name)
		time.sleep(4)

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

				# Sometimes the "Home" link is there, so we need to make sure we avoid it since we begin in it
				home_url = driver.current_url

				# First website where the entity could be found, i.e. the first Google search result
				entity_location_websites.append(home_url)

				# List of actual url links
				href_attribute_acquired = []

				# Furthermore, you can look through every tab of the navigation bar (a standard in websites) within the website and look for any "mailto:"
				try:
					# First, let's look for any <nav> tag, following by a search of <a href> within them
					nav_elements_in_website = driver.find_element(By.TAG_NAME,"nav") # list, need the first element of it always (top most nav)

					# For every navigation tag, find the link associated within it
					a_tags_nav = nav_elements_in_website.find_elements(By.TAG_NAME,"a")

					# Only get the ones that contain text because they are usually the valid links
					for a_tag_nav in a_tags_nav:
						if len(a_tag_nav.text) > 0:
							href_attribute = a_tag_nav.get_attribute("href")
							href_attribute_acquired.append(href_attribute)

				except Exception as exe:
					print("No <nav> tags")
					#print(exe)

				# Do the same but for the <footer>, find all <a> tags in it and the "mailto:" within them
				try:
					# Let's pinpoint the footer
					footer_tag_element = driver.find_element(By.TAG_NAME,"footer")

					# Find the <a> within <footer>
					a_tags_footer = footer_tag_element.find_elements(By.TAG_NAME,"a")

					# Append the 'href' attributes to the href list
					for a_tag_footer in a_tags_footer:
						if len(a_tag_footer.text) > 0:
							href_attribute_footer = a_tag_footer.get_attribute("href")
							href_attribute_acquired.append(href_attribute_footer)

				except Exception as exe:
					print("No <footer>")
					#print(exe)

				try:
					# Iterate through the new list of links
					thread_list = list()

					# Allocate the Queue
					output_queue = Queue()

					# Multithreading <nav> hrefs instance
					for href_element in range(len(href_attribute_acquired)):
						t = threading.Thread(name="Executing: {}".format(href_attribute_acquired[href_element]),
							target=a_tags_in_nav_tags,args=(href_attribute_acquired[href_element],output_queue))
						t.start()
						time.sleep(1)
						thread_list.append(t)

					for thread in thread_list:
						thread.join()

					while not output_queue.empty():
						emails_extracted.extend(output_queue.get())


				except Exception as exe:
					print("No <nav> multithrearding")
					print(exe)

				driver.back()


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

			print(driver.current_url)
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

	'''
	Step 1: Update the CSLB license
	'''
	#updating_cslb_subcontractors()

	'''
	Step 2: Combine and remove separates in the newly downloaded CSLB subs
	'''
	#clearing_newly_downloaded_cslb_subs()

	'''
	Step 3: Decide which subcontractors license and location is needeed for the bid (e.g. Electricians in the San Bernardino County)
	'''
	#new_csv_cslb_file = "all_subcontractors.csv"
	#print(subcontractor_categorization(new_csv_cslb_file))

	'''
	Step 4: Check if the subcontractors are in the existing DIR and DVE data bases.
	'''

	dir_database_file = "/Users/damiamalfaro/Desktop/testing_wesonder/Database_connections/dir_entities.csv"
	bid_needed_subs_csv_file = "/Users/damiamalfaro/Desktop/testing_wesonder/Database_connections/bid_subcontractors.csv"
	dir_search_results = existing_database_search(bid_needed_subs_csv_file,dir_database_file)

	# # The extracted data frame (intended to be allocated in a new excel)
	dataframe_with_results = dir_search_results[0]
	print(dataframe_with_results)

	# # Need to search for the following remaining subs
	subs_still_needed = dir_search_results[1] # Apply google search

	'''
	Step 5: Search subcontractor from the newly extracted list and search their email on the web.
	'''

	# Transcribed from the result of existing_database_search()
	#subs_to_be_searched_in_google = subs_still_needed
	#print(len(subs_to_be_searched_in_google))

	# Search for the remaining names
	# testing_list = ["CACY ELECTRIC","RAMONA METAL WORKS"]
	# print(searching_needed_subs(testing_list)) # Input: list()

	'''
	Step 6: Connect the google function the DIR data base does not contain the word we are looking for.
	'''














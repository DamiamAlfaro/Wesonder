import sys
import pandas as pd
import os
import re
import threading
import traceback
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
from string import ascii_letters, digits
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
	df_excel = pd.read_excel(newly_excel_cslb_file)
	df_excel.to_csv("all_subcontractors.csv",index=False)


'''
This shall be executed once we understand the plans from the Bid in question. What do we
need for this bid?
'''
def subcontractor_categorization(csv_in_question, counties, licences):

	# Read the csv file
	df_cslb = pd.read_csv(csv_in_question)


	# Identify which counties you need
	needed_counties = counties

	# Identify which licenses you need
	needed_licenses = licences

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

	return needed_counties, needed_licenses


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
Classifying permutations and outputing the ones including the first word of the company. For further explanation check the 
WeSonder notes [September 1, 2024, a]
'''
def first_word_appearance_only(permutations_for_each_name,first_word_of_the_names):

	# Iterating through the permutations and extracting the ones with the first word
	for permutation_set, first_word in zip(permutations_for_each_name,first_word_of_the_names):
		for permutation_pair in permutation_set:
			if first_word not in permutation_pair:
				permutation_set.remove(permutation_pair)


	# Return the permutations that will be searched on that include the first word
	return permutations_for_each_name # list of permutations


'''
Modifying resulting permutations from the function above that have a single-character as part of their name. 
For further explanation check WeSonder notes [September 1, 2024, a]
'''
def single_character_permutation_refinement(original_permutations_set,first_two_words_list):

	# Permutation_individual_set: a list of permutations -> ["WORD AND WORD2","WORD AND WORD2"]
	for permutation_individual_set in original_permutations_set:

		# Identify the index of the current permutation_individual_set
		current_permutation_individual_set_index = original_permutations_set.index(permutation_individual_set)

		# New two-character words needed for substitution below
		two_character_first_word = first_two_words_list[current_permutation_individual_set_index]


		# permutation_words: the string words within the permutation list -> "WORD AND WORD2"
		for permutation_words in permutation_individual_set:

			# Needed for substitution
			permutation_words_index = permutation_individual_set.index(permutation_words)

			# We actually want to look for the first two words by themselves -> "SINGLE_WORD SECOND_SINGLE_WORD"
			if permutation_words == two_character_first_word:
				pass

			# Substitution
			else:
				# permutation_words_list -> ["SINGLE_WORD","SECOND_SINGLE_WORD"]
				permutation_words_list = permutation_words.split(" ")

				# "SECOND_SINGLE_WORD" needed for substition with two_character_first_word
				second_word_for_substitution = permutation_words_list[1]

				permutation_individual_set[permutation_words_index] = f"{two_character_first_word} {second_word_for_substitution}"

	# Remove any duplicates that might've generated
	original_permutations_set = [list(set(single_set)) for single_set in original_permutations_set]

	# Single list containing all permutations in a single-layer list
	single_layer_permutations = [j for i in original_permutations_set for j in i]

	return original_permutations_set, single_layer_permutations


'''
Identify which are the subs that were not found and get their original (from the first array of values)
names in order to search for them in google.
'''
def subs_not_found_now_search(subs_not_found_list_2,permutation_list_1,subs_not_found_1):

	# Indexes of entities not found in proportion to the Not Found 1 List
	search_indexes = []

	# permutation_not_found: a permutated string that was not found -> "WORD ARRANGEMENT"
	for permutation_not_found in subs_not_found_list_2:

		# possible_permutations: a list containing the possible permutations of from the Not Found 1 list -> ["WORD ARRANGEMENT"]
		for possible_permutations in permutation_list_1:

			# Get the index of the location of such permutation to output its location in proportion to the original Not Found 1 List
			entity_not_found_index = permutation_list_1.index(possible_permutations)

			# permutation_word: the actual string in the possible_permutations list -> "WORD ARRANGEMENT"
			for permutation_word in possible_permutations:

				# Check if permutation_not_found (not found permutated string) is the same as permutation_word 
				if permutation_not_found == permutation_word:

					# Append the found index
					search_indexes.append(entity_not_found_index)

				else:
					pass

	# Remove duplicates
	search_indexes = list(set(search_indexes))

	# List the entities in need of a google search
	entities_to_search = [subs_not_found_1[i] for i in search_indexes]		

	return entities_to_search


'''
Here we will look for the emails and any related information in the data bases we already possess.
'''
def existing_database_search(bid_needed_csv_file,dir_database,counties_needed,cities_needed,count):
	# Define the Bid Needed Subs DataFrame
	df_dir_correlation = pd.read_csv(bid_needed_csv_file)

	print(len(df_dir_correlation))

	# Define the cities
	cities_needed = cities_needed

	# Define the DIR Tabulation database
	df_dir_tabulation = pd.read_csv(dir_database)

	# Convert the names column's values into Uppercase letters
	df_dir_tabulation["EntityName"] = df_dir_tabulation["EntityName"].str.upper()

	# Convert the names column's values into strings
	df_dir_tabulation["EntityName"] = df_dir_tabulation["EntityName"].astype(str)

	# Acquire the first four subs from the needed sub list for the bid in question
	testing_subs_needed = df_dir_correlation["BusinessName"][count:count+50]

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

	'''
	Approach 1: I would rather look in google, than 
	'''
	attempt_refined = []

	for sub_lost in subs_not_found:

		for undesider_word in undesired_company_words:

			if f" {undesider_word}" in sub_lost:
				undesired_word_index = sub_lost.index(undesider_word)
				new_sub = sub_lost[:undesired_word_index-1]
				if " " not in new_sub:
					continue
				else:
					attempt_refined.append(new_sub)

	# '''
	# Approach 2: This one works
	# '''

	# # Names not found First Word
	# sub_names_not_found_first_word = []

	# # Names not found first two words
	# sub_names_first_two_words = []

	# # Now that we know which were not found, we need to build the combination iteration
	# sub_names_splited = []

	# # Iterate through each not-found name and split it
	# for sub_notfound_name in subs_not_found:
	# 	spliting_name = sub_notfound_name.split(" ")
	# 	sub_names_splited.append(spliting_name)
	# 	sub_names_not_found_first_word.append(spliting_name[0])
	# 	sub_names_first_two_words.append(" ".join([spliting_name[0],spliting_name[1]]))

	# # List of lists of valid permutations, i.e. the number of permutations per each of the Not Found 1 without undesired words
	# permutations_inquiry = []

	# # A list of all possible individual sub name permutations
	# possible_subs_name_permutations = []

	# # Iterate through each splited name and pinpoint the possible permutations
	# for sub_splited_name in sub_names_splited:
	# 	sub_name_permutation = combinations(sub_splited_name,2) # two word combinations

	# 	# List of permutations for further list
	# 	list_of_permutations = []

	# 	# Extract the individual permutation
	# 	for permutation in sub_name_permutation:

	# 		# Unwanted words? "False" so far...
	# 		unwanted_words_status = False

	# 		# Check each individual words
	# 		for permutation_word in permutation:

	# 			# Determine if the permutation contains unwanted words
	# 			if permutation_word in undesired_company_words:

	# 				# Flip the switch
	# 				unwanted_words_status = True
	# 			else:
	# 				continue

	# 		# If the permutation does not contains unwanted, append it to desired list
	# 		if unwanted_words_status == False:

	# 			# Convert the set into a list
	# 			new_search_combination = list(permutation)

	# 			# Convert the list into a joined string separated by a space
	# 			new_search_word = " ".join(new_search_combination)

	# 			# Append the newly string into the desired list
	# 			possible_subs_name_permutations.append(new_search_word)
	# 			list_of_permutations.append(new_search_word)

	# 		# Continue basically
	# 		else:
	# 			pass

	# 	permutations_inquiry.append(list_of_permutations)

	# # New function to classify words that will be looked for only if they have the first word of the company
	# new_set_of_permutations_to_search = first_word_appearance_only(permutations_inquiry,sub_names_not_found_first_word)

	# # Single character permutations refinement step
	# refined_new_set_of_permutations_to_search = single_character_permutation_refinement(new_set_of_permutations_to_search,sub_names_first_two_words)
	# refined_original_permutations = refined_new_set_of_permutations_to_search[0]
	# refined_possible_subs_names = refined_new_set_of_permutations_to_search[1]

	# # Apply the searching function again with the new names to be searched
	# search_dir_result_2 = existing_database_search_dir_iteration(refined_possible_subs_names,df_dir_tabulation)


	'''
	Approach 1: Result
	'''
	search_dir_result_2 = existing_database_search_dir_iteration(attempt_refined,df_dir_tabulation)




	# Second search: Array of indexes
	index_list_subs_needed_2 = search_dir_result_2[0]

	# Second search: Subs found 
	sub_names_found_2 = search_dir_result_2[1]
	print(f"Search 2 Found: {len(sub_names_found_2)} {sub_names_found_2}")

	# Second search: Subs not found
	subs_not_found_2 = search_dir_result_2[2]
	print(f"Search 2 Not Found: {len(subs_not_found_2)} {subs_not_found_2}")

	# Indexes pertaining to the "permutations_inquiry" list that tell the items with the first word in them
	first_word_instance_indexes = []
	
	# Identify which subs were not found based on the original list
	# subs_not_found_search_need = subs_not_found_now_search(subs_not_found_2,
	# 	refined_original_permutations,
	# 	subs_not_found)


	# Appending the new indexes to the existing index lists
	for index_2 in index_list_subs_needed_2:
		index_list_subs_needed.append(index_2)


	# Remove duplicates from the index list
	index_list_subs_needed = list(set(index_list_subs_needed))

	# The new output containing the subcontractors' name with their email
	sub_information_output = pd.DataFrame()

	# An excel visualization of subs not found
	subs_not_found_df = pd.DataFrame()
	subs_not_found_total = [i for i in subs_not_found_2]
	subs_not_found_df["SubNotFound"] = subs_not_found_total

	# Lists for the new data frame
	sub_names = []
	sub_emails = []
	sub_counties = []
	sub_cities = []

	# Allocate parameters into a list for future dataframe
	for index in index_list_subs_needed:
		if "Awarding Body" in df_dir_tabulation.iloc[:,1][index]:
			pass
		else:
			sub_names.append(df_dir_tabulation.iloc[:,0][index]) # Name
			sub_emails.append(df_dir_tabulation.iloc[:,2][index]) # Email
			sub_cities.append(df_dir_tabulation.iloc[:,6][index]) # cities
			sub_counties.append(df_dir_tabulation.iloc[:,18][index]) # counties
			

	# Append the list and make them the columns of the new dataframe
	sub_information_output["SubNames"] = sub_names
	sub_information_output["SubEmails"] = sub_emails
	sub_information_output["SubCity"] = sub_cities
	sub_information_output["SubCounty"] = sub_counties
	
	# Drop any duplicates
	sub_information_output.drop_duplicates(inplace=True)

	cities_needed.sort()

	for index, row in sub_information_output.iterrows():

		if pd.isna(row.iloc[2]) == True:
			city = str(row.iloc[2])
		
		else:
			city = row.iloc[2].title()

		county = row.iloc[3]

		if county not in counties_needed and pd.isna(county) == False:
			sub_information_output.drop(index,inplace=True)

		elif city not in cities_needed and pd.isna(city) == False:
			sub_information_output.drop(index,inplace=True)



	return sub_information_output, subs_not_found_df 


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

	# Emails extracted list after all operations below
	emails_extracted = []

	# Allocate the names (and other attributes) that will help you find the entitiy in the web
	for remaining_name in list_with_remaining_sub_names:

		# Entity google searchg instance emails
		entity_google_search_emails = []

		# Websites in which the entity can be found
		entity_location_websites = []

		# Search it in the web
		driver = webdriver.Chrome()
		driver.get("https://google.co.in/search?q=" + remaining_name)
		time.sleep(4)

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
				EC.presence_of_element_located((By.ID,"res")))

			# Acquire the elements containing the links
			google_results_links = google_results.find_elements(By.TAG_NAME,"a")

			# Extract the actual urls from the links
			individual_links = [individual_link.get_attribute("href") for individual_link in google_results_links]

			# Before proceeding with entering every single Google search website, let's remove the first website we entered above from the list
			for website in individual_links:
				# Adding websites
				entity_location_websites.append(website)

			# Remove any duplicated websites that might've appeared
			entity_location_websites = list(set(entity_location_websites))

			# Where all the threads will be located
			linking_threads = []

			# Now, let's build something to iterate through each newly acquired website, while skipping the one we already visited
			result_queue = Queue()

			# Iterate through each website from the Google search results and extract the "mailto:" element using multithrearding()
			for url_attempt in entity_location_websites:

				# Apply the multithrearding() function: 
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

			# We allocate into the emails extracted list only the actual emails, not other elements
			for i in resultings:
				for j in i:
					if isinstance(j,list):
						for k in j:
							if "@" in k:
								entity_google_search_emails.append(k.lower())


			# Remove duplicates again
			entity_google_search_emails = list(set(entity_google_search_emails))

			# Remove debris
			entity_google_search_emails = [item for item in entity_google_search_emails if item]

			# Append the subset into the main set of emails 
			emails_extracted.append([remaining_name,entity_google_search_emails])

		except Exception as exc:
			raise RuntimeError("Top Google Searches problem") from exc 


	'''
	Allocate the results into a pandas DataFrame using the same structure of the DIR Results data frame for
	future combination of both.
	'''
	returnable_dataframe = pd.DataFrame()

	# Lists for data frame above
	sub_names_google_result = []
	sub_emails_google_result = []

	# EntityName column
	for entity_search_result in emails_extracted:
		sub_names_google_result.append(entity_search_result[0])
		sub_emails_google_result.append('; '.join(entity_search_result[1]))

	# Allocate the lists into the dataframe
	returnable_dataframe["SubNames"] = sub_names_google_result
	returnable_dataframe["SubEmails"] = sub_emails_google_result

	# Beautiful Result
	return returnable_dataframe

# Combining dataframes (pretty easy, but repetitive, therefore a function)
def combining_dataframes_and_outputing(list_of_dataframes):
	main_dataframe = pd.concat(list_of_dataframes)
	return main_dataframe



def append_county_column_to_database(original_database_file,ca_municipalities):

	# Load the DIR Data base
	original_dir_db = pd.read_csv(original_database_file)
	original_dir_db = original_dir_db.fillna("")

	# Load the CA Municipalities file
	ca_municipalities_file = pd.read_csv(ca_municipalities)

	# Where the real reference is going to be
	ca_counties = [row.iloc[1].split("County")[0][:-1] for index, row in ca_municipalities_file.iterrows()]
	ca_counties = list(set(ca_counties))
	ca_counties.sort()

	counties_municipalities = [[] for _ in range(len(ca_counties))]

	# Create a list that iterates through the ca_municipalities_file and if ca_counties[0] is in iloc[2], it appends it to a list
	for index, row in ca_municipalities_file.iterrows():

		# Pinpoint the county and cleanse it
		county = row.iloc[1].split("County")[0][:-1]

		# if the county is equal to one of the counties in the extracted ca_counties list, get its index from the counties_municipalities list
		if county in ca_counties:

			# Convert the position into an index
			index_of_county = ca_counties.index(county)

			# Transcribe the city to the county respective list in counties_municipalities
			counties_municipalities[index_of_county].append(row.iloc[2])


	# # Now, identify where is the newly county row number going to be based on index
	# for index, row in original_dir_db.iterrows():

	# 	# the city string
	# 	city_cell = row.iloc[6]

	# 	# Split the cities with a state on them
	# 	if "," in city_cell:
	# 		city_cell = city_cell.split(",")[0]
		
	# 	# Modify the string in order to match it with other strings
	# 	city_cell = city_cell.title()

	# 	# city_list: a list containing cities which was extracted previously -> ["City1","City2","City3"]
	# 	for city_list in counties_municipalities:

	# 		# The respective index of counties_municipalities in order to match it with the respective county index of ca_counties
	# 		county_index = counties_municipalities.index(city_list)

	# 		# city: the actual city string -> "City1"
	# 		for city in city_list:

	# 			# if the city is equal to the city_cell, then it is a match
	# 			if city_cell == city:

	# 				# Assign the respective county
	# 				original_dir_db.loc[index,"EntityCounty"] = ca_counties[county_index]
	

	# Transcribe to csv
	#original_dir_db.to_csv("dir_entities_refined.csv",index=False)
	

	return counties_municipalities, ca_counties


def generating_california_administrative_divisions(cities, counties, counties_needed, cdp_file):

	# List that will be outputed
	cities_needed = []

	# iterate through the given lists and output the desired list
	for county,city_list in zip(counties,cities):

		# If the city is in one of our desired counties, iterate through it and extract its cities
		if county in counties_needed:
			for city in city_list:
				cities_needed.append(city)

	# CDPs turn
	cdp_df = pd.read_csv(cdp_file)

	cities_2 = []

	# Segregate needed counties from non-needed counties
	for index, row in cdp_df.iterrows():

		city = row.iloc[0]
		county = row.iloc[1]

		# Segregation
		if county in counties_needed:
			cities_needed.append(city)


	cities_needed.sort()

	# Voila
	return cities_needed



def combining_csv_files(directory_with_files):
	csv_files = glob.glob(directory_with_files+'/*.csv')

	combined_df = pd.DataFrame()

	for csv_file in csv_files:
		df = pd.read_csv(csv_file)
		combined_df = pd.concat([combined_df,df],ignore_index=True)

	combined_df.drop_duplicates()

	return combined_df.to_csv(f"{directory_with_files}/subcontractors_ready.csv",index=False)

	
			





	


	

# Onset
if __name__ == '__main__':
	# Identify which counties you need/Users/damiamalfaro/Desktop/testing_wesonder/Database_connections/extractions
	needed_counties = ["San Diego","Los Angeles","San Bernardino","Orange","Riverside"]

	# Identify which licenses you need
	needed_licenses = ["C13|C-13"]

	# Census Designated Places in California
	cdps = "/Users/damiamalfaro/Desktop/testing_wesonder/Wikipedia/census_designated_places_california.csv"

	output_location = "/Users/damiamalfaro/Desktop/testing_wesonder/Database_connections/extractions2"

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
	#print(subcontractor_categorization(new_csv_cslb_file,needed_counties,needed_licenses))


	'''
	Step 3.5: Modify the existing DIR Entities data base in order to display the county as a column as well.
	The current step wasn't supposed to be included, but that is the beauty of practice, it reveals the beauty of phenomena by revealing its
	nature.
	'''
	# dir_database_file_original = "/Users/damiamalfaro/Desktop/testing_wesonder/Database_connections/dir_entities.csv"
	# california_municipalities_file = "/Users/damiamalfaro/Desktop/testing_wesonder/Database_connections/California_Incorporated_Cities.csv"
	# california_administrative_divisions = append_county_column_to_database(dir_database_file_original,california_municipalities_file)
	# cities = california_administrative_divisions[0]
	# counties = california_administrative_divisions[1]


	# # '''
	# # Sub-step 4: Generate a list of counties and cities needed from step 3.5
	# # '''
	# cities_in_question = generating_california_administrative_divisions(cities,counties,needed_counties,cdps)


	# # '''
	# # Step 4: Check if the subcontractors are in the existing DIR and DVE data bases.
	# # '''
	# count = 0
	# while count != 100:

	# 	print(f"\n-------------\nCurrent Count: {count}\n-------------")

	# 	count_index = int(count // 100)

	# 	dir_database_file = "/Users/damiamalfaro/Desktop/testing_wesonder/Database_connections/dir_entities_refined.csv"
	# 	bid_needed_subs_csv_file = "/Users/damiamalfaro/Desktop/testing_wesonder/Database_connections/bid_subcontractors.csv"
	# 	dir_search_results = existing_database_search(bid_needed_subs_csv_file,dir_database_file,needed_counties,cities_in_question,count)

	# 	# The extracted data frame (intended to be allocated in a new excel)
	# 	dataframe_with_results = dir_search_results[0]
	# 	dataframe_with_results.to_csv(f"extractions2/found_subs_{count_index}.csv",index=False)
	# 	print(dataframe_with_results)

	# # Need to search for the following remaining subs
	# # subs_still_needed_df = dir_search_results[1] # Apply google search
	# # subs_still_needed_df.to_csv(f"extractions2/not_found_subs_{count_index}.csv",index=False)
	# # print(subs_still_needed_df)

	# 	count += 100


	# '''
	# Step 5: Search subcontractor from the newly extracted list and search their email on the web.
	# '''
	# # Search for the remaining names
	# google_search_results = searching_needed_subs(subs_still_needed) # Input: list()

	# # Search for the needed entities
	# if len(google_search_results) == 0:
	# 	print("No Google Search Results")
	# else:
	# 	print(google_search_results)
	# 	google_search_df = google_search_results

	# '''
	# Combine dataframes and output them
	# '''
	# list_of_dataframes = [
	# dataframe_with_results,
	# google_search_df
	# ]
	# print(combining_dataframes_and_outputing(list_of_dataframes))

	'''
	Step 6: Put the resulting dataframes from Step 4 into a combined dataframe
	'''
	list_of_new_dataframes = os.path.join(os.getcwd(),"extractions2")
	combining_csv_files(list_of_new_dataframes)













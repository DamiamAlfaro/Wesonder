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

url = "https://vendors.planetbids.com/portal/14058/bo/bo-search"

def scroll_table_container(container, driver,scroll_pause_time=1):
    
    last_height = driver.execute_script("return arguments[0].scrollHeight", container)
    
    while True:
        # Scroll down by a small amount within the container
        driver.implicitly_wait(10)
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", container)
        driver.implicitly_wait(10)
        
        # Wait to load the new content
        time.sleep(scroll_pause_time)
        
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return arguments[0].scrollHeight", container)
        if new_height == last_height:
            break
        last_height = new_height

    result_message = "Round Completed"
    return result_message

def extraction(url,number):
    # Make sure the csv file ins't emtpy, if it is, set beacon to 0 as that is your starting point
    beacon = 0
    beacon += number

    # Start Selenium's webdriver
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(10)

    # Identifies if the total number of bids in the municipality increased
    total_bids = driver.find_element(By.CLASS_NAME,"bids-table-filter-message")
    total_bids_text_splitted = total_bids.text.split(" ")
    really_total_bids = int(total_bids_text_splitted[1])
    print(f"Found {really_total_bids} bids")

    # Table container with all bids in the municipality's planetbids portal
    current_bids = driver.find_element(By.CLASS_NAME,"table-overflow-container")
    driver.implicitly_wait(25)

    # Scroll through the table container
    resul_croll = scroll_table_container(current_bids,driver)
    print(resul_croll)
    driver.implicitly_wait(400)

    # After scrolling, we put all bids in the webpage into a list; n bids
    failing_count = 0
    bids = current_bids.find_elements(By.TAG_NAME,"tr")
    while len(bids) < really_total_bids:
        print(f"measurement {failing_count}")
        break
        failing_count += 1
        current_bids = driver.find_element(By.CLASS_NAME,"table-overflow-container")
        scroll_table_container(current_bids,driver)
        bids = current_bids.find_elements(By.TAG_NAME,"tr")
    print("Successful")







    # Output
    bid_general_info = []
    bid_line_items = []
    bid_documents = []
    bid_addenda = []
    bid_q_and_a = []
    bid_prospective_bidders = []
    bid_results = []

    '''
    General info
    '''
    try:
        # Assuring stability
        table_container = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CLASS_NAME,"bids-table-container"))
        )
    
        current_bids = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CLASS_NAME,"table-overflow-container"))
        )
    
        # The <tr> element we seek
        targeted_bids = bids[beacon+2]


    
        # Once acknowledged, pinpoint it and click on it, aka open it
        driver.execute_script("arguments[0].scrollIntoView();",targeted_bids)
        time.sleep(2)
        print(targeted_bids.text)
        driver.execute_script("arguments[0].click();",targeted_bids)
        
        # Make sure the element was clicked
        WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.CLASS_NAME,"bid-detail-wrapper"))
            )
    
        # Pinpoint the general info
        general_info = driver.find_element(By.CLASS_NAME,"bid-detail-wrapper")
    
        # Append the general info into the list
        bid_general_info.append(general_info.text.split("\n"))
            
        driver.implicitly_wait(1)
    except:
        sys.exit(1)

    '''
    Line Items
    '''
    try:
        try:
            WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.CLASS_NAME,"bidLineItems"))
            )
            # Pinpoint the line items tab element
            line_items_tab = driver.find_element(By.CLASS_NAME,"bidLineItems")
        
            # Click the element
            line_items_tab.click()
        
            # Assure the table was found
            WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.CLASS_NAME,"bid-line-items"))
            )
        
            # Pinpoint the table containing the line items
            line_items = driver.find_element(By.CLASS_NAME,"bid-line-items")
        
            # Materialize the line items into strings and append them respectively
            bid_line_items.append(line_items.text.split("\n"))
            driver.implicitly_wait(2)
        except TimeoutException:
            print("No Line items")
            bid_line_items.append(["No Line Items",0])
    except:
        print(f"Problem with the line items at {targeted_bids.text}")
        bid_line_items.append(["No Line Items",0])
        

    '''
    Documents
    '''
    try:
        documents_tab = driver.find_element(By.CLASS_NAME,"bidDocs")
        documents_tab.click()
        try:
            WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.CLASS_NAME,"table-overflow-container"))
            )
            documents = driver.find_element(By.CLASS_NAME,"table-overflow-container")
            
            bid_documents.append(documents.text.split('\n'))
                
            driver.implicitly_wait(1)
        except TimeoutException:
            print("No Documents")
            bid_documents.append(["No Documents",0])
        
    except:
        print(f"Problem with the bid documents at {targeted_bids.text}")
        bid_documents.append(["No Documents",0])

    '''
    Addenda/Emails
    '''
    try:
        # Reposition to the next tab
        addenda_tab = driver.find_element(By.CLASS_NAME,"bidAddendaAndEmails")
        addenda_tab.click()

        # Did the click worked?
        try:
            WebDriverWait(driver,20).until(
                EC.presence_of_element_located((By.CLASS_NAME,"section-heading"))
            )
            
            # If so, find each of the addenda/emails with their respective class "accordion"
            try:
                
                # The length of this list is the amount of addenda/emails found
                heading_check = driver.find_elements(By.CLASS_NAME,"accordion")

                # Iterate
                for addenda_item in heading_check:

                    # These functions check whether the item (<class "accordion">) is visible and is can be interacted with
                    if addenda_item.is_displayed() and addenda_item.is_enabled():
                        try:
                            WebDriverWait(driver,20).until(
                                EC.element_to_be_clickable((By.CLASS_NAME, "accordion"))
                            )

                            # Since there could be multiple items, we need to locate to their view and click on them
                            driver.execute_script("arguments[0].scrollIntoView();",addenda_item)
                            WebDriverWait(driver,20).until(
                                EC.presence_of_element_located((By.CLASS_NAME, "accordion"))
                            )

                            # Click click click click
                            addenda_item.click()

                            # Append the text of the newly opened accordion (containing the addenda/email update)
                            bid_addenda.append(addenda_item.text.split('\n'))
                            
                        except Exception as exe:
                            bid_addenda.append(["No Addenda",0])
                    else:
                        print(f"{i.text} is acting like a bitch")
            except:
                
                # There are bids with no addenda/emails
                print("No Addenda nor Emails")
                bid_addenda.append(["No Addenda",0])

          
        except TimeoutException:
            print("No Addenda")
            bid_addenda.append(["No Addenda",0])
        
    except:
        print(f"Problem with the bid addenda at {targeted_bids.text}")
        bid_addenda.append(["No Addenda",0])

    
    '''
    Q&A
    '''
    try:
        # Reposition towards the Q&A section
        try:
            WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.CLASS_NAME,"bidQandA"))
            )

            try:
                # Assure there are questions sets
                q_and_a_tab = driver.find_element(By.CLASS_NAME,"bidQandA")
                q_and_a_tab.click()
                WebDriverWait(driver,20).until(
                    EC.presence_of_element_located((By.CLASS_NAME,"bid-q-and-a-question"))
                )
                try:
                    # Position yourself on the tabulation of question
                    q_and_a_display = driver.find_element(By.CLASS_NAME,"bid-detail-wrapper")
        
                    # Count total question sets
                    question_sets = q_and_a_display.find_elements(By.CLASS_NAME,"bid-q-and-a-question") # int (total question sets)
        
                    # Locate buttoms
                    q_and_a_buttoms = q_and_a_display.find_elements(By.CLASS_NAME,"soft-blue-xs-btn")
        
                    # Locate "Expand All" buttom
                    expand_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[text()='Expand All' and contains(@class, 'soft-blue-xs-btn')]"))
                    )
    
                    # Click buttom
                    expand_button.click()
    
                    # Assure its functionality
                    bid_questions_in_q_and_a = WebDriverWait(driver,20).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR,".question-submenu"))
                    )

                    # Now you can retrieve the text of the Q&As
                    try:
                        for bid_q_and_a_question in bid_questions_in_q_and_a:
                            bid_q_and_a.append(bid_q_and_a_question.text)
                    except Exception as exe:
                        print("Q&A extraction did not work")
                        print(exe)
                        bid_q_and_a.append("No questions")
                except:
                    print("Buttom did not executed perhaps?")
                    bid_q_and_a.append("No questions")
                
            except:
                # Continue if not
                variable = "There is zero questions"
                bid_q_and_a.append([letter for letter in variable])

        except TimeoutException:
            bid_q_and_a.append("No questions")
    
    except:
        print(f"Problem with the bid Q&A at {targeted_bids.text}")
        bid_q_and_a.append("No questions")

    '''
    Prospective Bidders: one of the regular operations (we need to see the rate of change
    of new prospective additions for each bid) that will count as a datum.
    '''
    try:
        # Reposition yourself on the Prospective Bidders tab
        prospective_bidders_tab = driver.find_element(By.CLASS_NAME,"bidPBs")
        prospective_bidders_tab.click()

        try:
            # Make sure the relocation work
            WebDriverWait(driver,20).until(
                EC.presence_of_element_located((By.CLASS_NAME,"showingMessage"))
            )

            # Pinpointing the total amount of prospective bidders and recording it (this should be regularly though)
            prospective_bidders_message = driver.find_element(By.CLASS_NAME,"showingMessage")
            prospective_bidders_message_broken = prospective_bidders_message.text.split(" ")
            prospective_bidders_total = prospective_bidders_message_broken[1]
            bid_prospective_bidders.append([prospective_bidders_total])

            # # Now collect the names and information and append
            # prospective_bidders_text = driver.find_element(By.CLASS_NAME,"bid-detail-wrapper")
            # prospective_bidders_text_line_items = prospective_bidders_text.text.split('\n')
            # prospective_bidders_onset = 0
            # for pb_text_item in prospective_bidders_text_line_items:
            #     if pb_text_item == prospective_bidders_message.text:
            #         prospective_bidders_onset += prospective_bidders_text_line_items.index(pb_text_item)
            #     else:
            #         continue
            # bid_prospective_bidders.append(prospective_bidders_text_line_items[prospective_bidders_onset:])

            try:
                bid_prospective_bidders_tabulation = WebDriverWait(driver,10).until(
                    EC.presence_of_element_located((By.XPATH, "//tbody[@role='rowgroup']"))
                )
                bid_prospective_bidders_rows = bid_prospective_bidders_tabulation.find_elements(By.TAG_NAME,"tr")
                for bid_prospective_bidder in bid_prospective_bidders_rows:
                    bid_prospective_bidders.append([bid_prospective_bidder.text])
            except:
                print("DID NOT WORK BITCH")
                    
 
        except TimeoutException:
            print("Prospective Bidders Timeout")
            bid_prospective_bidders.append([0])
    except:
        print(f"Problem with the bid prospective bidders at {targeted_bids.text}")
        bid_prospective_bidders.append([0])

    '''
    Bid Results
    '''
    try:
        # Reposition yourself on the Bid Results tab, click() will work regardless of Bid Results being available or not
        bid_results_tab = driver.find_element(By.CLASS_NAME,"bidResults")
        bid_results_tab.click()

        # Indicators of scenarios 
        life_or_death_1 = False
        life_or_death_2 = False
        life_or_death_3 = False

        # Try to see if bid results are not found ("None" displayed).
        try: 
            # Make sure the display message is visible
            WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.CLASS_NAME,"no-records-found"))
            )

            # Pinpoint the message
            no_records_found = driver.find_element(By.CLASS_NAME,"no-records-found")

            # Append it as is ("None") to the list
            bid_results.append([0])
        except TimeoutException:
            life_or_death_1 = True

        # Try to see if bid results were not made public 
        try:
            WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.CLASS_NAME,"not-public-msg"))
            )
            
            bid_results_not_public = driver.find_element(By.CLASS_NAME,"not-public-msg")

            # The text is: "Bid Results have not been made public."
            bid_results.append([1])
        
        except TimeoutException:
            life_or_death_2 = True

        if life_or_death_1 == True and life_or_death_2 == True:
            try:
                # Make sure that is the case
                WebDriverWait(driver,10).until(
                    EC.presence_of_element_located((By.CLASS_NAME,"showingMessage"))
                )
            
                # Pinpoint the number of final bidders and append number: "Showing n Bid Results"
                bid_results_message = driver.find_element(By.CLASS_NAME,"showingMessage")
            
                # Pinpoint the table containting the final bidders and append the number
                bid_results_table_display = driver.find_element(By.CLASS_NAME,"table-overflow-container")
                
                # Convert the table to a list containing each bidder
                bidders = bid_results_table_display.find_elements(By.TAG_NAME,"tr")
            
                # Iterate through the list and mine each of the bidders
                for bidder in range(len(bidders[1:])):
                    WebDriverWait(driver,10).until(
                        EC.presence_of_element_located((By.CLASS_NAME,"showingMessage"))
                    )
                    testing3 = driver.find_element(By.CLASS_NAME,"table-overflow-container")
                    
                    other = testing3.find_elements(By.TAG_NAME,"tr")
                    
                    bid_results_bidder_information = []
                    # Make sure the bidder's <tr> element is clickable 
                    try:
                        WebDriverWait(driver,10).until(
                            EC.element_to_be_clickable((By.TAG_NAME,"tr"))
                        )
                    except:
                        print("Apparently it isn't clickable")
            
                    # If it is clickable, click it (duh)
                    driver.execute_script("arguments[0].click();", other[bidder+1])
            
                    # Make sure the click worked
                    WebDriverWait(driver,10).until(
                        EC.presence_of_element_located((By.CLASS_NAME,"sub-detail"))
                    )

                    # Grand-Total-Class
                    bidder_grand_total_class = driver.find_element(By.CLASS_NAME,"bid-totals")

                    # Grand total amount submitted and append only the amount, we don't care about the text...
                    bidder_grand_total_amount = bidder_grand_total_class.find_element(By.CLASS_NAME,"col-1-2")
                    grand_total_stratified = bidder_grand_total_amount.text.split(" ")
                    bid_results_bidder_information.append([grand_total_stratified[2]])
                    
                    # Position yourself within the detail tab
                    bidder_details = driver.find_element(By.CLASS_NAME,"sub-detail")
        
                    # We just want the text, not the useless header text, so let's extract it
                    bidder_general_info = bidder_details.find_element(By.CLASS_NAME,"col-12")
                    bid_results_bidder_information.append(bidder_general_info.text.split("\n"))
            
                    # See which options are available to mine (details, subcontractors, and line items)
                    bidder_buttoms_element = bidder_details.find_element(By.ID,"detail-navigation")
            
                    # Usually there are 3 options available, but some of them only have 1 or 2; nevertheless, the following list will tell you
                    bidder_total_buttoms = bidder_buttoms_element.text.split("\n")
            
                    # We need the variables to click on
                    if len(bidder_total_buttoms) > 2:
                        # [Subcontractors] available
                        bidder_subcontractors = driver.find_element(By.CLASS_NAME,"link-subcontractors")
                        bidder_line_items = driver.find_element(By.CLASS_NAME,"link-lineItems")
                        
                    else:
                        # Only line items available
                        try:
                            bidder_line_items = driver.find_element(By.CLASS_NAME,"link-lineItems")
                        except:
                            print("No Bid Results Line Items")
                        try:
                            bidder_subcontractors = driver.find_element(By.CLASS_NAME,"link-subcontractors")
                        except:
                            print("No Bid Results Subcontractors")
                        
            
                    # Extract subcontractors used as well as line items
                    try:
                        # First step
                        bidder_subcontractors_all = []
                        bidder_subcontractors.click()
                        WebDriverWait(driver,10).until(
                            EC.presence_of_element_located((By.CLASS_NAME,"bid-response-detail-tab"))
                        )
            
                        # Pinpoint the subcontractor view page, will be used as reference
                        bidder_subcontractor_page = driver.find_element(By.CLASS_NAME,"bid-response-detail-tab")
            
                        # Find all subcontractors
                        bidder_total_subcontractors = WebDriverWait(driver,10).until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.set-heading'))
                        )
        
                        try:
                            for bidder_subcontractor in range(len(bidder_total_subcontractors)):
                                subcontractor_information = []
                                driver.execute_script("arguments[0].click();", bidder_total_subcontractors[bidder_subcontractor])
                    
                                subcontractor_elements = WebDriverWait(driver,10).until(
                                    EC.presence_of_all_elements_located((By.CSS_SELECTOR,'input[type="text"]'))
                                )
                                for input_element in subcontractor_elements:
                                    input_value = input_element.get_attribute('value')
                                    subcontractor_information.append(input_value)
                                driver.execute_script("arguments[0].click();", bidder_total_subcontractors[bidder_subcontractor])
                                bidder_subcontractors_all.append(subcontractor_information)
                            
                            
                        except Exception as exe:
                            print("something's up")
                            print(exe)
                            
                        bid_results_bidder_information.append(bidder_subcontractors_all)
            
                        # Step 2: Get Bid Results line items 
                        bidder_line_items.click()
                        bid_line_items_results = []
                        try:
                            WebDriverWait(driver,10).until(
                                EC.presence_of_element_located((By.ID,"bidResultDetail"))
                            )
                        except:
                            print("No Bid Line Items Results showing")
            
                        bidder_results_table = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'table.pb-subheader-table.data'))
                        )
        
                        bidder_results_table_rows = bidder_results_table.find_elements(By.TAG_NAME, "tr")
            
                        for bid_results_table_row in bidder_results_table_rows:
                            bid_line_item = []
                            bid_results_table_row_cells = bid_results_table_row.find_elements(By.TAG_NAME,"td")
                            for bid_results_table_row_cell in bid_results_table_row_cells:
                                if len(bid_results_table_row_cell.text) == 0:
                                    pass
                                else:
                                    bid_line_item.append(bid_results_table_row_cell.text)
                            bid_line_items_results.append(bid_line_item)
                        
                        bid_results_bidder_information.append(bid_line_items_results)
                                   
                        
                    except Exception as exe:
                        print("No Subcontractors available")
                        bid_results.append([0])
        
                    # Only line items available
                    try:
                        bidder_line_items.click()
                        bid_line_items_results = []
                        try:
                            WebDriverWait(driver,10).until(
                                EC.presence_of_element_located((By.ID,"bidResultDetail"))
                            )
                        except:
                            print("No Bid Line Items Results showing")
            
                        bidder_results_table = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'table.pb-subheader-table.data'))
                        )
            
                        bidder_results_table_rows = bidder_results_table.find_elements(By.TAG_NAME, "tr")
            
                        for bid_results_table_row in bidder_results_table_rows:
                            bid_line_item = []
                            bid_results_table_row_cells = bid_results_table_row.find_elements(By.TAG_NAME,"td")
                            for bid_results_table_row_cell in bid_results_table_row_cells:
                                if len(bid_results_table_row_cell.text) == 0:
                                    pass
                                else:
                                    bid_line_item.append(bid_results_table_row_cell.text)
                            bid_line_items_results.append(bid_line_item)
                        
                        bid_results_bidder_information.append(bid_line_items_results)
                    except:
                        print("No Line items")
            
                    bid_results.append(bid_results_bidder_information)
                    bid_results_tab = driver.find_element(By.CLASS_NAME,"bidResults")
                    bid_results_tab.click()
                    
            except TimeoutException:
                print("No Bid Results yet")


        
        
            
    except:
        print(f"Problem with the bid results at {targeted_bids.text}")
        bid_results.append([0])
        
        
        
    driver.quit()
    
    return [bid_general_info, 
            bid_line_items, 
            bid_documents, 
            bid_addenda, 
            bid_q_and_a, 
            bid_prospective_bidders, 
            bid_results]

def allocating_within_csv_file(self,folder_name):
    '''
    General Information
    '''
    # [[General, information]]
    current_file_location_0 = os.getcwd()
    targeted_city_folder_0 = os.path.join(current_file_location_0,folder_name)
    csv_file_title = ""
    general_information = self[0]
    for looking_for_title in general_information[0]:
        if "Invitation #" in looking_for_title:
            flag = general_information[0].index(looking_for_title)
            csv_file_title += re.sub(r'[^a-zA-Z0-9]', '_', general_information[0][flag+1])
        if "Bid Due Date" in looking_for_title:
            flag_pole = general_information[0].index(looking_for_title)
            flag_silk = general_information[0][flag_pole+1].split(" ")
            flag_symbol = flag_silk[0]
            csv_file_title += re.sub(r'[^a-zA-Z0-9]', '_', flag_symbol)
        if "Project Title" in looking_for_title:
            flag_base = general_information[0].index(looking_for_title)
            if flag_base < 20:
                flag_rope = general_information[0][flag_base+1].split(" ")
                flag_screw = [first_letter[0] for first_letter in flag_rope]
                flag_truck = ''.join(flag_screw)
                csv_file_title += re.sub(r'[^a-zA-Z0-9]', '_', flag_truck.upper())
            else:
                continue

    # Naming the csv file
    for file_naming in os.listdir(targeted_city_folder_0):
    	if file_naming == f"{csv_file_title}.csv":
    		csv_file_title += "_XND"


    print(csv_file_title)
    
    '''
    Line Items
    '''
    # [[line,items]]
    line_items = self[1] 

    '''
    Documents
    '''
    # [[documents,files]]
    documents = self[2] 

    '''
    Addenda & Emails
    '''
    # [[addendainfo_a1,addendainfo_a2],[addendainfo_b1,addendainfo_b2]]
    addenda = self[3]
    all_addenda = []
    for addenda_iterate in addenda:
        for addenda_iterate_further in addenda_iterate:
            try:
                if len(addenda_iterate_further) == 0:
                    pass
                else:
                    all_addenda.append(addenda_iterate_further)
            except:
                all_addenda.append(0)
                

    '''
    Questions & Answers
    '''
    # [question_and_answer1,question_and_answer2]
    q_and_a = self[4] 

    # Need to break down the questions further because someone was too lazy to do so before...
    q_and_a_refined = []
    for question_stratification in q_and_a:
        try:
            q_and_a_stratification_instance = question_stratification.split("\n")
            for question_attribute in q_and_a_stratification_instance:
                q_and_a_refined.append(question_attribute)
        except:
            pass

        

    '''
    Prospective Bidders
    '''
    # [[total_prospective_bidders],[prospective_bidder1],[prospective_bidder2]...[]]
    all_prospective_bidders = []
    prospective_bidders = self[5]
    for prospective_bidder_attribute in prospective_bidders:
        try:
            if prospective_bidders.index(prospective_bidder_attribute) == 0:
                all_prospective_bidders.append(f"PB {prospective_bidder_attribute[0]}")
            else:
                for prospective_bidder_datum in prospective_bidder_attribute:
                    prospective_bidder_individual = prospective_bidder_datum.split("\n")
                    for prospective_bidder_individual_datum in prospective_bidder_individual:
                        all_prospective_bidders.append(prospective_bidder_individual_datum)
                    
        except:
            for prospective_bidder_datum in prospective_bidder_attribute:
                all_prospective_bidders.append(prospective_bidder_datum)
        
    
    '''
    Bid Results: the most arduous one
    '''
    # [[[]]]
    all_bidders_and_subs_information = []
    bid_results = self[6] 
    for bidder_filter_a in bid_results:
        for bidder_filter_b in bidder_filter_a:
            try:
                for bidder_filter_c in bidder_filter_b:
                    if isinstance(bidder_filter_c,list):
                        for bidder_filter_d in bidder_filter_c:
                            all_bidders_and_subs_information.append(bidder_filter_d)
                    else:
                        all_bidders_and_subs_information.append(bidder_filter_c)
            except:
                all_bidders_and_subs_information.append(bidder_filter_b)
            
        

    '''
    Data Frame construction: building the csv file with the results from extraction()
    '''
    # Finding largest list
    max_length = max(
        len(general_information[0]),
        len(line_items[0]),
        len(documents[0]),
        len(all_addenda),
        len(q_and_a_refined),
        len(all_prospective_bidders),
        len(all_bidders_and_subs_information)
    )

    # Fill gaps with np.nan
    general_information[0] += [np.nan] * (max_length - len(general_information[0]))
    line_items[0] += [np.nan] * (max_length - len(line_items[0]))
    documents[0] += [np.nan] * (max_length - len(documents[0]))
    all_addenda += [np.nan] * (max_length - len(all_addenda))
    q_and_a_refined += [np.nan] * (max_length - len(q_and_a_refined))
    all_prospective_bidders += [np.nan] * (max_length - len(all_prospective_bidders))
    all_bidders_and_subs_information += [np.nan] * (max_length - len(all_bidders_and_subs_information))

    # Transcribe the newly modified data frames
    df_columns = pd.DataFrame({
        "BidGeneralInfo":general_information[0],
        "BidLineItems":line_items[0],
        "BidDocuments":documents[0],
        "BidAddenda":all_addenda,
        "BidQAndA":q_and_a_refined,
        "BidProspectiveBidders":all_prospective_bidders,
        "BidResults":all_bidders_and_subs_information
    })

    output_file_path = os.path.join(targeted_city_folder_1,f'{csv_file_title}.csv')
    df_columns.to_csv(output_file_path,index=False)
    



def delete_ds_store_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == '.DS_Store':
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f'Deleted: {file_path}')
                except Exception as e:
                    print(f'Error deleting {file_path}: {e}')





count = 836
while count != 977:
	print(count)
	current_file_location_1 = os.getcwd()
	targeted_city_folder_1 = os.path.join(current_file_location_1,"Orange County Sanitation District")
	delete_ds_store_files(targeted_city_folder_1)
	total_municipality_files = len(os.listdir(targeted_city_folder_1))
	print(total_municipality_files)
	allocating_within_csv_file(extraction(url,total_municipality_files),targeted_city_folder_1)
	count += 1



















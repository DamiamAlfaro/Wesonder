import pandas as pd # type: ignore
import time
import sys
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore


'''
Locate the CSI codes first since we are not going to iterate through all of them,
just the ones that actually require manufacturers.
'''
def webscraping_costcodes(url):

    # Initiate the driver
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)

    # Locate the CSI Divisions
    divisions = driver.find_elements(By.CLASS_NAME, 'p1')

    # Single page approach: retrieving the link url of elements, and webscraping them in a separate webdriver session
    division_links = []
    
    # Iterate through each division and extract each division link from it
    for division in divisions:

        division_a_tag = division.find_element(By.TAG_NAME,'a')

        url_link = division_a_tag.get_attribute('href')
        division_links.append(url_link)

    driver.quit()

    # Jump to the next function
    return division_links


'''
CSV Storage mechanism
'''
def store_in_csv(column1, column2, entire_spec, url_link, csv_file):
    
    df = pd.DataFrame({'SpecNumber':[column1],'SpecName':[column2],'EntireSpec':[entire_spec],'Link':[url_link]})
    df.to_csv(csv_file,mode='a',index=False,header=False)




'''
Webscrap the data for each manufacturer; returns a dataframe with the respective section 
and its subsections, along with the respective manufacturers of each subsection and their
respective attributes for user usage. Acquire the subdivisions links first
'''
def retrieving_subdivisions(url, csv_file):

    # Initiate the driver
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)

    # Locate the subdivisions
    subdivisions = driver.find_elements(By.CSS_SELECTOR,"div.grid.csi-item")

    # Iterate through each subdivision
    for subdivision in range(len(subdivisions)):

        # Assign the respective variables: subdivision codes, names, and respective url links
        subdivision_name_string = subdivisions[subdivision].text
        subdivision_name_split = subdivision_name_string.split(' ')
        subdivision_code = " ".join(subdivision_name_split[:3])
        subdivision_name = " ".join(subdivision_name_split[3:])
        link_itself = subdivisions[subdivision].find_element(By.TAG_NAME,'a').get_attribute('href')

        print(f'Code: {subdivision_code}\nName: {subdivision_name}\nLink: {link_itself}')

        # Store into csv file
        store_in_csv(subdivision_code, subdivision_name, subdivision_name_string, link_itself, csv_file)
        

'''
I know we are iterating through multiple csv files here, but organization leads to fewer mistakes. I'd rather
take prophylactic measures that take time than webscraping erroneously or in a sloppy manner.
'''
def storing_manufacturers_links_into_csv(list_of_variables, manufacturer_name, link_itself, refined_csv_file):
    
    # Delegate the variables
    spec_number = list_of_variables[0]
    spec_name = list_of_variables[1]
    whole_spec = list_of_variables[2]
    spec_link = list_of_variables[3]

    # Create the dataframe with the respective variables
    df = pd.DataFrame({
        'SpecNumber': [spec_number],
        'SpecName': [spec_name],
        'EntireSpec': [whole_spec],
        'ManufacturersLink': [spec_link],
        'ManufacturerName': [manufacturer_name],
        'ManufacturerLink': [link_itself]
    })


    # Allocate into csv file
    df.to_csv(refined_csv_file, mode='a', index=False, header=False)


'''
Using webscraping techniques, we will be extracting the datums associated with each manufacturer,
such as address, website, phone number, etc.
'''
def webscrap_manufacturers_links(list_of_variables, refined_csv_file):

    # Delegate the variables
    spec_number = list_of_variables[0]
    spec_name = list_of_variables[1]
    whole_spec = list_of_variables[2]
    spec_link = list_of_variables[3]

    # Activate the webdriver
    driver = webdriver.Chrome()
    driver.get(spec_link)
    time.sleep(2)

    # Locate the specific element directing to each manufacturer and extract the respective url link from it
    ul_element = driver.find_element(By.XPATH, "//ul[contains(@class, 'pure-u-1') and contains(@class, 'pure-u-md-2-3') and contains(@class, 'pure-u-lg-3-4') and contains(@class, 'pl01')]")


    # Retrieval 1: Retrieve the manufacturers with images first, they are more complex to retrieve from
    try:
        li_tags = ul_element.find_elements(By.TAG_NAME,'li')
        for li_tag in li_tags:
            manufacturer_name = li_tag.find_element(By.CLASS_NAME,'company-name').text
            manufacturer_link = li_tag.find_element(By.CLASS_NAME,'company-name').get_attribute('href')
            storing_manufacturers_links_into_csv(list_of_variables, manufacturer_name, manufacturer_link, refined_csv_file)
            print(f'{manufacturer_name}\n{manufacturer_link}')
    
    except:
        print("IMAGE")

    # Retrieval 2: Retrieve the manufacturers without images, easier...
    try:
        other_manufacturers = ul_element.find_elements(By.CSS_SELECTOR, '.snc.db')
        for a_tags in other_manufacturers:
            manufacturer_name = a_tags.text
            manufacturer_link = a_tags.get_attribute('href')
            storing_manufacturers_links_into_csv(list_of_variables, manufacturer_name, manufacturer_link, refined_csv_file)
            print(f'{manufacturer_name}\n{manufacturer_link}')

    except:
        print('NO IMAGE')





'''
We will be extracting manufacturers data with the functionality below that links to other functionalities
from other functions. We plan to retrieve their information such as address, phone number, website, and also 
correlate them with their respective spec section.
'''     
def manufacturers_data(csv_file, refined_csv_file):
    
    # Convert the csv into dataframe
    df = pd.read_csv(csv_file)

    # Track the count just in case
    count = 'COMPLETED'

    # Iterate through each manufacturers link
    for index, row in df.iloc[count:].iterrows():

        # Visual Count
        print(f"Iteration {index} out of {len(df)}")
        
        # List of variables for an organized dataframe
        spec_number = row['SpecNumber']
        spec_name = row['SpecName']
        whole_spec = row['EntireSpec']
        spec_link = row['ManufacturersLink']
        dataframe_variables = [spec_number, spec_name, whole_spec, spec_link]

        # Retrieve the data from each individual link
        webscrap_manufacturers_links(dataframe_variables, refined_csv_file)
        

'''
Storing the manufacturers information on a csv file separately from the 
main ones
'''
def manufacturers_attributes_storage(spec_number, spec_name, whole_spec, spec_link, 
    manufacturer_name, manufacturer_link, manufacturer_address, manufacturer_phones, manufacturer_website, csv_file_number):

    df = pd.DataFrame({
        'SpecNumber': [spec_number],
        'SpecName': [spec_name],
        'EntireSpec': [whole_spec],
        'SpecLink': [spec_link],
        'ManufacturerName': [manufacturer_name],
        'ManufacturerLink': [manufacturer_link],
        'ManufacturerAddress':[manufacturer_address],
        'PhoneNumbers':[manufacturer_phones],
        'Website':[manufacturer_website]
    })


    # Allocate into csv file
    df.to_csv(f'manufacturers_attributes/manufacturers_attributes{csv_file_number}.csv', mode='a', index=False, header=False)

'''
Webscraping the manufacturer attributes from each of manufacturer
'''
def webscraping_manufacturer_attributes(index, spec_number, spec_name, whole_spec, spec_link, manufacturer_name, manufacturer_link, csv_file_number):

    # Activate webdriver
    driver = webdriver.Chrome()
    driver.get(manufacturer_link)
    time.sleep(2)

    # Search for the respective attributes
    try:
        # Street Address
        address1_element = driver.find_element(By.XPATH, "//div[@itemprop='streetAddress']")
        address1 = address1_element.text

        # Address Locality
        address2_element = driver.find_element(By.XPATH,"//span[@itemprop='addressLocality']")
        #address3_element = address2_element.find_element(By.TAG_NAME,'span')
        address2 = address2_element.text
        
        # Addres Postal Code
        adress_postal_code_element = driver.find_element(By.XPATH,"//span[@itemprop='postalCode']")
        address_postal_code = adress_postal_code_element.text

        address = f'{address1} {address2} {address_postal_code}'


    # Address is the only attribute that has to be acquired no matter what
    except:
        address = 'none'



    # Search for the phone numbers
    try:
        telephones_list = driver.find_elements(By.XPATH, "//a[@itemprop='telephone']")
        telephone_list_text = [number.text for number in telephones_list]
        telephones = ";".join(telephone_list_text)

    # We continue   
    except:
        telephones = 'none'
    


    # Search for the website link
    try:
        website_element = driver.find_element(By.XPATH, "//a[@itemprop='url']")
        website = website_element.text

    except:
        website = 'none'


    manufacturers_attributes_storage(spec_number, spec_name, whole_spec, spec_link, manufacturer_name, manufacturer_link, address, telephones, website, csv_file_number)
    print(f'Manufacturer #{index}: {manufacturer_name}\nAddress: {address}\nPhone: {telephones}\nWebsite: {website}')

        

    







'''
Acquire the individual data of each manufactuerer, i.e. cell phone number, website,
address, and any other available attribute, right?
Counts: 
    1. Current Count = 13934 (0 - 14914) Computer1 - COMPLETE
    2. Current Count = 25892 (14915 - 29828) Computer1 - COMPLETE
    3. Current Count = 40830 (29829 - 44742) Computer1 - COMPLETE
    4. Current Count = 55722 (44743 - 59656) Computer1 - COMPLETE
    5. Current Count = 61872 (59657 - 74570) Computer2
    6. Current Count = 76761 (74571 - 89484) Computer2
    7. Current Count = 95261 (89485 - 104398) Computer2
    8. Current Count = 106651 (104399 - 119313) Computer2

'''
def manufacturers_attributes(csv_file):
    
    # Import to DataFrame
    df = pd.read_csv(csv_file)

    # Track the count (Total Count: 119314)
    count = 61872
    halt_count = 74570
    #difference = halt_count - count # denominator
    csv_file_number = 5 # CHANGEEEEEEEE
    

    # Iterate through each manufacturer
    for index, row in df.iloc[count:halt_count].iterrows():

        # Percentage visualization
        percentage = round(index/halt_count,4)

        # Visual count
        print(f'Iteration {index} out of {halt_count}: {percentage} Complete')

        # List of variables for an organized dataframe
        spec_number = row['SpecNumber']
        spec_name = row['SpecName']
        whole_spec = row['EntireSpec']
        spec_link = row['ManufacturersLink']
        manufacturer_name = row['ManufacturerName']
        manufacturer_link = row['ManufacturerLink']

        # Webscrap the individual manufacturer attributes
        webscraping_manufacturer_attributes(index, spec_number, spec_name, whole_spec, spec_link, manufacturer_name, manufacturer_link, csv_file_number)


























if __name__ == "__main__":

    # The main url link
    url = 'https://www.arcat.com/content-type/product'
    csv_file = 'manufacturers.csv'
    refined_csv_file = 'manufacturers_refined.csv'

    # (COMPLETED) Step 1): Pinpoint and iterate within the list with all main divisions from the website for further analysis
    # division_links = webscraping_costcodes(url)
    # for division in division_links[3:]:
    #     retrieving_subdivisions(division, csv_file)

    # (COMPLETED) Step 2): Iterate through the list of all links that direct you to the manufacturers, and extract the manufacturer's data
    #manufacturers_data(csv_file, refined_csv_file)

    # Step 3): Iterate through each link of a single manufacturer in order to acquire their attributes
    manufacturers_attributes(refined_csv_file)

          
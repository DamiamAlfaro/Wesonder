import pandas as pd
import requests # type: ignore
from bs4 import BeautifulSoup




'''
Store the manufactuerer's data into and CSV file
'''
def store_into_file(list_of_variables, manufactuerer_attributes, csv_file_in_question):
    df = pd.DataFrame({
        'SpecNumber': [list_of_variables[0]],
        'SpecName': [list_of_variables[1]],
        'EntireSpec': [list_of_variables[2]],
        'SpecLink': [list_of_variables[3]],
        'ManufacturerName': [list_of_variables[4]],
        'ManufacturerLink': [list_of_variables[5]],
        'ManufacturerAddress':[manufactuerer_attributes[0]],
        'PhoneNumbers':[manufactuerer_attributes[1]],
        'Website':[manufactuerer_attributes[2]]
    })

    df.to_csv(csv_file_in_question, mode='a', index=False, header=False)


'''
Extract the desired datums from the manufacturers link from the manufacturers file
'''
def extract_data_from_link(url):
    
    # Cook the stew
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Locate the street variables
    try:
        streetaddress1 = soup.find('div', itemprop='streetAddress').text
        streetaddess2 = soup.find('span',itemprop='addressLocality').text
        postal_code = soup.find('span',itemprop='postalCode').text
        address = f'{streetaddress1} {streetaddess2} {postal_code}'

    except:
        address = 'none'


    # Locate the phone variable
    try:
        phone_numbers = soup.find_all('a', attrs={'itemprop':'telephone'})
        phone_numbers_list = [phone.text for phone in phone_numbers]
        telephones = ";".join(phone_numbers_list)
    
    except:
        telephones = 'none'

    # Locate the Manufacturer's Website
    try:
        website_string = soup.find('a', attrs={'itemprop':'url'}).text
        website = website_string.replace("\n","").replace("\t","").replace(" ","")
    
    except:
        website = 'none'


    return address, telephones, website

'''
Where all the individual manufacturers link are located
'''
def reading_initial_file(csv_file, count, halt, allocation_file):

    # Import as dataframe file
    df = pd.read_csv(csv_file)

    # Iterate, this is where the count comes into place
    for index, row in df.iloc[count:halt].iterrows():

        # Assign variables; they will be needed later
        spec_number = row['SpecNumber']
        spec_name = row['SpecName']
        whole_spec = row['EntireSpec']
        spec_link = row['ManufacturersLink']
        manufacturer_name = row['ManufacturerName']
        manufacturer_link = row['ManufacturerLink']
        list_of_variables = [
            spec_number,
            spec_name,
            whole_spec,
            spec_link,
            manufacturer_name,
            manufacturer_link
        ]

        # Using the link, locate the data, extract it as text, and output it for usage
        manufacturer_data = extract_data_from_link(manufacturer_link)
        
        # Store into CSV
        store_into_file(list_of_variables, manufacturer_data, allocation_file)

        # Confirm appendment 
        print(f'\nManufacturer #{index} appended\nName: {manufacturer_name}\nAddress: {manufacturer_data[0]}\nPhone Numbers: {manufacturer_data[1]}\nWebsite: {manufacturer_data[2]}')
        print(f'Total Completeness: {round((index/halt)*100,4)}%')





'''
Clean the last file from manufacturers without attributes
'''
def cleaning_none_manufacturers(csv_file):
    df = pd.read_csv(csv_file)
    df_cleaned = df[df['ManufacturerAddress'] != 'none']
    df_cleaned.to_csv('all_manufacturers.csv',index=False)





if __name__ == "__main__":
    '''
    Acquire the individual data of each manufactuerer, i.e. cell phone number, website,
    address, and any other available attribute, right?
    Counts: 
        1. Current Count = 13934 (0 - 14914) Computer1 - COMPLETE
        2. Current Count = 25892 (14915 - 29828) Computer1 - COMPLETE
        3. Current Count = 40830 (29829 - 44742) Computer1 - COMPLETE
        4. Current Count = 55722 (44743 - 59656) Computer1 - COMPLETE
        5. Current Count = 74570 (59657 - 74570) Computer2 - COMPLETE
        6. Current Count = 89484 (74571 - 89484) Computer2 - 
        7. Current Count = 104398 (89485 - 104398) Computer2 - COMPLETE
        8. Current Count = 119313 (104399 - 119313) Computer2
    '''
    count = 74570
    halt = 74570
    manufacturers_file = 'manufacturers_refined.csv'

    allocation_file_number = 5
    allocation_file = f'manufacturers_attributes{allocation_file_number}.csv'

    # Read the file above based on the counts
    #reading_initial_file(manufacturers_file, count, halt, allocation_file)

    # Now, as a last step, clear the file of manufacturers from "none", i.e. manufacturers withouth attributes
    final_file = 'manufacturers.csv'
    cleaning_none_manufacturers(final_file)






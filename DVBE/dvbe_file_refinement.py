import pandas as pd




'''
Using the Address Line1, Address Line2, City, State, and Postal code,
we will create a new column containing all those attributes in a single
cell value in order to use that cell value to find the respective geolocation
further on.
'''
def complete_address_column_creation(csv_file):
    
    # Read the file, covert it to a DataFrame using pandas, then locate
    # the five columns that contain the CompleteAddress attribute, concatenate
    # them together, and create a new column containing the result of the
    # adjunction. One can locate the five columns using the itterrows() 
    # functionality which works efficiently for dataframes.

    df = pd.read_csv(csv_file,low_memory=False)
    
    df['CompleteAddress'] = df['CompleteAddress'].astype(str)

    for index, row in df.iterrows():
        
        # This is where we locate each column by pinpointing it using
        # the title of each column respectively. Each column contains an
        # attribute of the complete address.

        address_line1 = str(row['AddressLine1']).title()
        address_line2 = str(row['AddressLine2']).title()
        city = str(row['City']).title()
        state = row['State']

        # Some of the zip codes contain more than five digits, including a
        # '-' character. Let's remove them since they sometimes alter the 
        # posibility of finding the correct address in question.

        zip_code = str(row['PostalCode'])

        if '-' in zip_code:
            zip_code_split = zip_code.split('-')
            zip_code = zip_code_split[0]

        # Some of the columns cells under 'AddressLine2' are empty, therefore
        # useless. We can build a if statement to apply the address line 2 if
        # applicable, and dismiss it if non-applicable.

        if df.isnull().loc[index,'AddressLine2']:
            complete_address = f'{address_line1}, {city}, {state} {zip_code}'
        
        else:
            complete_address = f'{address_line1}, {address_line2}, {city}, {state} {zip_code}'
        
        # Now, it is time to allocate the complete address string into its new
        # column, 'CompleteAddress'. We will do this individually with each of the
        # cells along the dataframe.

        df.at[index,'CompleteAddress'] = complete_address
    
    # Once all the complete addresses have been iterated to their respective column,
    # we need to export the dataframe into a csv file for future usage. After that, we
    # will jump to step 2: Geolocation Acquisition.
    
    df.to_csv('refined_latest_dvbe.csv',index=False)
        













if __name__ == '__main__':
    
    # The goal with this program is to make some adjustments and crucial changes to the
    # csv file that contain all of the dvbe information. So far, I have two goals involving
    # this file in mind: 1) the acquisition of geolocations, and 2) the correlation of 
    # the 'Keywords' column with CSLB license titles via Linguistic Patterns.

    csv_file_dvbe_initial = 'latest_dvbes.csv'
    step = int(input('Step: '))

    match step:

        case 1:
            
            # Step 1: Complete Address Creation, the first step will be creation of a 'CompleteAddress' column. We need to create
            # a column to include the complete addresses. Currently, the addresses are splitted 
            # into 5 columns, we need to put the values of each of those 5 columns into a single
            # column in order for the geofinder to find the geolocation coordinates. After that, 
            # we will output a new file containing such column, in which we will use to find the
            # geolocations directly with.
            
            complete_address_column_creation(csv_file_dvbe_initial)






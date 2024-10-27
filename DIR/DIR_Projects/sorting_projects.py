import pandas as pd  # type: ignore









'''
Cleanse the shit out of the csv file
'''
def cleansing_file(csv_file):
    
    # Convert the csv file into a Pandas Dataframe
    df = pd.read_csv(csv_file)
    df =  df.drop_duplicates()

    # Separate the rows without geolocations
    df_faulty = df[df['X_Coordinates'] != 0]
    df_faulty.to_csv('cleaned_dir_projects.csv',index=False)


'''
Let's clean the main csv file a little bit by removing duplicated rows
'''
def cleaninsing_main_file(main_csv_file):
    
    # Import it as a DataFrame and remove duplicates... Yes, that's it
    df = pd.read_csv(main_csv_file)
    df = df.drop_duplicates()
    df.to_csv('refined_dir_projects_complete.csv',index=False)


'''
Allocate the complete addresses in the main csv file on a new column
in order to facilitate the correlation of geolocations further on
'''
def complete_addresses_allocation(main_csv_file):
    
    # Import as DataFrame
    df = pd.read_csv(main_csv_file, low_memory=False)

    # Allocate the attributes of the complete address
    for index, row in df.iterrows():
        address1 = row['ProjectAddress1']
        address2 = row['ProjectAddress2']
        city = row['City']
        state = row['State']

        # Check if the address is empty, if it is, do not even bother to allocate it
        if pd.isna(address1) or address1.strip() == "":
            continue
        
        else:
            # Create scenarios for when there is an actual address2 line
            if pd.isna(address2) or address2.strip() == "":
                complete_address_string = f"{address1}, {city}, {state}"
            
            else:
                # CompleteAddress string
                complete_address_string = f"{address1} {address2}, {city}, {state}"
        
        # Allocate the complete address string in its respective location
        df.at[index,'CompleteAddress'] = complete_address_string
    
    df.to_csv('refined_dir_projects_projects.csv',index=False)




'''
From the main file, categorize the projects that have addresses with the ones
that do not have addresses in order to make iteration faster, and just have those files
as reference.
'''
def categorizing_addresses(main_csv_file):
    
    # Folder Location of new files
    folder_location = "/Users/damiamalfaro/Desktop/Europe/testing_wesonder/Geolocations_DIR_Projects/"
    
    # Read into DataFrame
    df = pd.read_csv(main_csv_file)
    
    # Categorize non-addresses and addresses projects
    df_no_address = df[df['CompleteAddress'].isnull()]
    df_with_address = df[df['CompleteAddress'].notna()]
    
    # Transcribe to csv file
    df_no_address.to_csv(f'{folder_location}dir_projects_without_addresses.csv',index=False)
    df_with_address.to_csv(f'{folder_location}dir_projects_containing_addresses.csv',index=False)

    
    


'''
Allocate the respective addresses to the respective projects
'''
def allocation_of_geolocations(main_csv_file, geolocations_csv_file,folder_name):
    
    # Import files as dataframes 
    df_main = pd.read_csv(main_csv_file, low_memory=False)
    df_geo = pd.read_csv(geolocations_csv_file)

    # Iterate through the main csv file while correlating the addresses on the geolocation file
    for index, row in df_main.iterrows():
        address = row['CompleteAddress'].title()
        
        # iterate in order to find all geolocations
        for indexb, rowb in df_geo.iterrows():
            if address in rowb['Address'].title():
                x_coordinates = rowb['X_Coordinates']
                y_coordinates = rowb['Y_Coordinates']
                
                df_main.at[index,'X_Coordinates'] = x_coordinates
                df_main.at[index,'Y_Coordinates'] = y_coordinates
                print(f"{address} {x_coordinates} {y_coordinates}")
                break
    
    # Import into csv
    df_main.to_csv(f'{folder_name}dir_projects_mapping.csv',index=False)
                










if __name__ == "__main__":
    
    # Import csv files
    folder_name = '/Users/damiamalfaro/Desktop/Europe/testing_wesonder/Geolocations_DIR_Projects/'
    main_csv_file = f'{folder_name}addresses_dir_projects_complete.csv'
    faulty_csv_file = f'{folder_name}dir_projects_faulty.csv'
    geolocations_file = f'{folder_name}dir_projects_geolocations.csv'
    projects_with_addreses = f'{folder_name}dir_projects_containing_addresses.csv'

    # Clean the DIR Projects Geolocations
    #cleansing_file(faulty_csv_file)

    # Clean the main file
    #cleaninsing_main_file(main_csv_file)

    # Allocate complete addresses in main csv file
    #complete_addresses_allocation(main_csv_file)

    # Categorize the projects with and without addresses to make iteration easier
    #categorizing_addresses(main_csv_file)

    # Allocate the respective geolocations into the addresses
    allocation_of_geolocations(projects_with_addreses,geolocations_file,folder_name)


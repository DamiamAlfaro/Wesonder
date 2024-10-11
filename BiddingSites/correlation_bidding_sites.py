import pandas as pd










'''
Check if all of the awarding bodies are within the website csv file
'''
def appearance_check(csv_file_1, csv_file_2):

    # File 1 is the websites file
    df_websites = pd.read_csv(csv_file_1)

    # File 2 is the awarding bodies file
    df_ab = pd.read_csv(csv_file_2)

    # Check if teh values in df_ab are in df_websites
    df = df_ab['EntityName'].isin(df_websites['AwardingBody'])


    return df


'''
Correlating the links with the respective awarding body
'''
def link_correlation(csv_file_1, csv_file_2):
    # Awarding Bodies websites
    df_websites = pd.read_csv(csv_file_1, on_bad_lines='skip')

    # Awarding bodies list
    df_ab = pd.read_csv(csv_file_2, on_bad_lines='skip')

    # Correlations data
    awarding_bodies_names = []
    row_indexes = []
    website_addresses = []
    website_links = []
    
    # Iterate through every awarding body and find the row indexes, web addresses, and website links
    for index, row in df_ab.iterrows():
        # Assign a variable for the awarding body name
        entity_in_question = row['EntityName']
        awarding_bodies_names.append(entity_in_question)

        # If the awarding body is found within the website dataframe, obtain the desired variables
        if entity_in_question in df_websites['AwardingBody'].values:
            # Create a list of indexes where the awarding body is found
            indexes = df_websites[df_websites['AwardingBody'] == entity_in_question].index.tolist()

            # Initialize lists for storing website addresses and links
            website_addresses_list = []
            website_link_list = []

            # Iterate through the list of indexes and acquire the remaining variables (web addresses and web links)
            for i in indexes:
                website_address = df_websites.at[i, 'BiddingSite']
                website_link = df_websites.at[i, 'SiteLink']

                # To avoid duplicates, check if the site is already in the list
                if website_address not in website_addresses_list:
                    website_addresses_list.append(website_address)
                    website_link_list.append(website_link)

            # Append to the main list
            row_indexes.append(indexes)
            website_addresses.append(website_addresses_list)
            website_links.append(website_link_list)

        else:
            # Append empty lists if no match found
            row_indexes.append([])
            website_addresses.append([])
            website_links.append([])


    # Return all variables
    return awarding_bodies_names, row_indexes, website_addresses, website_links



'''
Before allocating this into a csv file, we need to structure it horizontally.
'''
def horizontal_display_of_data(tuple_with_data):

    # Assign the variables
    names = tuple_with_data[0]
    indexes = tuple_with_data[1]
    web_addresses = tuple_with_data[2]
    web_links = tuple_with_data[3]

    # Create the new dataframe
    df = pd.DataFrame(columns=["AwardingBodyName","WebPages","WebPagesLinks"])

    for index, (name, web_address, web_link) in enumerate(zip(names, web_addresses, web_links)):

        web_addresses_string = ",".join(web_address)
        web_links_string = ",".join(web_link)

        row_data = [name, web_addresses_string, web_links_string]


        df = pd.concat([df, pd.DataFrame([row_data], columns=df.columns)], ignore_index=True)

    df.to_csv("correlation_biddingsites.csv", index=False)

    
       



'''
Correlate the awarding body with the main dataset
'''
def main_correlation(main_csv_file, converted_csv_file):

    # Read the main dataset into a df
    df_main = pd.read_csv(main_csv_file, on_bad_lines='skip', low_memory=False)

    # Read the converted csv file
    df_sites = pd.read_csv(converted_csv_file, on_bad_lines='skip')

    for index, row in df_sites.iterrows():

        # Assign the variables you want to allocate in the main dataset
        awarding_body_name = row['AwardingBodyName']
        web_pages = row['WebPages']
        web_pages_links = row['WebPagesLinks']

        # Iterate through the main dataset to match values
        if awarding_body_name in df_main['EntityName'].values:

            # Get the row index of the main dataset where the match occurs
            row_number = df_main.index.get_loc(df_main[df_main['EntityName'] == awarding_body_name].index[0])

            print(f"{index}: {awarding_body_name} - Row: {row_number}")

            df_main['AwardingBodyName'][row_number] = awarding_body_name
            df_main['WebPages'][row_number] = web_pages
            df_main['WebPagesLinks'][row_number] = web_pages_links


    
    new_refined_df_main = df_main
    new_refined_df_main.to_csv('new_refined_dir_entities.csv',index=False)

    








if __name__ == "__main__":

    # Read the source of websites
    awarding_bodies_websites = '/Users/damiamalfaro/Desktop/Europe/testing_wesonder/BiddingSitesDB/awarding_bodies_bidding_sites.csv'

    # Read the awarding body list
    awarding_bodies_list = "awarding_bodies.csv"

    # Main Dataset
    main_dataset = "/Users/damiamalfaro/Desktop/Europe/testing_wesonder/Geolocations_DIR_Entities/dir_entities_geolocations.csv"

    # Converted csv file
    converted_file = "correlation_biddingsites.csv"

    # Correlate the files and its variables
    #correlation_tuple = link_correlation(awarding_bodies_websites, awarding_bodies_list)

    # Create the new dataframe for further correlation
    #horizontal_display_of_data(correlation_tuple)

    # Main Correlation
    #main_correlation(main_dataset, converted_file)














































































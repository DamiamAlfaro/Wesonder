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
    
    # Iterate through every awarding body and find the row indexes, web addreses, and website links
    for index, row in df_ab.head(10).iterrows():

        # Assign a variable for the awarding body name
        entity_in_question = row['EntityName']
        awarding_bodies_names.append(entity_in_question)
        print(entity_in_question)

        # If the awarding body is found within the website dataframe, obtain the desired variables aforementioned
        if entity_in_question in df_websites['AwardingBody'].values:

            # Creates a list of indexes where the name of the awarding boyd is found, such indexes will be use for identification below
            indexes = df_websites[df_websites['AwardingBody'] == entity_in_question].index.tolist()
            row_indexes.append(indexes)

            # Where the rest of the variables will reside
            website_addresses_list = [] 
            website_link_list = []

            # Iterate through the list of indexes and acquire the remaining variables (web addresses and web links)
            for index in indexes:
                
                # Pinpoint the respective website address and website link based on index
                website_address = df_websites['BiddingSite'][index]
                website_link = df_websites['SiteLink'][index]
                
                # To avoid duplicates, check if the site is already in the list, add bidding site and site link if not
                if website_address not in website_addresses_list:
                    website_addresses_list.append(website_address)
                    website_link_list.append(website_link)

            # Append to the main list
            website_addresses.append(website_addresses_list)
            website_links.append(website_link_list)
            #print(website_addresses_list)
            #print(website_link_list)
            #print(len(website_addresses_list) == len(website_link_list))

        #print("--------------------------------------------")


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
        print(index)
        print(name)
    
        web_addresses_string = ",".join(web_address)
        web_links_string = ",".join(web_link)
        
        print(web_addresses_string)
        print(web_links_string)

        print('=========================================')

        row_data = [name, web_addresses_string, web_links_string]

        df = pd.concat([df, pd.DataFrame([row_data], columns=df.columns)], ignore_index=True)

    df.to_csv("testing.csv", index=False)

       








def convert_to_csv(dataframe):
    pass





if __name__ == "__main__":

    # Read the source of websites
    awarding_bodies_websites = '/Users/damiamalfaro/Desktop/Europe/testing_wesonder/BiddingSitesDB/awarding_bodies_bidding_sites.csv'

    # Read the awarding body list
    awarding_bodies_list = "awarding_bodies.csv"

    # Correlate the files and its variables
    correlation_tuple = link_correlation(awarding_bodies_websites, awarding_bodies_list)

    horizontal_display_of_data(correlation_tuple)
















































































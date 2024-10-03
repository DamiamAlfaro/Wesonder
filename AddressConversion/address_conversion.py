import pandas as pd
from geopy.geocoders import Nominatim


'''
This function converts all addresses into Latitude & Longitude coordinates
that will be used in Leaflet later on.
'''
def cslb_conversion(csv_file):


    
    # Convert the file to a DataFrame
    df = pd.read_csv(csv_file, low_memory=False)

    # Acquire the Address Columns (4-7)
    df_addresses = df.iloc[:, 4:8]

    '''
    Geolocation Conversion and Allocation
    '''

    # Upcoming Columns
    complete_addresses = [] # CompleteAddress
    existence_status = [] # AddressExistence
    coordinates = [] # [X_Coordinates, Y_Coordinates]

    # Iterate through the addreses
    for index, row in df_addresses.head(5).iterrows():

        # Identify the address parts
        street = row['Address']
        city = row['City']
        state = row['State']
        zip_code = row['Zip']

        # Combine the Address' parts to form an entire address
        complete_address = f"{street.title()}, {city.title()}, {state}"

        # Append the complete address for reference
        complete_addresses.append(complete_address)
        print(complete_address)

        # Get the numerical geolocation
        location = geolocator.geocode(complete_address)

        # Where X & Y Coordinates will be allocated
        splited_coordinates = []
        
        # If the address' geolocation is found, append it to the list
        if location:
            x_coordinate = location.latitude
            splited_coordinates.append(x_coordinate)
            y_coordinate = location.longitude
            splited_coordinates.append(y_coordinate)
            existence_status.append(0)
            print(x_coordinate, y_coordinate)
        
        # If not (most likely PO Box) then append counterfeit
        else:
            splited_coordinates.append(0)
            splited_coordinates.append(0)
            existence_status.append(1)
            print("Nonexistent")

        coordinates.append(splited_coordinates)    
        
        # Checks if the folder have the same length, in order to assure organization
        fraudulent_check =  len(complete_addresses) == len(existence_status) == len(coordinates)        
        
        # If it is the same, add it to the DataFrame
        if fraudulent_check == True:
            print("het:")

        else:
            print(f"something happened at {row}")
            break
        
                

        








    return "yes"
    


'''
Here we will write the new 4 columns into the existent csv file
that display whether the address exists or not, if the former, include its
X and Y coordinates, if the latter, nothing.
'''
def address_status_columns_append(dataframe):
    pass





if __name__ == "__main__":

    # Set up the file with addresses
    cslb_contractors_file = "/Users/damiamalfaro/Desktop/Europe/testing_wesonder/testing_allsubs.csv"

    # Set up the geolocator
    geolocator = Nominatim(user_agent="my-app",timeout=20)
    
    # Just for reference, not used
    total_rows = 253006

    # Current count for the thousands, i.e. 1 = 1000
    current_count = 0 

    cslb_conversion(cslb_contractors_file)

    #while current_count != 254
        
        # Display the count
        #print(current_count)

        # Address-Geolocation Conversion
        #cslb_conversion(cslb_contractors_file,current_count)

        # Add to the count after each iteration
        #current_count += 1






























































































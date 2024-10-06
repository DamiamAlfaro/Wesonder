import pandas as pd
from geopy.geocoders import Nominatim


'''
This function converts all addresses into Latitude & Longitude coordinates
that will be used in Leaflet later on.
'''
def cslb_conversion(csv_file, address_file, count):



    # Convert the file to a DataFrame
    df = pd.read_csv(csv_file, low_memory=False)

    # Acquire the Address Columns (4-7)
    df_addresses = df.iloc[:, 23:27]

    '''
    Geolocation Conversion and Allocation
    '''

    # Iterate through the addreses
    for index, row in df_addresses.iloc[count:429916].iterrows():

        # Empty cells check
        if pd.isna(row['ProjectAddress1']) or pd.isna(row['City']) or pd.isna(row['State']):
            continue

        # Situation Awareness
        print(f"Current Count: {index}")

        # Upcoming Columns
        complete_addresses = [] # CompleteAddress
        existence_status = [] # AddressExistence
        x_coordinates = [] # X_Coordinates
        y_coordinates = []

        # Identify the address parts
        street = row['ProjectAddress1']
        street_2 = row.get('ProjectAddress2','')
        city = row['City']
        state = row['State']

        # Combine the addresses if there is a second part of it
        if street_2 and not pd.isna(street_2):
            complete_address = f"{street.title()} {street_2.title()}, {city.title()}, {state}"
        
        # If not, that's even better
        else:
            complete_address = f"{street.title()}, {city.title()}, {state}"


        # Append the complete address for reference
        complete_addresses.append(complete_address)
        print(f"Address: {complete_address}")

        # Get the numerical geolocation
        location = geolocator.geocode(complete_address)

        # If the address' geolocation is found, append it to the list
        if location:
            x_coordinate = location.latitude
            x_coordinates.append(x_coordinate)
            y_coordinate = location.longitude
            y_coordinates.append(y_coordinate)
            existence_status.append(0)
            print("Geolocation: Exists")
            print(f"X-Coordinate: {x_coordinate}")
            print(f"Y-Coordinate: {y_coordinate}")



        # If not (most likely PO Box) then append counterfeit
        else:
            x_coordinates.append(0)
            y_coordinates.append(0)
            existence_status.append(1)
            print("Geolocation: Nonexistent")
            print("X-Coordinate: NA")
            print("Y-Coordinate: NA")


        # Checks if the folder have the same length, in order to assure organization
        fraudulent_check =  len(complete_addresses) == len(existence_status) == len(x_coordinates) == len(y_coordinates)

        # If it is the same, add it to the DataFrame
        if fraudulent_check == True:
            data_to_df = {"CompleteAddress":complete_addresses,
                          "AddressExistence":existence_status,
                          "X_Coordinates":x_coordinates,
                          "Y_Coordinates":y_coordinates}

            # Convert to DataFrame
            df = pd.DataFrame(data_to_df)

            # Allocate to file
            dataframe_to_file(df, address_file)


        else:
            print(f"something happened at {row}")
            break


'''
Here we will write the new 4 columns into the existent csv file
that display whether the address exists or not, if the former, include its
X and Y coordinates, if the latter, nothing.
'''
def dataframe_to_file(dataframe,csv_file):

    # Convert the dataframe to a csv file
    dataframe.to_csv(csv_file, mode="a", header=False, index=False)





if __name__ == "__main__":

    # Source File
    source_contractors_file = "/Users/damiamalfaro/Desktop/Europe/testing_wesonder/dir_projects_complete.csv"

    # Address Conversion File
    address_conversion_file = "/Users/damiamalfaro/Desktop/Europe/testing_wesonder/geolocation_conversion/file_projects_conversion_three.csv"

    # Set up the geolocator
    geolocator = Nominatim(user_agent="my-app",timeout=24)

    # Just for reference, not used
    total_rows = 573220

    # Current count for the thousands, i.e. 1 = 1000
    current_count = 286611

    # Convert the addresses to Geolocations and store them in new csv file for later use
    cslb_conversion(source_contractors_file, address_conversion_file, current_count)























































































































































































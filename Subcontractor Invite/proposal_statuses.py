import pandas as pd
import openpyxl
import os
import numpy as np

'''
Here we will execute the updating of proposal statuses based on
the ContactsSoFar.xlsx file that we have.
'''
def updating_sub_status(excel_file_all_subs):
    df_excel = pd.read_excel(excel_file_all_subs)

    # Ask for Subcontractor Name
    subcontractor_name = input("Looking for: ").upper()

    '''
    First, check if the input string is found as it is; the problem with
    this functionality is that one has to be very specific with the name of
    the entity in order for the entity to be found, which is why we will
    approach what I like to call "fragmentation".
    '''
    sub_row_found_single = df_excel[df_excel.iloc[:,0].str.contains(subcontractor_name,case=False,na=False)]

    print("\n")

    # SubjectiveProjectID Names
    subjective_project_id = df_excel.columns[5:10]
    for subjective_project_id_index, subjective_project_id_column_name in enumerate(subjective_project_id,start=5):
        print(f"{subjective_project_id_index}: {subjective_project_id_column_name}")

    print("\n")

    if not sub_row_found_single.empty:
        matching_sub_name = df_excel.index[df_excel['SubName'].str.contains(subcontractor_name,
                                                                            case=False,na=False)].tolist()
        print(f"Row {matching_sub_name}")
        for found_sub_name_index in matching_sub_name:
            if found_sub_name_index in df_excel.index:
                row_to_print = df_excel.iloc[found_sub_name_index, [0,5,6,7,8,9]]
                print(f"{row_to_print}")
        '''
        Changing the status of a subcontractor based on columns F:ZZZZ,
        which are the columns pertaining to the SubjectiveNameIDs for each
        project.
        '''
        # Ask for SubjectiveProjectID to change (input to be a integer signifying the Column Name)
        halt_signifier = False

        while halt_signifier == False:
            try:
                column_header_index = int(input("\nColumn Index: "))
            except ValueError:
                print("Integer, dumbass...")
                column_header_index = int(input("\nColumn Index: "))
            if 5 <= column_header_index <= 9:
                project_in_question = df_excel.columns[int(column_header_index)]
                print(f"\nCurrent Status: {df_excel.at[matching_sub_name[0],project_in_question]}")
                try:
                    change_status_action = input("\nChange to: ").upper()
                except ValueError:
                    print("String dumbass...")
                if change_status_action == "INVITED" or change_status_action == "DENIED" or change_status_action == "RECEIVED":
                    df_excel.at[matching_sub_name[0],project_in_question] = change_status_action
                    df_excel.to_excel(excel_file_all_subs,index=False)
                elif change_status_action == "":
                    df_excel.at[matching_sub_name[0],project_in_question] = np.nan
                    df_excel.to_excel(excel_file_all_subs,index=False)
                else:
                    print("Wrong Input")
            elif column_header_index == 0:
                print("Nice")
                halt_signifier = True
            elif column_header_index == 1:
                delete_which = int(input("Type Index: "))
                df_excel = df_excel.drop(delete_which)
                df_excel.to_excel(excel_file_all_subs,index=False)
                
            else:
                print("\nWe aren't that far just yet...")
                

'''
We might need to add a new subcontractor, here's the function to do so.
'''
def adding_sub_to_database(excel_file):
    # Open the DataFrame
    df = pd.read_excel(excel_file)

    # Pinpoint the last row available
    latest_row = len(df)

    # The list we will be inputing into the Data Frame
    new_sub_attributes = []

    # SubName
    sub_name = input("SubName: ").upper()
    new_sub_attributes.append(sub_name)

    # SubAddress
    sub_address = input("SubAddress: ").upper()
    new_sub_attributes.append(sub_address)

    # SubEmail
    sub_email = input("SubEmail: ").upper()
    new_sub_attributes.append(sub_email)

    # SubTrait
    sub_trait = input("SubTrait: ").upper()
    new_sub_attributes.append(sub_trait)

    # SubPhoneNumber
    sub_phone_number = input("SubPhoneNumber: ").upper()
    new_sub_attributes.append(sub_phone_number)
    
    for desired_column_index, sub_attribute in enumerate(new_sub_attributes):
        column_name = df.columns[desired_column_index]
        df.at[latest_row,column_name] = sub_attribute

    df.to_excel(excel_file,index=False)

'''
Perhaps, let's create a function that combines the subcontractors sharing
the same name verbatim (let's combine their email address and phone number 
only). This will elimenate the need to update emails or remove rows.
'''
def combining_duplicated_names(excel_file):
    pass
        

'''
ONSET
'''
if __name__ == "__main__":
    # List the indexes of each of the files in the Desktop
    desktop_files = os.listdir()
    for index_file, file_itself in enumerate(desktop_files):
        print(f"{index_file}: {file_itself}")

    # Subcontractor directory
    subcontractor_directory = desktop_files[7]

    # Updating Sub's proposal status
    updating_sub_status(subcontractor_directory)

    # Creating a new Subcontractor row
    adding_sub_to_database(subcontractor_directory)

    # Cleanse the database (one time function)
    combining_duplicated_names(subcontractor_directory)
    

    
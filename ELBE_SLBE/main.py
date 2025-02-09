import fitz  # PyMuPDF
import re
import pandas as pd





# [1.0] Reading and outputing entities and their attributes

def extract_emails_and_names(pdf_path):
    emails = []
    names = []

    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    full_text = ""

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text = page.get_text()
        full_text += text

    # Split entire text by "Phone #"
    text_breakdown = full_text.split("Phone #")

    last_index = len(text_breakdown)-1

    # What we will return
    all_entities = []

    for index, entity_body_string in enumerate(text_breakdown):

        # We need a list like this for the proper entity
        splitted_string = entity_body_string.split('\n')

        if index == 0:
            continue

        name = text_breakdown[index-1].split('\n')[-3]
        email = text_breakdown[index-1].split('\n')[-2]
        splitted_string.insert(0, name)
        splitted_string.insert(1, email)

        # We don't want the document's footer strings in our last entity list
        if index == last_index:
            splitted_string = splitted_string[:-4]
            all_entities.append(splitted_string)

        # We are trying to only get the necessary components based on indexes
        else:

            splitted_string = splitted_string[:-3]

            small_string = 'Small'
            small_indexes = [index for index, value in enumerate(splitted_string) if value == small_string]

            emerging_string = 'Emerging'
            emerging_indexes = [index for index, value in enumerate(splitted_string) if value == emerging_string]   
            
            if small_indexes:
                last_occurrence = small_indexes[-1]
                splitted_string = splitted_string[:last_occurrence]
                splitted_string.append(small_string)

            elif emerging_indexes:
                last_occurrence = emerging_indexes[-1]
                splitted_string = splitted_string[:last_occurrence]
                splitted_string.append(emerging_string)
            


            all_entities.append(splitted_string)



    return all_entities
        



# [2]
def finding_patterns(entities_list):

    count = 0

    entities_all = []

    for index, entity in enumerate(entities_list):

        fax_string_index = [index for index, string in enumerate(entity) if 'Fax #' in string]
        written_services = ",".join(entity[4:fax_string_index[0]])
        new_entity = entity[fax_string_index[0]+3:]
        licenses = ", ".join(list(set(new_entity[::2])))        
    
        entity_attributes = [
            entity[0], # Name
            entity[1], # Email
            entity[2][1:], # Phone Number
            entity[3], # Point of Contact
            written_services, # Written services
            licenses
        ]

        entities_all.append(entity_attributes)

        count += 1


    print(f"\nTotal Entities: {count}")

    return entities_all




# [3]
def csv_allocation(list_of_entities):
    
    headers = [
        "Name",
        "Email",
        "PhoneNumber",
        "POC",
        "Services",
        "Licenses"
    ]

    df = pd.DataFrame(list_of_entities, columns=headers)
    df.to_csv('finalized_slbe_elbe.csv',index=False)

        

'''
FUNCTIONALITY STEPS - Estimated Time (5-10 min): 


[1] Read the pdf and turn it into text, then outputs a list with all of the entities and
their respective attributes serving as the items of the list.

[2] Recognizes the patterns needed to acquire all respective attributes align with their respective title
in order to be tabulated in a dataframe, increasing the data's usability.

[3] Allocate the organized entities into a csv file for export.
'''


# Outset Files
pdf_path = 'slbeapprovednaics.pdf'

# [1]
entities = extract_emails_and_names(pdf_path)

# [2]
all_entities_organized = finding_patterns(entities)

# [3]
csv_allocation(all_entities_organized)











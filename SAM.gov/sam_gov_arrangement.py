import pandas as pd
import time
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys






'''
Using the function below, we will be entering the SAM.gov website in order to check the status
of multiple project types: MACCs, IDIQs, MATOCs, and miscellaneous federal projects. There will
probably be multiple functions associated with each of the project types, but also probably
just one main function.
'''
def entering_the_site(url_site):

    # The first step is to remove the annoying pop-up display as soon as one enters the website,
    # which I assume is implemented to prevent bot attacks, which I mean, we are talking about the
    # U.S. Government, they aren't that smart...

    driver = webdriver.Chrome()
    driver.get(url_site)
    time.sleep(4)

    close_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'close-btn'))
    )
    close_button.click()

    time.sleep(4)
    



'''
The title speaks for itself...
'''    
def csv_file_iteration(csv_file):

    # However, there will be multiple things occurring in this function: within each iteration, we 
    # will collect the respective href attributes for each of the results found in each selenium 
    # session, then, we will store those href values into a list/csv file, and iterate through it. 
    # Using selenium (or if possible, beautiful soup) we will opene each of the url in the list, and
    # extract the attributes of each project: due date, code, location, etc. We will store the 
    # attributes in another list/csv file, then we will find the respective geolocations for each
    # of the projects, and yes, I know we aren't given precise addresses, we will only display either
    # the city, county, or state.

    df = pd.read_csv(csv_file)

    for index, row in df.iterrows():

        url = row['URL']
        entering_the_site(url)








if __name__ == "__main__":

    # The goal of this program is, similar to the real-time display of bids from planetbids, we
    # will do the same but with SAM.gov, however, the new thing here is that there will be
    # multiple categories of projects, i.e. types of searches for types of projects. Change of
    # plans, we will be getting all of the individual type of projects from a csv file. Why?
    # because it is too complex to do selenium movements, this has to be a precise and suttle
    # execution.

    csv_file_with_all_parameters = 'sam_gov_parameters.csv'    

    step = int(input("Step: "))

    match step:

        case 1:

            # Step 1 - SAM.gov Parameter Webscraping: using the csv file above, we will iterate
            # through every single URL row, open it with selenium (maybe even Beautiful soup) and
            # extract the necessary information from each of them.

            csv_file_iteration(csv_file_with_all_parameters)











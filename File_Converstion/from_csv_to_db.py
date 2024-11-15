import pandas as pd # type: ignore
import sqlite3






'''
Convert from .csv to .db
'''
def csv_db_conversion(csv_file, file_theme):

    # Import csv
    df = pd.read_csv(csv_file)

    # Mix in SQLite
    conn = sqlite3.connect(f'{file_theme}.db')
    
    # Convert csv file into sqlite db file
    df.to_sql(f'{file_theme.upper()}', conn, if_exists='replace',index=False)









if __name__ == "__main__":
    
    # Locate the desired files
    projects_file = "/Users/damiamalfaro/Downloads/geolocations_dir_projects.csv"
    enitities_file = "/Users/damiamalfaro/Downloads/new_refined_dir_entities.csv"
    contractors_file = "/Users/damiamalfaro/Downloads/refined_refined_cslb_geolocations.csv"

    # Convert files to .db type
    csv_db_conversion(projects_file, 'projects')
    csv_db_conversion(enitities_file, 'entities')
    csv_db_conversion(contractors_file, 'contractors')


    
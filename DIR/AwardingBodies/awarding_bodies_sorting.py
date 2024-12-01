import pandas as pd





'''
We will sort the entities to solely awarding bodies
since those are the commercial enterprises of our 
interest within that file. Why should we include the 
others if we aren't using them?...
'''
def sorting_awarding_bodies(csv):
    
    # Convert to readable dataframe
    df = pd.read_csv(csv)

    # Segregate Awarding Bodies
    df_ab = df[(df['EntityType'] == "Awarding Body\nType") & (df['AwardingBodyName'].str.strip() != "") & df["AwardingBodyName"].notna()]

    # Drop any duplicates
    df_ab.drop_duplicates()

    # Allocate into new csv file
    df_ab.to_csv("/Users/damiamalfaro/Downloads/other.csv",index=False,header=False)






if __name__ == "__main__":
    
    # Specify the csv location
    csv_file = "/Users/damiamalfaro/Downloads/ultimate_dir_entities.csv"

    sorting_awarding_bodies(csv_file)

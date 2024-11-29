import pandas as pd  # type: ignore




def cleansing_file(csv_file):
    
    df = pd.read_csv(csv_file)
    df_refined = df[df['X_Coordinate'] != 0]

    # New csv
    df_refined.to_csv('/Users/damiamalfaro/Downloads/all_manufacturers.csv',index=False,header=False)















if __name__ == "__main__":
    
    csv_file = "/Users/damiamalfaro/Downloads/ultimate_all_manufacturers.csv"

    cleansing_file(csv_file)

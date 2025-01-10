import pandas as pd
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




def site_html_webscrap(url):

    return url





planetbids_sites_csv = 'https://storage.googleapis.com/wesonder_databases/Planetbids/refined_planetbids_sites.csv'
df = pd.read_csv(planetbids_sites_csv)

for index, row in df.head(1).iterrows():
    
    awarding_body = row['AwardingBody']
    weblink = row['WebLink']
    county = row['County']
    x_coord = row['X_Coordinates']
    y_coord = row['Y_Coordinates']

    html_content = site_html_webscrap(weblink)

    print(html_content)












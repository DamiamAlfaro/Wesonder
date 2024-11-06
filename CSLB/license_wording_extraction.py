import pandas as pd
import time
import sys
import requests  # type: ignore
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from bs4 import BeautifulSoup


'''
Text within each link has to be accessed and mapped somewhere
'''
def text_extraction_c(link):
    
    # Cook the stew mon ami, and cook it fast mate.
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Locate the desired class
    paragraph_class = soup.find(class_="main-primary")
    paragraph_subclass = paragraph_class.find(class_="section")
    paragraphs = paragraph_subclass.find_all('p')
    print(paragraphs[1:-1])
    
'''
Text within each link has to be accessed and mapped somewhere
'''
def text_extraction_d(list_of_links, license_names):
    pass




'''
Extract individual links for each license from the D department
'''
def license_d_extraction(definitive_url):

    # URL response
    driver = webdriver.Chrome()
    driver.get(definitive_url)
    time.sleep(2)

    # Links to access
    links = []
    license_names = []

    # Locate the individual license links
    list_with_licenses = driver.find_element(By.CLASS_NAME, 'list-understated')
    li_tags = list_with_licenses.find_elements(By.TAG_NAME, 'li')
    for li_tag in li_tags:
        license_names.append(li_tag.text)
        a_tag = li_tag.find_elements(By.TAG_NAME,'a')

        # Since some include two or more licenses, we extract their links as well
        sub_links = []

        for href_attribute in a_tag:
            link_pair = href_attribute.get_attribute('href')
            sub_links.append(link_pair)
    
        links.append(sub_links)

    return links, license_names


'''
Extract individual links for each license from the C department
'''
def license_c_extraction(definitive_url):

    # URL response
    driver = webdriver.Chrome()
    driver.get(definitive_url)
    time.sleep(2)

    # Links to access
    links = []
    license_names = []

    # Locate the individual license links
    list_with_licenses = driver.find_element(By.CLASS_NAME, 'list-understated')
    li_tags = list_with_licenses.find_elements(By.TAG_NAME, 'li')
    for li_tag in li_tags:
        a_tag = li_tag.find_element(By.TAG_NAME,'a')
        license_link = a_tag.get_attribute('href')

        # Skip the C-61 section as we are doing it above
        if 'C-61' not in license_link:
            links.append(license_link)
            license_names.append(li_tag.text)

    driver.quit()

    # Iterate through each link
    for individual_link, individual_name in zip(links, license_names):
        text_extraction_c(individual_link)
        



if __name__ == "__main__":
    
    # Important links you know...
    url_c_licenses = "https://www.cslb.ca.gov/about_us/library/licensing_classifications/"
    url_d_licenses = "https://www.cslb.ca.gov/about_us/library/licensing_classifications/C-61_Limited_Speciality/Default.aspx"

    # Acquire each links and text first
    c_licenses = license_c_extraction(url_c_licenses)
    #d_licenses = license_d_extraction(url_d_licenses)

    # Allocate information into csv file
    #allocate_to_csv(c_licenses, d_licenses)

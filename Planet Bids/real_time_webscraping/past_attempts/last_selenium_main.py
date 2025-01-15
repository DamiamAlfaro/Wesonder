import pandas as pd
import time
import re
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("This working?")

# Configure Chrome options for headless mode
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--no-sandbox")  # Required for Docker
options.add_argument("--disable-dev-shm-usage")  # Prevent shared memory issues
options.add_argument("--disable-gpu")  # Disable GPU acceleration
options.add_argument("--disable-crash-reporter")  # Disable crash reporter
options.add_argument("--disable-extensions")  # Disable extensions
options.add_argument("--disable-in-process-stack-traces")  # Simplify stack traces
options.add_argument("--disable-logging")  # Disable logging
options.add_argument("--disable-dev-shm-usage")  # Disable /dev/shm usage
options.add_argument("--disable-default-apps")  # Disable default apps
options.add_argument("--disable-popup-blocking")  # Disable popup blocking
options.add_argument("--window-size=1920,1080")  # Set window size (useful for screenshots)

# Initialize WebDriver
driver = webdriver.Chrome(options=options)
driver.get("https://example.com")

# Print the page title
print(driver.title)

# Quit the driver
driver.quit()

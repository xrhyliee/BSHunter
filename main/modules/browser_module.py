from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def setup_driver() -> webdriver.Chrome:

    # create chrome options
    chrome_options = ChromeOptions()

    # add headless option (no visible browser window)
    chrome_options.add_argument("--headless")

    # disable images to optimize page loading
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")

    # set user agent to mimic a real browser
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

    # disable popups and notifications
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")

    # initialize the driver and set to wait for elements to load
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)

    print(f"Driver setup complete. Let er rip.")
    return driver

# STOPPED HERE; TODO add functions for navigating searching hashtags, extracting post data, and looping through posts and comments.






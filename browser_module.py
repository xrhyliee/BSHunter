from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# this initializes the selenium driver with the
# necessary options for optimized scraping

def setup_driver() -> webdriver.Chrome:

    # create chrome options
    chrome_options = ChromeOptions()

    # add headless option (no visible browser window)
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

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

# this function will navigate to the specified hashtag page and scrape through the posts,
# extracting post urls, captions, and other relevant data.
# this is essentially the same thing as going to the hashtag page yourself
# and copy and pasting every post into a notepad, except less tedious

def search_hashtag(driver: webdriver.Chrome, hashtag: str) -> None:
    url = f"https://www.instagram.com/explore/tags/{hashtag}/"

    try:
        driver.get(url)

        # wait for post grid to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'article'))
        )

        print(f"Explore page loaded for #{hashtag}. Starting to scrape posts...")

    except Exception as e:
        print(f"Uh oh. There was an error navigating to the hashtag page {e}.")
        print(f"Double-check your spelling and try again next")
        raise(f"If this issue persists, text/email Rhylie or open an issue on GitHub.")

def wait_and_scroll(driver: webdriver.Chrome, max_scrolls: int = 5) -> None:

    # scrolls down the page to load more posts,
    # waits for new posts to load, and repeats until max scrolls is reached
    # this simulates the user behavior of scrolling through the hashtag page

    try: 
        for scroll_count in range(max_scrolls):

            # execute JavaScript (barf) to scroll down the page
            driver.execute_script("window.scrollTo(0, window.innerHeight);")

            print(f"Scrolled down {scroll_count + 1}/{max_scrolls}. Waiting for new posts to load...")

            # wait for new posts to load
            time.sleep(3)

        print(f"Finished scrolling.")

    except Exception as e:
        print(f"Uh oh. There was an error while scrolling {e}")
        print(f"This could be because of Instagram's anti-scraping API. (bastards)")
        print(f"Try running the actor again, and if the issue persists, text/email Rhylie or open an issue on GitHub.")

def get_page_html(driver: webdriver.Chrome) -> str:

    try:
        html = driver.page_source
        print(f"Successfully extracted page HTML consisting of {len(html)} characters.")
        return html
    
    except Exception as e:
        print(f"There was an error extracting the HTML data associated with this page: {e}")
        print(f"Try running the actor again, and if the issue persists, text/email Rhylie or open an issue on GitHub.")
        raise

def close_driver(driver: webdriver.Chrome) -> None:
    # safely closes the driver

    try: 
        driver.quit()
        print(f"Driver closed successfully!! Always good when nothing explodes.")

    except Exception as e:
        print(f"There was an error closing the driver...")
        print(f"Something is DEFINITELY wrong, so please either text/email Rhylie or open an issue on GitHub.")
        raise

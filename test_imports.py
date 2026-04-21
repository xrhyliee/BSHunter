
import sys
import os

# Add main directory to path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'main'))

print("Testing imports...\n")

try:
    print("Importing browser_module...")
    from modules.browser_module import setup_driver, search_hashtag, wait_and_scroll, get_page_html, close_driver
    
    print("Importing post_scraper...")
    from modules.post_scraper import scrape_feed_posts
    
    print("Importing post_details...")
    from modules.post_details import get_post_details
    
    print("Importing data_parser...")
    from modules.data_parser import process_all_posts
    
    print("\nAll imports successful!")
    print("\nAvailable functions:")
    print("  - setup_driver()")
    print("  - search_hashtag(driver, hashtag)")
    print("  - wait_and_scroll(driver, max_scrolls, wait_time)")
    print("  - get_page_html(driver)")
    print("  - close_driver(driver)")
    print("  - scrape_feed_posts(html)")
    print("  - get_post_details(post_url, max_comments)")
    print("  - process_all_posts(raw_posts)")
    
except ImportError as e:
    print(f"\nImport Error: {e}")
    print("\nMake sure all module files exist:")
    print("  - main/modules/browser_module.py")
    print("  - main/modules/post_scraper.py")
    print("  - main/modules/post_details.py")
    print("  - main/modules/data_parser.py")
    sys.exit(1)

except Exception as e:
    print(f"\nUnexpected Error: {e}")
    print(f"\nSomething is definitely wrong here. Please email/text Rhylie or open an issue on GitHub.")
    sys.exit(1)

from apify import Actor, Event
from apify_client import ApifyClient
from bs4 import BeautifulSoup
from instagramproperties.instaproperties import extract_insta_desc, extract_insta_username, extract_posts, extract_specified_hashtags
from crawlee.crawlers import PlaywrightCrawler
import asyncio
import csv
from datetime import datetime
import sys

class InstagramScraper:
    def __init__(self, urls, target_hashtags=None):
        self.urls = urls
        self.target_hashtags = target_hashtags or []
        self.client = ApifyClient()
        self.scraped_data = []
    
    async def scrape(self):
        async with PlaywrightCrawler() as crawler:
            for url in self.urls:
                response = await crawler.crawl(url)
                if response.status_code == 200:
                    hashtags = extract_specified_hashtags(response.text, self.target_hashtags)
                    posts = extract_posts(response.text) 
                    username = extract_insta_username(response.text)
                    description = extract_insta_desc(response.text)
                    for post in posts:
                        self.scraped_data.append({
                            "username": username,
                            "description": description,
                            "post_caption": post.get("caption"),
                            "likes": post.get("likes"),
                            "image": post.get("image"),
                            "hashtags": ",".join(hashtags),
                            "url": url
                        })
        print(f"Found {len(self.scraped_data)} posts! Exporting to CSV. :O")
        self.export_to_csv()

    def export_to_csv(self, filename=None):
        if not filename:
            filename = f"BS_scrape_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        if not self.scraped_data:
            print("No posts found. :( Please double-check your spelling and try again!")
            return

        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ["username", "description", "post_caption", "likes", "image", "hashtags", "url"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.scraped_data)
            print(f"Data has been exported to {filename}! Please ask Rhylie or open an issue on Github if you have any questions. :)")
        except Exception as e:
            print(f"An error occurred while exporting CSV: {e} Please open an issue on Github or text Rhylie because they DEFINITELY broke something...")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("To use this program, use it as such: python src.py <url1>")

"""stopped here; 11/03/26. i need to study physics...."""
from apify import Actor
import asyncio
import os
from dotenv import load_dotenv

# CUSTOM MODULE IMPORTS BEGIN HERE

from browser_module import setup_driver, search_hashtag, wait_and_scroll, get_page_html, close_driver
from post_scraper import scrape_feed_posts
from post_details import get_post_details
from data_parser import process_all_posts

load_dotenv()

TOKEN = os.getenv('APIFY_API_TOKEN')

async def main() -> None:

    async with Actor:
        actor_input = await Actor.get_input()

        # validate input, if not valid, throw and log error, then abort
        if not actor_input:
            Actor.log.error("Bro literally just activated the actor without any input... dawg are we fr?")
            await Actor.exit()

        # extract input params
        username = actor_input.get("username")
        hashtags = actor_input.get("hashtags", [])
        max_posts = actor_input.get("maxPostsPerHashtag", 10)
        max_comments = actor_input.get("maxCommentsPerPost", 5)
        max_scrolls = actor_input.get("maxScrolls", 5)

        # log configuration
        Actor.log.info(f"Let's find some BS!")
        Actor.log.info(f"Username: {username}")
        Actor.log.info(f"Hashtags: {hashtags}")
        Actor.log.info(f"Max Posts per Hashtag: {max_posts}")
        Actor.log.info(f"Max Comments per Post: {max_comments}")

        # PHASE 2: browser automation to scrape post data 
        Actor.log.info("Initializing Chrome driver using Selenium...")
        try:
            driver = setup_driver()
        except Exception as e:
            Actor.log.error(f"Failed to initialize driver: {e}")
            Actor.log.error("There's definitely a problem here. Please open an issue on GitHub or call/text Rhylie.")
            await Actor.exit()

        all_posts_data = []

        # main loop will go here for processing each hashtag
        try:
            for hashtag in hashtags:
                hashtag = hashtag.lstrip("#").strip()  # sanitize hashtag input
                if not hashtag:
                    Actor.log.warning(f"Skipping empty hashtag entry.")
                    continue
                Actor.log.info(f"\n=== Scraping hashtag: #{hashtag} ===\n")

                try: 
                    # navigate to hashtag and scroll to load posts (like you would)
                    search_hashtag(driver, hashtag)
                    wait_and_scroll(driver, max_scrolls=max_scrolls)

                    # phase 3: extract post URLs and metadata from feed
                    html = get_page_html(driver)
                    feed_posts = scrape_feed_posts(html)
                    Actor.log.info(f"Found {len(feed_posts)} posts in feed for #{hashtag}")

                    # limit to max posts per hashtag so we dont kill our program
                    feed_posts = feed_posts[:max_posts]

                    # phase 3b: fetch individual post details 
                    Actor.log.info(f"Fetching details for {len(feed_posts)} posts...")
                    
                    for idx, post in enumerate(feed_posts):
                        try:
                            post_url = post.get('post_url')
                            if not post_url:
                                Actor.log.warning(f"Skipping post. No valid URL found.")
                                continue

                            Actor.log.info(f"Fetching post {idx + 1}/{len(feed_posts)}: {post_url}")

                            # get full details of the post (caption, likes, comments, etc)
                            post_details = get_post_details(post_url, max_comments)

                            # merge feed daata with details
                            merged_post = {**post, **post_details}
                            all_posts_data.append(merged_post)
                        
                        except Exception as e:
                            Actor.log.warning(f"Error processing post: {e}")
                            continue

                except Exception as e:
                    Actor.log.error(f"Error processing hashtag #{hashtag}: {e}")
                    continue

        finally:
            # always close the driver
            Actor.log.info("Closing down Chrome driver...")
            close_driver(driver)

        # phase 4: normalize and validate data
        Actor.log.info(f"\nProcessing {len(all_posts_data)} posts for normalization...")
        normalized_posts = process_all_posts(all_posts_data)

        # output to apify dataset
        Actor.log.info(f"Pushing {len(normalized_posts)} posts to Apify dataset, this might take a bit...")

        dataset = await Actor.open_dataset()

        for post in normalized_posts:
            try:
                await dataset.push_data(post)
            except Exception as e:
                Actor.log.error(f"Error pushing data to dataset: {e}")
                Actor.log.error("Something is DEFINITELY wrong here. Please text/email Rhylie, or open an issue in GitHub.")

        Actor.log.info(f"\nScraping Complete!")
        Actor.log.info(f"Total posts scraped: {len(normalized_posts)}")
        Actor.log.info(f"All done! Please make sure you double-check your results to make sure everything lines up!")


if __name__ == "__main__":
    asyncio.run(main())


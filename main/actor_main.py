from apify import Actor
import asyncio
import os
from dotenv import load_dotenv

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

    Actor.log.info(f"Let's find some BS!")
    Actor.log.info(f"Username: {username}")
    Actor.log.info(f"Hashtags: {hashtags}")
    Actor.log.info(f"Max Posts per Hashtag: {max_posts}")
    Actor.log.info(f"Max Comments per Post: {max_comments}")

    # import and call browser module, post scraper, and data parser

    Actor.log.info("Done! Make sure you double check your results to make sure this is what you wanted!")

if __name__ == "__main__":
    asyncio.run(main())

# STOPPED HERE; SEE browser_module.py FOR TODO
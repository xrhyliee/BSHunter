from apify import Actor, Event
from apify_client import ApifyClient
from apify_client.async_client import ApifyClientAsync
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os


TOKEN = 'MY_APIFY_TOKEN'

async def main() -> None:
    apify_client = ApifyClientAsync(TOKEN)
    actor_client = apify_client.actor('BSHunter')
    call_result = await actor_client.call()

    if call_result is None:
        print("No data was retrieved from the actor. Check your token and actor name, then try again.")
        return
    
    dataset_client = apify_client.dataset(call_result.default_dataset_id)
    list_items_result = await dataset_client.list_items()
    print(f'Dataset: {list_items_result}')

run_input = {
    "directURLs": ["https://www.instagram.com/clemsontigers/"],
    "resultsType": "posts",
    "resultsLimit": 200,
    "onlyPostsNewerThan": None,
    "search": None,
    "searchType": "hashtag",
    "addParentData": False,
    }

run = client.actor('BSHunter').call(run_input=run_input) 

for item in client.dataset(run['defaultDatasetId']).iterate_items():
    print(item)
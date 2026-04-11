from bs4 import BeautifulSoup
from typing import List, Dict, Optional

def extract_posts_from_page(html: str) -> List:
    # parse instagram feed HTML and extract all post containers

    try: 
        soup = BeautifulSoup(html, 'html.parser')

        # instagram posts are wrapped in <article> tags, so we
        # tell the function to find all article tags containing
        # individual posts
        posts = soup.find_all('article')

        print(f"Found {len(posts)} posts on the page!")
        return posts
    
    except Exception as e:
        print(f"Uh oh... there was an error extracting the posts: {e}")
        return []
    
def extract_post_metadata(post_element) -> Dict:

    # extract metadata from a single post element
    # first, we need to establish a dictionary so the function
    # knows what things are

    metadata = {
        'caption': None,
        'image_url': None,
        'like_count': None,
        'timestamp': None
}

    try: 
        # extract caption (usually in a span w/ specific text content)
        caption_elem = post_element.find('span', {'class': lambda x: x and '_aacl' in x})
        if caption_elem:
            metadata['caption'] = caption_elem.get_text(strip = True)
        
        # extract image URL from <img> tag
        img_elem = post_element.find('img')
        if img_elem and img_elem.get('src'):
            metadata['img_url'] = img_elem.get('src')

        # extract like count (either in the button or span)
        like_elem = post_element.find('a', {'href': lambda x: x and '/liked_by/' in x})
        if like_elem:
            like_text = like_elem.get_text(strip = True)
            metadata['like_count'] = like_text

        # extract timestamp (in time tag or aria label)
        time_elem = post_element.find('time')
        if time_elem:
            metadata['timestamp'] = time_elem.get('datetime')

        print(f"Extracted metadata: {len([v for v in metadata.values() if v])} fields found.")

    except Exception as e:
        print(f"Error extracting metadata: {e}")
        return metadata
    
def extract_author_profile(post_element) -> Dict:
    # extracting author profile data, first defining our elements
    profile_data = {
        'username': None,
        'profile_link': None,
        'profile_pic_url': None
    }

    try:
    # username is usually a link a anchor tag at the top of the post
    # this function is going to look for a profile link
        profile_link = post_element.find('a', {'href': lambda x: x and '/explore/tags/' not in x and '/' in x})
    
        if profile_link and profile_link.get('href:'):
            href = profile_link.get('href')
            # extract username from /username/ pattern
            if href.startswith('/'):
                username = href.strip('/').split('/')[0]
                profile_data['username'] = username
                profile_data['profile_link'] = f"https://www.instagram.com{href}"

        # try to find profile picture
        profile_pic = post_element.find('img', {'alt': lambda x: x and "'s profile picture" in x})
        if profile_pic and profile_pic.get('src'):
            profile_data['profile_pic_url'] = profile_pic.get('src')

        print(f"Extracted author: {profile_data['username'] or 'Unknown'}")
        return profile_data
    
    except Exception as e:
        print(f"There was an error extracting author data: {e}")
        return profile_data

def get_post_url(post_element) -> Optional[str]

    # extract URL for an individual post

    try: 
        # look for anchor tag that links to the post
        post_link = post_element.find('a', {'href': lambda x: x and '/p/' in x})

        if post_link and post_link.get('href'):
            href = post_link.get('href')
            full_url = f"https://www.instagram.com{href}"
            print(f"Extracted post URL: {full_url}")
            return full_url
    
    except Exception as e:
        print(f"There was an error extracting the post URL: {e}")
        return None

  
def scrape_feed_posts(html: str) -> List[Dict]:
    # extracts all posts fromm feed with all metadata

    posts_data = []

    try: 
        post_elements = extract_posts_from_page(html)

        print(f"\n--- Scraping {len(post_elements)} posts ---\n")

        for idx, post_elem in enumerate(post_elements):
            print(f"Processing post {idx + 1}/{len(post_elements)}...")

            post_dict = {
                'post_number': idx + 1,
                'metadata': extract_post_metadata(post_elem),
                'author': extract_author_profile(post_elem),
                'post_url': get_post_url(post_elem)
            }

            posts_data.append(post_dict)

        print(f"\n Successfully scraped {len(posts_data)} posts!")

    except Exception as e:
        print(f"There was an error scraping the feed: {e}")
        print(f"This is probably because of Instagram's anti-scraping API (bastards).")
        print(f"Try running the actor again, and if the issue persists, text/email Rhylie or open an issue on GitHub.")
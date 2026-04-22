from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import requests
import time

def fetch_post_page(post_url: str, delay: float = 1.5) -> Optional[str]:
	
    # wait before making request (rate limiting)
    time.sleep(delay)

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(post_url, headers = headers, timeout = 10)

        response.raise_for_status()

        print(f"Fetched post: {post_url}")
        return response.text
    
    except requests.exceptions.RequestException as e:
        print(f"There was an error attempting to fetch the post url. {e}")
        return None

    
def extract_all_likes(html: str) -> Optional[int]:
    try:
        soup = BeautifulSoup(html, 'html.parser')

        like_elem = soup.find('a', {'href': lambda x: x and '/liked_by/' in x})

        if like_elem:
            like_text = like_elem.get_text(strip = True)

            like_count = parse_like_count(like_text)

            if like_count is not None:
                print(f"Extracted likes: {like_count}")
                return like_count
            
        print(f"Like count not found.")
        return None
    
    except Exception as e:
        print(f"Error extracting likes: {e}")
        return None
    
def parse_like_count(like_text: str) -> Optional[int]:
    try:
        like_text = like_text.strip()

        # handle 'K' notation (1.5K = 1,500)
        if 'K' in like_text.upper():
            number = float(like_text.upper().replace('K', ''))
            return int(number * 1000)
        
        # handle 'M' notation (1.0M = 1,000,000)
        if 'M' in like_text.upper():
            number = float(like_text.upper().replace('M', ''))
            return int(number * 1000000)
        
        # removes commas and converts to list
        like_count = int(like_text.replace(',', ''))
        return like_count
    
    except ValueError:
        return None

def extract_post_caption_full(html: str) -> Optional[str]:

    try:
        soup = BeautifulSoup(html, 'html.parser')

        caption_elem = soup.find('h1', {'class': lambda x: x and '_aacl' in x})

        if not caption_elem:
            caption_elem = soup.find('span', {'class': lambda x: x and '_aacl' in x})

        if caption_elem:
            caption_text = caption_elem.get_text(strip = True)
            print(f"Extracted caption: {caption_text[:50]}...")
            return caption_text
        
    except Exception as e:
        print(f"There was an error extracting the caption: {e}")
        return None

def extract_comments(html: str, max_count: int = 5) -> List[Dict]:
    """
    Extract top N comments from a post page.
    
    Args:
        html (str): HTML from individual post page
        max_count (int): Maximum number of comments to extract (default: 5)
        
    Returns:
        List[Dict]: List of comment dictionaries with:
            - 'author': Username who commented
            - 'text': Comment text
            - 'likes': Number of likes on comment
            - 'timestamp': When comment was posted
    """
    comments_list = []

    try:
        soup = BeautifulSoup(html, 'html.parser')

        comments_section = soup.find('ul', {'class': lambda x: x and '_acnb' in x})

        if not comments_section:
            comments_section = soup.find('ul', {'role': 'presentation'})
        
        if not comments_section:
            print(f"Couldn't find the comments section.")
            print(f"This is probably becuase the post author either limited or turned off comments.")
            return comments_list
        
        comment_items = comments_section.find_all('li', limit = max_count)

        print(f"Found {len(comment_items)} comments (max: {max_count})")

        for idx, comment_item in enumerate(comment_items):

            comment_dict = {
                'author': None,
                'text': None,
                'likes': None,
                'timestamp': None
            }

            try:
                # extract author username
                author_link = comment_item.find('a', {'title': lambda x: x is not None})
                if author_link:
                    comment_dict['author'] = author_link.get_text(strip = True)

                # extract comment text
                text_elem = comment_item.find('span', {'class': lambda x: x and '_aacl' in x})
                if text_elem:
                    comment_dict['text'] = text_elem.get_text(strip = True)

                # extract comment likes (if presesnt)
                like_button = comment_item.find('button', {'aria-label': lambda x: x and 'like' in x.lower()})
                if like_button:
                    like_text = like_button.get_text(strip = True)
                    comment_dict['likes'] = parse_like_count(like_text)

                # extract timestamp 
                time_link = comment_item.find('a', {'class': lambda x: x and '_aacl' in x})
                if time_link:
                    comment_dict['timestamp'] = time_link.get_text(strip = True)

                comments_list.append(comment_dict)
                print(f"Extracted comment {idx + 1}: @{comment_dict['author']}")

            except Exception as e:
                print(f"Error parsing comment {idx + 1}: {e}")
                continue

        print(f"Extracted {len(comments_list)} comments.")

    except Exception as e:
        print(f"There was an error when attempting to extract the comments: {e}")
        print("This might be because the author has their comments turned off or limited... nothing we can really do about that unfortunately.")
    
    return comments_list

def extract_profile_data(html: str, username: str) -> Dict:
    # extracts the profile information: such as username, bio, followers, and following, posts, and profile picture

    profile_data = {
        'username': username,
        'bio': None,
        'followers': None,
        'following': None,
        'posts': None,
        'profile_pic_url': None
    }

    try: 
        soup = BeautifulSoup(html, 'html.parser')

        profile_pic = soup.find('img', {'alt': lambda x: x and username in x})
        if profile_pic and profile_pic.get('src'):
            profile_data['profile_pic_url'] = profile_pic.get('src')

        # bio and stats are typically on the profile page, not post page
        # note this needs a separate page 
        print(f"Heads up: full profile data requires visiting the actual profile page.")
        print(f"Profile data extracted for: {username}.")

        return profile_data
    
    except Exception as e:
        print(f"There was an issue extracting profile data... {e}")
        print(f"This might be because the user has their profile set to private...")
        print(f"Nothing much can be done about that, unfortunately.")
        return profile_data 

def get_post_details(post_url: str, max_comments: int = 5) -> Dict:

    post_details = {
        'url': post_url,
        'caption': None,
        'likes': None,
        'comments': [],
        'author': None
    }
    
    try:
        # fetch post page
        html = fetch_post_page(post_url)

        if not html:
            print(f"Could not fetch post details.")
            return post_details
        
        post_details['caption'] = extract_post_caption_full(html)
        post_details['likes'] = extract_all_likes(html)
        post_details['comments'] = extract_comments(html, max_comments)

        print(f"Post details have been extracted successfully!\n")
        return post_details
    
    except Exception as e:
        print(f"There was an error getting post details: {e}")
        return post_details

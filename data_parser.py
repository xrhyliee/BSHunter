from typing import Dict, List, Optional
from datetime import datetime
import json

def normalize_post(raw_post_data: Dict) -> Dict:

    try: 
        author_data = raw_post_data.get('author', {})
        if isinstance(author_data, dict):
            username = author_data.get('username')
        else:
            username = str(author_data)

        metadata = raw_post_data.get('metadata', {})
        if not isinstance(metadata, dict):
            metadata = {}

        # normalize timestamp to iso format [YYYY-MM-DDTHH:MM:SSZ]
        timestamp = parse_datetime(metadata.get('timestamp'))
        
        # normalize like count to integer
        like_count = normalize_like_count(metadata.get('like_count'))

        # normalize comments
        raw_comments = raw_post_data.get('comments', [])
        normalized_comments = [normalize_comment(c) for c in raw_comments]

        # build normalized post
        normalized = {
            'username': username or 'Unknown',
            'caption': metadata.get('caption') or None,
            'post_url': raw_post_data.get('post_url') or raw_post_data.get('url'),
            'image_url': metadata.get('image_url') or None,
            'like_count': like_count,
            'comment_count': len(normalized_comments),
            'comments': normalized_comments,
            'timestamp': timestamp,
            'scraped_at': datetime.utcnow().isoformat() + 'Z'
        }

        print(f"Normalized post from @{username}.")
        return normalized
    
    except Exception as e:
        print(f"There was an issue normalizing the post: {e}")
        return {
            'username': 'Error',
            'caption': None,
            'post_url': None,
            'image_url': None,
            'like_count': 0,
            'comment_count': 0,
            'comments': [],
            'timestamp': None,
            'scraped_at': datetime.utcnow().isoformat() + 'Z'
        }
    
# normalize comment data, standardizing into a consistent format

def normalize_comment(raw_comment: Dict) -> Dict:
    
    try:
        #first, ensure we have a dict
        if not isinstance(raw_comment, dict):
            return {
                'author' : 'Unknown',
                'text': 'Error parsing comment',
                'likes': 0,
                'timestamp': None
            }
        
        normalized = {
            'author': raw_comment.get('author') or 'Unknown',
            'text': raw_comment.get('text') or '',
            'likes': normalize_like_count(raw_comment.get('likes')),
            'timestamp': parse_datetime(raw_comment.get('timestamp'))
        }

        return normalized
    
    except Exception as e:
        print(f"Error normalizing comment: {e}")
        return {
            'author': 'Unknown',
            'text': 'Error parsing comment',
            'likes': 0,
            'timestamp': None
        }
    
def normalize_profile(raw_profile: Dict, username: str) -> Dict:
    # flatten and standardize profile data

    try: 
        if not isinstance(raw_profile, dict):
            raw_profile = {}

        normalized = {
            'username': username,
            'bio': raw_profile.get('bio') or '',
            'followers': normalize_like_count(raw_profile.get('followers')),
            'following': normalize_like_count(raw_profile.get('following')),
            'post_count': normalize_like_count(raw_profile.get('posts')),
            'profile_pic_url': raw_profile.get('profile_pic_url') or None
        }

        print(f"Normalized profile data for @{username}.")
        return normalized
    
    except Exception as e:
        print(f"There was an issue normalizing profile data for @{username}: {e}")
        return {
            'username': username,
            'bio': '',
            'followers': 0,
            'following': 0,
            'post_count': 0,
            'profile_pic_url': None
        }
    
def normalize_like_count(value) -> int:

    # convert like count to integer if it isnt already

    try:
        # if the value is already an integer
        if isinstance(value, int):
            return value
        
        # if not an integer or empty
        if value is None or value == '':
            return 0
        
        # convert to string
        value_str = str(value).strip().upper()

        # handle k format (10k, 1k, etc)
        if 'K' in value_str:
            number = float(value_str.replace('K', ''))
            return int(number * 1000)
        
        # handle m format (1M, 10M, etc)
        if 'M' in value_str:
            number = float(value_str.replace('M', ''))
            return int(number * 1000000)
        
        # remove commas and convert to int
        return int(value_str.replace(',',''))
    
    except (ValueError, TypeError):
        return 0
    
def parse_datetime(date_string) -> Optional[str]:
    # parse date and time formats and return iso format string

    if not date_string or date_string == '':
        return None
    
    try:
        # if already in iso format, then return as is
        if isinstance(date_string, str) and 'T' in date_string and 'Z' in date_string:
            return date_string
        
        # try and parse iso format
        if isinstance(date_string, str) and 'T' in date_string:
            dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            return dt.isoformat().replace('+00:00', 'Z')
        
        # for relative time (i.e. "2 hours ago"), we can't really parse the exact time and date,
        # so we'll just have to return the string as metadata
        if isinstance(date_string, str):
            return date_string
        
        return None
    
    except Exception as e:
        print(f"Could not parse date and time '{date_string}: {e}")
        print("This may be because the date and time data is just a string, and not an actual timestamp.")
        return None
    
def validate_data(post_object: Dict) -> bool:

    # validate that a post has all required fields with the correct metadata type
    # return as a boolean (true or false)

    try: 
        # check that the required fields exist
        required_fields = ['username', 'post_url', 'like_count', 'comment_count']

        for field in required_fields:
            if field not in post_object:
                print(f"Validation failed: missing field '{field}")
                print("This is not a valid post! Out with you!")
                return False
        
        if not isinstance(post_object['username'], str) or not post_object['username']:
            print(f"'username' cannot be an empty string.")
            return False
        
        if not isinstance(post_object['post_url'], str) or not post_object['post_url']:
            print(f"'post_url' cannot be an empty string.")
            return False
        
        if not isinstance(post_object['like_count'], int) or post_object['like_count'] < 0:
            print(f"'like_count' must be a non-negative integer. If only we could bring back YouTube dislikes...")
            return False
        
        if not isinstance(post_object['comment_count'], int) or post_object['comment_count'] < 0:
            print(f"'comment_count' must be a non-negative integer.")
            return False
        
        print(f"Validation passed for @{post_object['username']}")
        return True
        
    except Exception as e:
        print(f"There was an error validating this post... {e}")
        return False
    

def process_all_posts(raw_posts: List[Dict]) -> List[Dict]:

    # normalize, validate, and process all scraped posts
    # main pipeline function:
    # 1. normalize each post
    # 2. validate each post
    # 3. filter out invalid or bot posts
    # 4. return cleaned data ready for apify dataset

    processed_posts = []

    try:
        print(f"\n--- Processing {len(raw_posts)} posts ---\n")
        
        for idx, raw_post in enumerate(raw_posts):
            print(f"Processing post {idx + 1}/{len(raw_posts)}...")

            # 1. normalize
            normalized = normalize_post(raw_post)

            # validate
            if validate_data(normalized):
                processed_posts.append(normalized)

            else:
                print(f"Skipping invalid post from @{normalized.get('username', 'Unknown')}\n")

        print(f"\nSuccessfully processed {len(processed_posts)}/{len(raw_posts)}")
        return processed_posts
    
    except Exception as e:
        print(f"There was an error processing posts... {e}")
        print("There is DEFINITELY something wrong here. Please open an issue on GitHub, or text/email Rhylie.")
        return processed_posts



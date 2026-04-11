from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import requests
import time

def fetch_post_page(post_url: str, delay: float = 1.5) -> Optional[str]:
	
    # wait before making request (rate limiting)
    time.sleep(delay)

    try: 
        soup = BeautifulSoup(html, 'html.parser')

        caption_elem = soup.find('h1', {'class': lambda x: x and '_aacl' in x})

        if not caption_elem:
            caption_elem = soup.find('span', {'class': lambda x: x and '_aacl' in x})

        if caption_elem:
            caption_text = caption_elem.get_text(strip = True)
            print(f"Extracted caption: {caption_text[:50]}.")
            return caption_text
        
        print(f"No caption found.")
        return None
    
    except Exception as e:
        print(f"There was an error extracting the caption: {e}")
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
            number = float(like_text.upper().replace('K', ''))
            return int(number * 1000000)
        
        # removes commas and converts to list
        like_count = int(like_text.replace(',', ''))
        return like_count
    
    except ValueError:
        return None
    
def extract_comments(html: str, max_count: int = 5) -> List[Dict]:
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
                like_button = comment_item.find('button', 'aria-label': lambda x: x and 'like' in x.lower())
                if like_button:
                    like_text = like_button.get_text(strip = True)
                    comment_dict['likes'] = parse_like_count(like_text)

                # extract timestamp 
                time_link = comment_item.find('a', {'class': lambda x: x and '_aacl' in x})
                if time_link:
                    comment_dict['timestamp'] = time_link.get_text(strip = True)

                comments_list.append(comment_dict)

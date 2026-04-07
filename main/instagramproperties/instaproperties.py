from bs4 import BeautifulSoup


def extract_insta_desc(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    insta_description = soup.find("meta", {"property": "og:description"})
    return insta_description["content"] if insta_description else None

def extract_insta_username(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    insta_username = soup.find("meta", {"property": "og:title"})
    return insta_username["content"] if insta_username else None

def extract_posts(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    posts = []
    for post in soup.find_all("div", class_= "post"):
        post_data = {
            "image": post.find("img")["src"],
            "caption": post.find("span", class_= "caption").text,
            "likes": post.find("span", class_= "likes").text
        }
        posts.append(post_data)
    return posts

def extract_hashtags(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    hashtags = []
    for link in soup.find_all("a", href=True):
        if link["href"].startswith("/explore/tags/"):
            hashtags.append(link.text)
    return hashtags

def extract_specified_hashtags(html_content, specified_hashtags):
    soup = BeautifulSoup(html_content, 'html.parser')
    found_hashtags = []
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if "/explore/tags/" in href:
            hashtag = href.split("/explore/tags/")[1].strip("/")
            if hashtag in specified_hashtags:
                found_hashtags.append(hashtag)
    return found_hashtags


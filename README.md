# BSHunter - Instagram Hashtag Scraper

A production-ready Apify actor that scrapes Instagram posts by hashtag using Selenium and BeautifulSoup.

## Features

✨ **Complete Post Data**
- Caption text
- Image URL
- Like count
- Post timestamp
- Author username & profile link

💬 **Comment Extraction**
- Top N comments per post
- Comment author & text
- Comment likes & timestamp
- Configurable comment limit

👤 **Profile Data**
- Author username
- Profile picture URL
- Profile link

🔧 **Smart Data Processing**
- Normalizes all data to consistent format
- Converts like counts (1.2K → 1200, 1.5M → 1500000)
- Validates all required fields
- Handles edge cases gracefully

## Input Parameters

```json
{
  "hashtags": ["python", "programming"],
  "maxPostsPerHashtag": 10,
  "maxCommentsPerPost": 5,
  "maxScrolls": 5
}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `hashtags` | Array | Required | Instagram hashtags to scrape (without #) |
| `maxPostsPerHashtag` | Int | 10 | Max posts to collect per hashtag |
| `maxCommentsPerPost` | Int | 5 | Max top comments per post |
| `maxScrolls` | Int | 5 | Number of scrolls to load posts |

## Output

The actor outputs normalized posts to the dataset:

```json
{
  "username": "instauser",
  "caption": "Amazing sunset! 🌅",
  "post_url": "https://instagram.com/p/ABC123/",
  "image_url": "https://scontent.../image.jpg",
  "like_count": 1200,
  "comment_count": 3,
  "comments": [
    {
      "author": "user1",
      "text": "Beautiful!",
      "likes": 42,
      "timestamp": "2 days ago"
    }
  ],
  "timestamp": "2024-04-13T10:30:00Z",
  "scraped_at": "2024-04-13T15:45:22Z"
}
```

## Architecture

```
Selenium WebDriver
    ↓
Navigate & Scroll Instagram
    ↓
BeautifulSoup Feed Parsing
    ↓
Extract Post URLs
    ↓
Fetch Individual Posts (HTTP)
    ↓
Extract Comments & Profile
    ↓
Data Normalization & Validation
    ↓
Apify Dataset Output
```

## Modules

- **browser_module.py** — Selenium WebDriver automation
- **post_scraper.py** — BeautifulSoup feed parsing  
- **post_details.py** — Individual post & comment extraction
- **data_parser.py** — Data normalization & validation
- **actor_main.py** — Main orchestration script

## Rate Limiting

- 1.5 second delay between post requests
- Headless Chrome with realistic user-agent
- Respects Instagram's rate limits

## Performance

- Typical: 1-3 seconds per post
- 50 posts ≈ 2-5 minutes
- Scales to hundreds on Apify Platform

## Limitations

- Public hashtags only (no login)
- Some posts have comments disabled
- Instagram HTML structure changes frequently (selectors may need updates)
- Comment pagination requires Selenium clicks (see code for implementation)

## Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Validate setup
python verify_setup.py

# Run unit tests
python test_data_parser.py
python test_imports.py
```

## GitHub Repository

https://github.com/xrhyliee/BSHunter

## License

MIT

---

**Created:** April 2026  
**Version:** 1.0.0  
**Status:** Production-Ready ✅

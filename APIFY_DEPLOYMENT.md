# 🚀 Deploying BSHunter to Apify Platform

## Prerequisites

1. **Apify Account** — Sign up at https://apify.com
2. **Apify CLI** — Install with `npm install -g apify-cli`
3. **GitHub Repository** — Already pushed ✅ (https://github.com/xrhyliee/BSHunter)

---

## Option 1: Deploy via Apify CLI (Recommended)

### Step 1: Install Apify CLI

```bash
npm install -g apify-cli
```

### Step 2: Authenticate

```bash
apify auth --token YOUR_APIFY_TOKEN
```

Get your token from: https://console.apify.com/account/integrations/api

### Step 3: Deploy from GitHub

```bash
cd c:\Users\scgra\OneDrive\GitHub\BSHunter

# Push to Apify
apify push --git-repo https://github.com/xrhyliee/BSHunter.git
```

Or clone and push:

```bash
apify create my-instagram-scraper --template python_playwright
cd my-instagram-scraper
# Copy files from BSHunter...
apify push
```

---

## Option 2: Deploy via Web UI

### Step 1: Go to Apify Console

https://console.apify.com/actors

### Step 2: Create New Actor

Click **"Create new actor"** → **"From code"**

### Step 3: Connect GitHub

1. Click **"Integrate repository"**
2. Select your GitHub account
3. Select **xrhyliee/BSHunter** repository
4. Authenticate GitHub

### Step 4: Configure Build

The `Dockerfile` and `apify.json` will be auto-detected.

### Step 5: Publish

Click **"Publish actor"**

---

## Option 3: Deploy via Docker

### Build Local Image

```bash
cd c:\Users\scgra\OneDrive\GitHub\BSHunter

docker build -t my-instagram-scraper:latest .
```

### Test Locally

```bash
docker run -e APIFY_TOKEN=YOUR_TOKEN \
  -v "$(pwd)/test_input.json:/src/test_input.json" \
  my-instagram-scraper:latest
```

### Push to Docker Hub (Optional)

```bash
docker tag my-instagram-scraper:latest YOUR_DOCKERHUB_USERNAME/my-instagram-scraper:latest
docker push YOUR_DOCKERHUB_USERNAME/my-instagram-scraper:latest
```

---

## Testing on Apify

### Run Test

1. Go to actor page → **"Test Actor"**
2. Paste input:
```json
{
  "hashtags": ["python"],
  "maxPostsPerHashtag": 3,
  "maxCommentsPerPost": 2,
  "maxScrolls": 2
}
```
3. Click **"Test run"**

### Monitor Execution

- **Logs** tab — View print statements & errors
- **Dataset** tab — See output data
- **Storage** tab — Check memory usage

---

## Troubleshooting

### Issue: Selenium/Chrome not found

```
Error: chromedriver executable not found
```

**Solution:** Update Dockerfile:

```dockerfile
FROM apify/actor-python-selenium:3.11

# Rest of Dockerfile...
```

### Issue: SSL/Certificate errors

Add to actor_main.py:

```python
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```

### Issue: Rate limited by Instagram

Increase delays in `post_details.py`:

```python
def fetch_post_page(post_url: str, delay: float = 3.0) -> Optional[str]:
    # Increase delay from 1.5 to 3.0
    time.sleep(delay)
```

### Issue: CSS selectors not matching

Instagram HTML changes frequently. Update selectors:

1. Open Instagram in browser
2. Inspect post element (F12)
3. Update CSS selector in relevant module
4. Commit & push to GitHub
5. Apify auto-rebuilds

---

## Performance Optimization

### For Large-Scale Scraping

#### Use Proxies (Apify Platform)

In `actor_main.py`:

```python
from apify import Actor

async with Actor:
    actor_input = await Actor.get_input()
    
    # Apify provides proxy automatically
    proxy_url = Actor.get_proxy_url()
    # Pass to requests library
```

#### Enable Concurrency

Run multiple hashtags in parallel:

```python
import asyncio

async def scrape_hashtag(hashtag):
    # Scraping logic
    pass

# Run 3 hashtags in parallel
await asyncio.gather(
    scrape_hashtag('python'),
    scrape_hashtag('programming'),
    scrape_hashtag('coding')
)
```

#### Cache Results

Store scraped data locally to avoid re-scraping:

```python
import json

CACHE_FILE = 'posts_cache.json'

def load_cache():
    try:
        with open(CACHE_FILE) as f:
            return json.load(f)
    except:
        return {}

def save_cache(data):
    with open(CACHE_FILE, 'w') as f:
        json.dump(data, f)
```

---

## Scheduling Runs

### Via Apify UI

1. Actor page → **"Runs" tab**
2. Click **"Schedule run"**
3. Set frequency (hourly, daily, weekly)
4. Configure input

### Via API

```bash
# Run every day at 9 AM
curl https://api.apify.com/v2/actor-tasks \
  -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "actorId": "YOUR_ACTOR_ID",
    "input": {
      "hashtags": ["python"],
      "maxPostsPerHashtag": 10
    },
    "isScheduled": true,
    "frequency": "0 9 * * *"
  }'
```

---

## Cost Estimation

**Pricing** (as of April 2026):

| Item | Cost |
|------|------|
| Compute | $0.15/hour |
| Typical 50-post run | ~$0.10 |
| 100 runs/month | ~$10 |
| Storage | Free (first 10 GB) |

---

## Monitoring & Analytics

### View Actor Stats

https://console.apify.com/actors/YOUR_ACTOR_ID/stats

- Total runs
- Avg duration
- Cost per run
- Success/failure rate
- Dataset size

### Webhook Integration

Connect to Slack/Discord to get notified of run completions:

```json
{
  "eventTypes": ["ACTOR_RUN_SUCCEEDED"],
  "webhookUrl": "https://hooks.slack.com/services/YOUR/WEBHOOK"
}
```

---

## Publishing to Apify Store

To make your actor publicly available:

1. Go to actor page → **"Publish"**
2. Set pricing (free or paid)
3. Add description, screenshots, examples
4. Click **"Publish to Apify Store"**

Your actor will appear in https://apify.com/store

---

## Quick Deployment Checklist

- [ ] Add your Apify API token to environment
- [ ] Test locally with `python verify_setup.py`
- [ ] Commit all changes to GitHub
- [ ] Update `.env` variables (remove dummy values)
- [ ] Test `Dockerfile` builds locally
- [ ] Deploy via CLI or Web UI
- [ ] Run test execution on Apify
- [ ] Monitor logs for errors
- [ ] Adjust CSS selectors if needed
- [ ] Set up scheduling (optional)
- [ ] Monitor costs & performance

---

## Next Steps

✅ **Done:** Build & test locally  
→ **Next:** Deploy to Apify Platform  
→ **Future:** Monitor & optimize performance

---

**Questions?** See [Apify Docs](https://docs.apify.com/)

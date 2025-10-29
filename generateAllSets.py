try:
    import cloudscraper
    USE_CLOUDSCRAPER = True
except ImportError:
    import requests
    USE_CLOUDSCRAPER = False

from bs4 import BeautifulSoup
import os

# Get the directory of this file and do the file checks
script_dir = os.path.dirname(os.path.abspath(__file__))
allSets = []

# Scrape the website to find new sets
url = "https://www.magicspoiler.com/mtg-spoilers/"

# Use cloudscraper if available (handles Cloudflare protection)
if USE_CLOUDSCRAPER:
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'firefox',
            'platform': 'windows',
            'desktop': True
        }
    )
    response = scraper.get(url)
else:
    # Fallback to requests with browser-like headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:144.0) Gecko/20100101 Firefox/144.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Priority': 'u=0, i',
        'TE': 'trailers',
    }
    response = requests.get(url, headers=headers)

response.raise_for_status()
soup = BeautifulSoup(response.content, 'html.parser')

# Extract all sets
for a_tag in soup.find_all('a', href=True):
    upcoming_set_div = a_tag.find('div', class_='upcoming-set')
    if upcoming_set_div:
        href = a_tag['href']
        parts = href.strip('/').split('/')
        set_id = parts[-1]
        allSets.append(set_id + "\n")

# Write all sets to a file
with open(os.path.join(script_dir, "all_sets.txt"), "w") as f:
    f.writelines(allSets)

print("all_sets.txt has been generated.")

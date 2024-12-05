import requests
from bs4 import BeautifulSoup
import os

# Get the directory of this file and do the file checks
script_dir = os.path.dirname(os.path.abspath(__file__))
allSets = []

# Scrape the website to find new sets
url = "https://www.magicspoiler.com/mtg-spoilers/"
response = requests.get(url)
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

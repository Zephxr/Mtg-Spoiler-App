import requests
from bs4 import BeautifulSoup
from discordFunc import process_sets
newSets = []
oldSets = []
allSets = []
# Load old sets from file
with open("old_sets.txt", "r") as f:
    oldSets = [line.strip() for line in f.readlines()]

# Scrape the website to find new sets
url = "https://www.magicspoiler.com/mtg-spoilers/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract new sets
for a_tag in soup.find_all('a', href=True):
    # Check if the anchor contains a div with class "upcoming-set"
    upcoming_set_div = a_tag.find('div', class_='upcoming-set')
    if upcoming_set_div:
        href = a_tag['href']
        
        # Extract the set ID (text between the last / and second to last /)
        parts = href.strip('/').split('/')
        set_id = parts[-1]  # The second-to-last part is the set ID
        
        # Check if the set is new
        if set_id not in oldSets:
            print(f"New set found: {href}, {set_id}")
            newSets.append(set_id)
        allSets.append(set_id + "\n")

with open("all_sets.txt","w") as f:
    f.writelines(allSets)

import asyncio
asyncio.run(process_sets(newSets))


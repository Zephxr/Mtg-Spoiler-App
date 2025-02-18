import requests
from bs4 import BeautifulSoup
from discordFunc import process_sets
import os

newSets = []  # List to store new sets that are found
oldSets = []  # List to store previously seen sets
allSets = set()  # Set to store all unique sets (including new and old)

# Get the directory of this file for proper path handling
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load the list of all sets from the 'all_sets.txt' file to keep track of the sets
with open(os.path.join(script_dir, "all_sets.txt"), "r") as f:
    allSets = set(line.strip() for line in f.readlines())

# Load old sets (sets that were previously seen) from the 'old_sets.txt' file
with open(os.path.join(script_dir, "old_sets.txt"), "r") as f:
    oldSets = [line.strip() for line in f.readlines()]

# Scrape the website to find new sets
url = "https://www.magicspoiler.com/mtg-spoilers/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract new sets from the website by checking the appropriate HTML structure
for a_tag in soup.find_all('a', href=True):
    # Check if the anchor contains a div with class "upcoming-set" (indicating a new set)
    upcoming_set_div = a_tag.find('div', class_='upcoming-set')
    if upcoming_set_div:
        href = a_tag['href']
        
        # Extract the set ID by splitting the URL at '/' and taking the second-to-last part
        parts = href.strip('/').split('/')
        set_id = parts[-1]  # The second-to-last part is the set ID
        
        # Only add the set if it is not already in the "oldSets" list
        if set_id not in oldSets:
            # Add the set to the list of new sets if it hasn't been processed before
            newSets.append(set_id)
            allSets.add(set_id)  # Add the new set to the allSets collection to keep track

# Update the 'all_sets.txt' file with the latest set data
# This ensures that we keep track of all the sets we've seen
with open(os.path.join(script_dir, "all_sets.txt"), "w") as f:
    for item in allSets:
        f.write(item + '\n')

# Process the newly found sets by passing them to the discordFunc process_sets function
import asyncio
asyncio.run(process_sets(newSets))

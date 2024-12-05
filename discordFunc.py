import os
import asyncio
import requests
from bs4 import BeautifulSoup
from webhook import webhook

async def sendDiscord(card_title, card_link, card_image, set_name):
    webhook_url = webhook
    data = {
        "content": f"New card found: {card_title} ({set_name})\n{card_link}",
        "embeds": [
            {
                "title": card_title,
                "url": card_link,
                "image": {
                    "url": card_image
                }
            }
        ]
    }

    # Retry logic in case of HTTP 429 (Too Many Requests)
    while True:
        response = await asyncio.to_thread(requests.post, webhook_url, json=data)
        
        if response.status_code == 204:
            print("Successfully sent the message to Discord!")
            break  # Exit the loop if the request was successful
        elif response.status_code == 429:
            print("Rate limit exceeded. Retrying after 1 second...")
            await asyncio.sleep(1)  # Wait for 1 second before retrying
        else:
            print(f"Failed to send the message to Discord: {response.status_code}")
            break  # Exit the loop on any other error

async def process_sets(newSets):
    # Get the directory of this file and do the file checks.  This works around using the script in a cronjob.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Process each new set
    for set in newSets:
        seenCards = []

        # Check if set has a file in the 'sets' directory, if not, create one
        set_file_path = os.path.join(script_dir, 'sets', f"{set}.txt")

        # If the set file doesn't exist, create it
        if not os.path.exists(set_file_path):
            with open(set_file_path, "w") as f:
                f.write("")

        # Read the seen cards from the set file
        with open(set_file_path, "r") as f:
            print(set_file_path)
            seenCards = [line.strip() for line in f.readlines()]

        # Scrape the cards from the website
        set_url = f"https://www.magicspoiler.com/mtg-set/{set}/"
        set_response = requests.get(set_url)
        set_soup = BeautifulSoup(set_response.content, 'html.parser')

        # Look for cards in the "set-card-2" class
        for card in set_soup.find_all('article', class_='set-card-2'):
            card_title_tag = card.find('a', title=True)
            if card_title_tag:
                card_title = card_title_tag['title']
                card_link = card_title_tag['href']
                card_image_tag = card.find('img', src=True)
                card_image = card_image_tag['src'] if card_image_tag else ""

                # If the card has not been seen before, send a notification
                if card_title not in seenCards:
                    # Send the new card notification
                    await sendDiscord(card_title, card_link, card_image, set)

                    # Add the card to the seenCards list and update the file
                    seenCards.append(card_title)
                    with open(set_file_path, "a") as f:
                        f.write(f"{card_title}\n")

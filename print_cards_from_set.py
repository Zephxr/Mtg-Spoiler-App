try:
    import cloudscraper
    USE_CLOUDSCRAPER = True
except ImportError:
    import requests
    USE_CLOUDSCRAPER = False

from bs4 import BeautifulSoup
import sys
import os

def print_cards_from_set(set_id):
    """
    Args:
        set_id: The set identifier (e.g., 'aetherdrift', 'spider-man')
    """
    print(f"\nFetching cards from set: {set_id}")
    print("=" * 60)
    
    set_url = f"https://www.magicspoiler.com/mtg-set/{set_id}/"
    
    try:
        if USE_CLOUDSCRAPER:
            scraper = cloudscraper.create_scraper(
                browser={
                    'browser': 'firefox',
                    'platform': 'windows',
                    'desktop': True
                }
            )
            set_response = scraper.get(set_url)
        else:
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
            set_response = requests.get(set_url, headers=headers)
        
        set_response.raise_for_status()
        set_soup = BeautifulSoup(set_response.content, 'html.parser')
        
        set_name_tag = set_soup.find('h1')
        set_name = set_name_tag.get_text().strip() if set_name_tag else set_id
        
        print(f"Set Name: {set_name}")
        print("=" * 60)
        
        cards = set_soup.find_all('article', class_='set-card-2')
        
        if not cards:
            print(f"No cards found for set '{set_id}'.")
            return
        
        print(f"\nFound {len(cards)} cards:\n")
        
        for index, card in enumerate(cards, 1):
            card_title_tag = card.find('a', title=True)
            
            if card_title_tag:
                card_title = card_title_tag['title']
                card_link = card_title_tag['href']
                card_image_tag = card.find('img', src=True)
                card_image = card_image_tag['src'] if card_image_tag else "No image"
                
                print(f"{index}. {card_title}")
                print(f"   Link: {card_link}")
                print(f"   Image: {card_image}")
                print()
            else:
                print(f"{index}. [Card title not found]")
                print()
        
        print("=" * 60)
        print(f"Total cards printed: {len(cards)}")
        
    except Exception as e:
        error_type = type(e).__name__
        if 'RequestException' in error_type or 'HTTP' in error_type or '403' in str(e):
            print(f"Error fetching set data: {e}")
            if '403' in str(e):
                print("\nNote: 403 Forbidden error detected. This usually means Cloudflare protection is active.")
                if not USE_CLOUDSCRAPER:
                    print("Try installing cloudscraper: pip install cloudscraper")
            print(f"Please check if the set ID '{set_id}' is correct.")
        else:
            print(f"An error occurred: {e}")


def main():
    if len(sys.argv) > 1:
        set_id = sys.argv[1]
    else:
        print("MTG Card Set Printer")
        print("=" * 60)
        print("\nEnter the set ID (e.g., 'aetherdrift', 'spider-man', 'bloomburrow')")
        print("You can find set IDs in all_sets.txt file")
        print("=" * 60)
        set_id = input("\nSet ID: ").strip()
        
        if not set_id:
            print("Error: Set ID cannot be empty.")
            sys.exit(1)
    
    print_cards_from_set(set_id)


if __name__ == "__main__":
    main()

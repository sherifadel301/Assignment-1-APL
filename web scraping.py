"""
Simple Web Scraper with BeautifulSoup
Scrapes quotes from quotes.toscrape.com
"""

import requests
from bs4 import BeautifulSoup
import json
import os

# Configuration
BASE_URL = "http://quotes.toscrape.com"

def fetch_page(url):
    """Download a web page"""
    response = requests.get(url)
    return response.text

def scrape_quotes(page_url):
    """Extract quotes from a page"""
    # Get HTML
    html = fetch_page(page_url)
    
    # Parse with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find all quote divs
    quote_divs = soup.find_all('div', class_='quote')
    
    quotes = []
    for div in quote_divs:
        # Extract text
        text = div.find('span', class_='text').text
        
        # Extract author
        author = div.find('small', class_='author').text
        
        # Extract tags
        tags = [tag.text for tag in div.find_all('a', class_='tag')]
        
        # Store in dictionary
        quote = {
            'text': text,
            'author': author,
            'tags': tags
        }
        quotes.append(quote)
    
    return quotes

def save_to_json(data, filename='quotes.json'):
    """Save data to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Saved to {filename}")

# Main program
if __name__ == "__main__":
    print("Quote Scraper")
    print("-" * 40)
    
    # Where to save?
    save_path = input("Enter folder path (or press Enter for current folder): ").strip()
    if not save_path:
        save_path = os.getcwd()  # Current folder
    
    filename = input("Enter filename (default: quotes.json): ").strip()
    if not filename:
        filename = "quotes.json"
    
    # Full path
    full_path = os.path.join(save_path, filename)
    
    # How many pages?
    num_pages = int(input("How many pages? (1-10): "))
    
    all_quotes = []
    
    # Scrape each page
    for page in range(1, num_pages + 1):
        url = f"{BASE_URL}/page/{page}/"
        print(f"Scraping page {page}...")
        
        quotes = scrape_quotes(url)
        all_quotes.extend(quotes)
    
    # Save to file
    print(f"\nScraped {len(all_quotes)} quotes!")
    save_to_json(all_quotes, full_path)
    print(f"Done! Check {full_path}")
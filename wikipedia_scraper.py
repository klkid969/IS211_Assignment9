# wikipedia_scraper.py
# Scrapes World Series champions from: https://en.wikipedia.org/wiki/List_of_World_Series_champions

import requests
from bs4 import BeautifulSoup

def scrape_world_series_champions():
    try:
        # Configure request
        url = "https://en.wikipedia.org/wiki/List_of_World_Series_champions"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        print("⏳ Downloading World Series champions data from Wikipedia...")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the main champions table
        table = soup.find('table', {'class': 'wikitable'})
        
        if not table:
            print("❌ Error: Could not find World Series champions table.")
            return
            
        # Print header
        print("\n⚾ World Series Champions")
        print("=" * 90)
        print("{:<6} {:<25} {:<25} {:<25}".format(
            "Year", "Winning Team", "Manager", "Games"
        ))
        print("-" * 90)
        
        # Extract and print data
        for row in table.find_all('tr')[1:]:  # Skip header row
            cols = row.find_all(['td', 'th'])
            
            if len(cols) >= 4:
                try:
                    year = cols[0].get_text(strip=True)
                    if not year.isdigit():  # Skip non-data rows
                        continue
                        
                    team = cols[1].get_text(strip=True).split('[')[0]
                    manager = cols[2].get_text(strip=True).split('[')[0]
                    games = cols[3].get_text(strip=True)
                    
                    print("{:<6} {:<25} {:<25} {:<25}".format(
                        year, team[:24], manager[:24], games
                    ))
                except:
                    continue  # Skip problematic rows
        
        print("\n✅ Data successfully scraped!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    scrape_world_series_champions()

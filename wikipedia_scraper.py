# wikipedia_scraper.py
# Scrapes World Series champions from: https://en.wikipedia.org/wiki/List_of_World_Series_champions

import requests
from bs4 import BeautifulSoup

def scrape_world_series():
    try:
        url = "https://en.wikipedia.org/wiki/List_of_World_Series_champions"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        table = soup.find('table', {'class': 'wikitable'})
        if not table:
            print("Error: World Series table not found")
            return

        print("\nWorld Series Champions:")
        print("=" * 80)
        print("{:<6} {:<25} {:<25} {:<15}".format(
            "Year", "Winning Team", "Manager", "Games"
        ))
        print("-" * 80)

        for row in table.find_all('tr')[1:]:
            cols = row.find_all(['td', 'th'])
            if len(cols) >= 4:
                year = cols[0].text.strip()
                if year.isdigit():
                    team = cols[1].text.split('[')[0].strip()
                    manager = cols[2].text.split('[')[0].strip()
                    games = cols[3].text.strip()
                    print("{:<6} {:<25} {:<25} {:<15}".format(
                        year, team[:22], manager[:22], games
                    ))

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape_world_series()

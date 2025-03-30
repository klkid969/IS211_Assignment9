# football_stats.py
# Scrapes NFL scoring leaders from: https://www.cbssports.com/nfl/stats/player/scoring/nfl/regular/all/

import requests
from bs4 import BeautifulSoup

def scrape_football_stats():
    try:
        url = "https://www.cbssports.com/nfl/stats/player/scoring/nfl/regular/all/"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        table = soup.find('table', class_='TableBase-table')
        if not table:
            print("Error: Stats table not found")
            return

        print("\nTop 20 NFL Scoring Leaders:")
        print("=" * 90)
        print("{:<25} {:<5} {:<5} {:<8} {:<8} {:<8}".format(
            "Player", "Pos", "Team", "Games", "FG", "PTS"
        ))
        print("-" * 90)

        for row in table.find_all('tr')[1:21]:
            cols = row.find_all('td')
            if len(cols) >= 6:
                player = cols[0].find('a').text.strip()
                pos_team = cols[0].find('span', class_='CellPlayerName-position').text.strip()
                pos, team = (pos_team.split('•') + ['N/A'])[:2]
                games = cols[1].text.strip()
                fg = cols[2].text.strip()
                pts = cols[4].text.strip()

                print("{:<25} {:<5} {:<5} {:<8} {:<8} {:<8}".format(
                    player[:22], pos.strip(), team.strip(), games, fg, pts
                ))

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape_football_stats()

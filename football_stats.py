# football_stats.py
# Scrapes NFL scoring leaders from: https://www.cbssports.com/nfl/stats/player/scoring/nfl/regular/all/

import requests
from bs4 import BeautifulSoup

def scrape_football_stats():
    try:
        # Configure request
        url = "https://www.cbssports.com/nfl/stats/player/scoring/nfl/regular/all/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        
        # Fetch data
        print("⏳ Downloading data from CBS Sports...")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'class': 'TableBase-table'})
        
        if not table:
            print("❌ Error: Could not find stats table.")
            return
        
        # Custom headers (using abbreviations)
        headers = ["Player", "Pos", "Team", "GP", "RUTD", "RETD", "PR", "KR", 
                  "INTR", "FUMR", "FG", "XP", "SFTY", "2-PT", "PTS", "PTS/G"]
        
        # Print table header
        print("\n🏈 Top 20 NFL Scoring Leaders")
        print("=" * 120)
        print("{:<22} {:<4} {:<4} {:<4} {:<6} {:<6} {:<4} {:<4} {:<6} {:<6} {:<4} {:<4} {:<5} {:<5} {:<6} {:<6}".format(*headers))
        print("-" * 120)
        
        # Extract player data
        for row in table.find('tbody').find_all('tr')[:20]:
            cols = row.find_all('td')
            
            # Player info - NEW TEAM EXTRACTION METHOD
            player = cols[0].find('a').get_text(strip=True)
            pos_team_span = cols[0].find('span', class_='CellPlayerName-team')
            
            if pos_team_span:
                team = pos_team_span.get_text(strip=True)
                pos = cols[0].find('span', class_='CellPlayerName-position').get_text(strip=True)
            else:
                # Fallback method
                pos_team = cols[0].find('span', class_='CellPlayerName-position')
                if pos_team:
                    pos_team_text = pos_team.get_text(strip=True)
                    if '•' in pos_team_text:
                        pos, team = [x.strip() for x in pos_team_text.split('•')]
                    else:
                        pos = pos_team_text
                        team = "N/A"
                else:
                    pos = team = "N/A"
            
            # Stats (use '—' for empty values)
            stats = [col.get_text(strip=True) or '—' for col in cols[1:15]]
            
            # Print row
            print("{:<22} {:<4} {:<4} {:<4} {:<6} {:<6} {:<4} {:<4} {:<6} {:<6} {:<4} {:<4} {:<5} {:<5} {:<6} {:<6}".format(
                player[:20], pos, team, *stats
            ))
            
        print("\n✅ Data successfully scraped!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    scrape_football_stats()

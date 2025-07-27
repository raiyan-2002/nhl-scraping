from scrape_team import scrape_all_player_stats

# all team abbreviations

# atlantic division teams
atl_teams = [
    "TOR", "TBL", "FLA", "OTT", "MTL", "DET", "BUF", "BOS"
]

# metropolitan division teams
met_teams = [
    "WSH", "CAR", "NJD", "CBJ", "NYR", "NYI", "PIT", "PHI"
]

# central division teams
cen_teams = [
    "WPG", "DAL", "COL", "MIN", "STL", "UTA", "NSH", "CHI"
]

# pacific division teams
pac_teams = [
    "VEG", "LAK", "EDM", "CGY", "VAN", "ANA", "SEA", "SJS"
]

def scrape_all_teams():
    """Scrapes all player stats for all teams."""
    
    for team in atl_teams + met_teams + cen_teams + pac_teams:
        print(f"Scraping data for {team}...")
        scrape_all_player_stats(team)
        print(f"Finished scraping data for {team}.\n")

def main():
    """Main function to scrape all teams."""
    
    scrape_all_teams()

if __name__ == "__main__":
    main()
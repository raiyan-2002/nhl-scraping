from scrape_player import extract_and_save_tables
import csv
import time

# table IDs for player stats
table_ids_player = [
    "player_stats",  # Standard Stats
    "skaters_advanced_all",  # NHL Possession Metrics
    "skaters_play_by_play_playoffs_all",  # NHL Playoffs Extra Stats
    "skaters_advanced_playoffs_all"  # NHL Playoffs Possession Metrics
]

# table IDs for goalie stats
table_ids_goalie = [
    "goalie_stats",  # Goalie Stats
    "goalie_stats_post"  # Goalie Playoffs Stats
]

# table ID for team roster
ROSTER = "roster" # Roster Table

def form_team_url(team_abbr):
    """Forms the URL for a given team abbreviation. Default is for the 2025 season."""
    
    return f"https://www.hockey-reference.com/teams/{team_abbr}/2025.html"

def scrape_team_data(team_abbr):
    """Scrapes the roster for a given team abbreviation."""
    
    url = form_team_url(team_abbr)
    extract_and_save_tables(url, [ROSTER], f"{team_abbr}")

def scrape_all_player_info(team_abbr):
    """
    Scrapes all player information for a given team abbreviation.
    Returns a list of tuples containing player name, number, and URL.
    """
    
    scrape_team_data(team_abbr)
    res = []

    with open(f"{team_abbr}/roster.csv", "r") as file:
        reader = csv.DictReader(file)  

        for row in reader:
            player_name = row["Player"].rstrip(" (C)") # remove captain designation
            player_number = row["No."]
            player_url = row["Link"]
            player_position = row["Pos"]
            if player_url:
                player_url = f"https://www.hockey-reference.com{player_url}"
                res.append((player_name, player_number,  player_url, player_position))
            else:
                res.append((player_name, "No link available"))
        return res

def scrape_all_player_stats(team_abbr):
    """Scrapes all the player information for a given team."""
    
    players = scrape_all_player_info(team_abbr)

    for name, number, link, position in players:

        table_ids = table_ids_player
        if position == "G":
            table_ids = table_ids_goalie

        file_name = f"{team_abbr}/{name.replace(' ', '_')}_{number}"
        print(f"Scraping data for {name} ({number}) from {link}...")
        extract_and_save_tables(link, table_ids, file_name)
        time.sleep(20)


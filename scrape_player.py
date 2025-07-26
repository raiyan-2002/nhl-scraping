import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO

table_ids = [
    "player_stats",  # Standard Stats
    "skaters_advanced_all",  # NHL Possession Metrics
    "skaters_play_by_play_playoffs_all",  # NHL Playoffs Extra Stats
    "skaters_advanced_playoffs_all"  # NHL Playoffs Possession Metrics
]

def flatten_multiindex_columns(df):
    new_cols = []
    for col in df.columns:
        # col is a tuple, e.g. ('Unnamed: 0_level_0', '')
        # Filter out empty strings or 'Unnamed...' parts
        filtered = [c for c in col if c and not c.startswith('Unnamed')]
        if filtered:
            new_col = ' '.join(filtered)
        else:
            # fallback to just last element or a placeholder
            new_col = col[-1] if col[-1] else 'unknown'
        new_cols.append(new_col)
    df.columns = new_cols
    return df

def extract_table(soup, table_id):
    from io import StringIO
    table = soup.find("table", id=table_id)
    if table:
        html_str = str(table)
        df = pd.read_html(StringIO(html_str))[0]
        df = flatten_multiindex_columns(df)
        return df
    else:
        print(f"Table '{table_id}' not found.")
        return pd.DataFrame()

def save_to_csv(df, filename):
    if not df.empty:
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    else:
        print("DataFrame is empty, nothing to save.")

def save_tables(soup):
    for table_id in table_ids:
        df = extract_table(soup, table_id)
        if not df.empty:
            filename = f"{table_id}.csv"
            save_to_csv(df, filename)

def extract_and_save_tables(url):
    # Get page content
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    save_tables(soup)

extract_and_save_tables("https://www.hockey-reference.com/players/b/bouchev01.html")
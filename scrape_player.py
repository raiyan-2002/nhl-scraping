import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import os
import time

def flatten_multiindex_columns(df):
    """Flatten multi-index columns in a DataFrame."""

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
    """Extracts a table from the BeautifulSoup object and returns it as a DataFrame."""
    
    table = soup.find("table", id=table_id)
    if table:
        html_str = str(table)
        df = pd.read_html(StringIO(html_str))[0]
        df = flatten_multiindex_columns(df)
        df.columns = [''.join(str(col).split()) for col in df.columns]

        if table_id == "roster":
            hrefs = []
            for tr in table.find_all("tr")[1:]:  
                a = tr.find("a", href=True)
                hrefs.append(a["href"] if a else None)

            # Match the hrefs to the DataFrame rows
            if len(hrefs) == len(df):
                df["Link"] = hrefs
            else:
                print("Warning: Number of links does not match number of rows.")

        return df
    else:
        print(f"Table '{table_id}' not found.")
        return pd.DataFrame()

def save_to_csv(df, filename):
    """Saves a DataFrame to a CSV file."""
    
    if not df.empty:
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    else:
        print("DataFrame is empty, nothing to save.")

def save_table(soup, table_id, file_path=""):
    """Saves a table from the BeautifulSoup object to a CSV file."""

    df = extract_table(soup, table_id)
    os.makedirs(file_path, exist_ok=True)
    if not df.empty:
        filename = f"{file_path}/{table_id}.csv"
        save_to_csv(df, filename)
    else:
        raise ValueError(f"No data found for table ID: {table_id}")

def extract_and_save_tables(url, table_ids, file_path=""):
    """Extracts and saves multiple tables from a given URL."""

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(url, headers=headers)

    print(f"Status code: {response.status_code}")
    retry_after = response.headers.get("Retry-After")
    print(f"Retry-After: {retry_after}")

    if retry_after:
        time.sleep(int(retry_after))
        print(f"Retrying after {retry_after} seconds...")
        extract_and_save_tables(url, table_ids, file_path)

    soup = BeautifulSoup(response.content, "html.parser")
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    for table_id in table_ids:
        try:
            save_table(soup, table_id, file_path)
        except ValueError as e:
            print(f"Error saving table {table_id}: {e}")
            continue

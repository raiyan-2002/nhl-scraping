# NHL Data Scraper

This tool helps collect NHL team and player data in the form of CSV files. It obtains stats and advanced stats of player and goalie performance in the regular season and the playoffs. All data comes from [hockey-reference.com](https://www.hockey-reference.com/). This is only intended for personal use.

---

## Setup Instructions

### 1. Create a Virtual Environment

#### On macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies
Make sure your virtual environment is activated, then run:

```bash
pip install -r requirements.txt
```

### 3. Run the Scraper
```bash
python scrape.py
```
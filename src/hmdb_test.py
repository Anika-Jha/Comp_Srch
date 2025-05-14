import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import time

def get_hmdb_id(compound_name):
    formatted_name = compound_name.replace("-", " ").replace("(", "").replace(")", "")
    search_url = f"https://hmdb.ca/unearth/q?utf8=✓&query={quote(formatted_name)}&searcher=metabolites"

    print(f"🔍 Searching HMDB for: {formatted_name}")
    
    try:
        response = requests.get(search_url, timeout=15)
        if response.status_code != 200:
            return "Unavailable"

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find("table", {"class": "table"})

        if not table:
            return "Unavailable"

        rows = table.find_all("tr")[1:]  # Skip header row
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 1:
                name_cell = cols[0]
                name_text = name_cell.get_text(strip=True).lower()
                if name_text == compound_name.lower():
                    link = name_cell.find("a")
                    if link and "/metabolites/HMDB" in link["href"]:
                        return link["href"].split("/")[-1]  # e.g., HMDB0001234
        return "Unavailable"
    except Exception as e:
        print(f"❌ Error searching HMDB: {e}")
        return "Unavailable"

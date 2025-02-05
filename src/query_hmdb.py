import requests
from bs4 import BeautifulSoup

HMDB_SEARCH_URL = "https://hmdb.ca/unearth/q"

def get_hmdb_id(compound_name):
    """Search HMDB for the compound and return its HMDB ID."""
    params = {
        "utf8": "✓",
        "query": compound_name,
        "searcher": "metabolites"
    }

    try:
        response = requests.get(HMDB_SEARCH_URL, params=params)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            result = soup.find("a", href=lambda href: href and "/metabolites/HMDB" in href)

            if result:
                return result.text.strip()  # Extracts HMDB ID (e.g., HMDB0000122)
        
        return None
    except requests.RequestException as e:
        print(f"Error fetching HMDB data: {e}")
        return None

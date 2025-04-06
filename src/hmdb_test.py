import requests
import time
from urllib.parse import quote
from bs4 import BeautifulSoup
import re

def get_hmdb_id(compound_name):
    """Fetch HMDB ID for a compound with HTML parsing (forward lookup)."""
    
    # Clean compound name: remove parentheses, normalize whitespace
    formatted_name = re.sub(r"[()]", "", compound_name).strip()
    formatted_name = re.sub(r"\s+", " ", formatted_name)

    search_url = f"https://hmdb.ca/unearth/q?utf8=✓&query={quote(formatted_name)}&searcher=metabolites"
    print(f"🔎 Searching HMDB for: {formatted_name}")

    headers = {"User-Agent": "Mozilla/5.0"}
    max_retries = 3

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(search_url, timeout=10, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                result_link = soup.find('a', href=lambda x: x and x.startswith('/metabolites/HMDB'))
                if result_link:
                    hmdb_id = result_link['href'].split('/')[-1]
                    print(f"✅ Found HMDB ID: {hmdb_id}")
                    return hmdb_id
                else:
                    print("❌ No valid HMDB ID found in results.")
                    return "Not found"
            else:
                print(f"❌ HTTP Error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Attempt {attempt} failed: {e}")
            time.sleep(2)

    print("❌ HMDB ID: Failed after retries")
    return "Failed after retries"


def get_compound_name_from_hmdb(hmdb_id):
    """Reverse lookup: get compound name from HMDB ID."""
    url = f"https://hmdb.ca/metabolites/{hmdb_id}"
    print(f"🔄 Looking up compound name for HMDB ID: {hmdb_id}")

    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, timeout=10, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            name_tag = soup.find('h1')  # Compound name is typically in <h1>
            if name_tag:
                name = name_tag.text.strip()
                print(f"✅ Compound Name: {name}")
                return name
            else:
                print("❌ Name tag not found on page.")
                return "Name not found"
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return f"Error: {response.status_code}"
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return f"Request failed: {e}"


def main():
    query = input("Enter compound name or HMDB ID: ").strip()

    if re.match(r'^HMDB\d{7}$', query):  # HMDB ID pattern
        name = get_compound_name_from_hmdb(query)
        print(f"\nCompound Name: {name}")
    else:
        hmdb_id = get_hmdb_id(query)
        print(f"\nHMDB ID: {hmdb_id}")

if __name__ == "__main__":
    main()

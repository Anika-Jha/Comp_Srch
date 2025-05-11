import requests
from bs4 import BeautifulSoup
import time

HMDB_SEARCH_URL = "https://hmdb.ca/metabolites?utf8=%E2%9C%93&query={}&search_field=all"
HMDB_BASE_URL = "https://hmdb.ca"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

MAX_RETRIES = 3  # Number of times to retry a request before giving up
TIMEOUT = 30  # Increase timeout to 30 seconds

def get_hmdb_id(compound_name):
    """Fetches the correct HMDB ID for a given compound from the HMDB website."""
    session = requests.Session()
    search_url = HMDB_SEARCH_URL.format(compound_name.replace(" ", "+"))

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"🔍 Attempt {attempt}: Searching for {compound_name}...")

            # Step 1: Perform search request
            response = session.get(search_url, headers=HEADERS, timeout=TIMEOUT)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")

            # Step 2: Find ALL links to metabolites
            metabolite_links = soup.select("td a[href^='/metabolites/HMDB']")

            if not metabolite_links:
                print(f"⚠️ No HMDB entry found for {compound_name}.")
                return "Unavailable"

            # Step 3: Pick the FIRST valid HMDB ID (avoid HMDB0000001)
            for link in metabolite_links:
                metabolite_url = HMDB_BASE_URL + link["href"]
                if "HMDB0000001" not in metabolite_url:  # Skip invalid default
                    print(f"🔗 Selected Metabolite URL: {metabolite_url}")
                    break
            else:
                return "Unavailable"

            # Step 4: Visit the metabolite page and extract the actual HMDB ID
            metabolite_response = session.get(metabolite_url, headers=HEADERS, timeout=TIMEOUT)
            metabolite_response.raise_for_status()
            
            soup_metabolite = BeautifulSoup(metabolite_response.text, "html.parser")

            # Step 5: Extract HMDB ID
            hmdb_id_element = soup_metabolite.find("th", string="HMDB ID")
            if hmdb_id_element:
                hmdb_id = hmdb_id_element.find_next("td").text.strip()
                return hmdb_id

            return "Unavailable"

        except requests.exceptions.Timeout:
            print(f"⚠️ HMDB request timed out for {compound_name}. Retrying...")
            time.sleep(5)  # Wait before retrying
        except Exception as e:
            print(f"❌ Error fetching HMDB ID for {compound_name}: {e}")
            return "Unavailable"

    print(f"❌ Failed to retrieve HMDB ID for {compound_name} after {MAX_RETRIES} attempts.")
    return "Unavailable"

# 🔍 Testing
print(get_hmdb_id("glucose"))  # Should return the correct HMDB ID
print(get_hmdb_id("aniline"))  # Should return a different HMDB ID

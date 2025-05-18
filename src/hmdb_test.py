import requests
import time
from urllib.parse import quote
from bs4 import BeautifulSoup

def get_hmdb_id(compound_name, force_fuzzy=True):
    """Fetch HMDB ID using HTML parsing, optionally enforcing exact name match."""
    formatted_name = compound_name.replace("-", " ").replace("(", "").replace(")", "")
    search_url = f"https://hmdb.ca/unearth/q?utf8=✓&query={quote(formatted_name)}&searcher=metabolites"

    for attempt in range(3):
        try:
            response = requests.get(search_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                result_link = soup.find("a", href=lambda x: x and x.startswith("/metabolites/HMDB"))
                if result_link:
                    href = result_link["href"]
                    metabolite_url = f"https://hmdb.ca{href}"
                    print(f"🔗 Metabolite URL: {metabolite_url}")
                    try:
                        metab_resp = requests.get(metabolite_url, timeout=10)
                        metab_soup = BeautifulSoup(metab_resp.text, "html.parser")
                        title = metab_soup.find("title").text.strip()
                        hmdb_id = href.split("/")[-1]

                        if force_fuzzy:
                            return hmdb_id, title
                        elif formatted_name.lower() in title.lower():
                            return hmdb_id, title
                        else:
                            print("❌ Match failed: official name does not match query.")
                            return "Unavailable", "No match"
                    except:
                        return "Unavailable", "Timeout"
                return "Unavailable", "No match"
        except Exception as e:
            print(f"⚠️ HMDB request failed: {e}")
            time.sleep(2)
    return "Unavailable", "Failed"

if __name__ == "__main__":
    name = input("\n🔍 Enter compound name: ")
    result, title = get_hmdb_id(name)
    print(f"\nResult HMDB ID: {result}")
    print(f"Match Title: {title}")

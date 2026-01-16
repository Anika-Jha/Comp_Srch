import requests
import time
import random
from urllib.parse import quote
from bs4 import BeautifulSoup

# Persistent session for reuse
session = requests.Session()

def get_hmdb_id(compound_name, force_fuzzy=True):
    """Fetch HMDB ID using HTML parsing, optionally enforcing exact name match."""
    formatted_name = compound_name.replace("-", " ").replace("(", "").replace(")", "")
    search_url = f"https://hmdb.ca/unearth/q?utf8=✓&query={quote(formatted_name)}&searcher=metabolites"

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = session.get(search_url, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                result_link = soup.find("a", href=lambda x: x and x.startswith("/metabolites/HMDB"))

                if result_link:
                    href = result_link["href"]
                    hmdb_id = href.split("/")[-1]
                    metabolite_url = f"https://hmdb.ca{href}"
                    print(f"🔗 Metabolite URL: {metabolite_url}")

                    try:
                        metab_resp = session.get(metabolite_url, timeout=15)
                        if metab_resp.status_code == 200:
                            metab_soup = BeautifulSoup(metab_resp.text, "html.parser")
                            title = metab_soup.find("title").text.strip()

                            if force_fuzzy:
                                return hmdb_id, title
                            elif formatted_name.lower() in title.lower():
                                return hmdb_id, title
                            else:
                                print(" Match failed: official name does not match query.")
                                return "Unavailable", "No match"
                        else:
                            print(f" Metabolite page error: {metab_resp.status_code}")
                            return "Unavailable", "Timeout"
                    except Exception as e:
                        print(f" Error loading metabolite page: {e}")
                        return "Unavailable", "Timeout"

                else:
                    return "Unavailable", "No match"

            else:
                print(f" Bad response: {response.status_code}")
        except Exception as e:
            print(f" HMDB request failed on attempt {attempt+1}: {e}")
            backoff = 2 ** attempt + random.uniform(0.5, 2)
            time.sleep(backoff)

    return "Unavailable", "Failed after retries"

#  For manual testing
if __name__ == "__main__":
    name = input("\n Enter compound name: ")
    result, title = get_hmdb_id(name)
    print(f"\nResult HMDB ID: {result}")
    print(f"Match Title: {title}")

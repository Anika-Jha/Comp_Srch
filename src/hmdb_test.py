import requests
import time
from urllib.parse import quote
from bs4 import BeautifulSoup

def get_hmdb_id(compound_name, force_fuzzy=False):
    formatted_name = compound_name.replace("-", " ").replace("(", "").replace(")", "")  
    search_url = f"https://hmdb.ca/unearth/q?utf8=✓&query={quote(formatted_name)}&searcher=metabolites"
    print(f"Searching HMDB for: {formatted_name}")

    try:
        response = requests.get(search_url, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            result_link = soup.find("a", href=lambda x: x and x.startswith("/metabolites/HMDB"))
            if result_link:
                metabolite_url = "https://hmdb.ca" + result_link["href"]
                print("🔗 Metabolite URL:", metabolite_url)

                metabocard_resp = requests.get(metabolite_url, timeout=10)
                if metabocard_resp.status_code == 200:
                    metabocard_soup = BeautifulSoup(metabocard_resp.text, "html.parser")
                    title = metabocard_soup.find("title").text.strip()
                    if formatted_name.lower() in title.lower() or force_fuzzy:
                        return metabolite_url.split("/")[-1]
                    else:
                        print("❌ Match failed: official name does not match query.")
                        return "Not found"
        return None
    except Exception as e:
        print(f"⚠️ HMDB request failed: {e}")
        return None

if __name__ == "__main__":
    compound = input("\n🔍 Enter compound name: ")
    result = get_hmdb_id(compound)
    print("\nResult HMDB ID:", result)

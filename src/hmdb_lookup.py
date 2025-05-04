
import requests
import time

def fetch_hmdb_id(compound_name):
    """Fetches HMDB ID from online sources with error handling and retries."""
    sources = {
        "HMDB": f"https://hmdb.ca/metabolites?query={compound_name}",
        "MetaboAnalyst": f"https://rest.xialab.ca/api/mapcompounds?queryList={compound_name}&inputType=name",
        "CTS": f"https://cts.fiehnlab.ucdavis.edu/rest/convert?from=Chemical+Name&to=HMDB&q={compound_name}"
    }
    
    headers = {"User-Agent": "Mozilla/5.0"}

    for source, url in sources.items():
        for attempt in range(3):
            try:
                response = requests.get(url, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    data = response.json() if "json" in response.headers.get("Content-Type", "") else response.text
                    return parse_hmdb_response(data, source)
                
                elif response.status_code == 405:
                    print(f"❌ {source} Method Not Allowed (Check API docs)")
                    break
                
                else:
                    print(f"⚠️ {source} returned {response.status_code}. Retrying ({attempt+1}/3)...")
            
            except requests.Timeout:
                print(f"⏳ {source} timed out. Retrying ({attempt+1}/3)...")
                time.sleep(2)
            
            except requests.RequestException as e:
                print(f"❌ Error fetching HMDB from {source}: {e}")
                break  

    print("❌ All sources failed. HMDB ID unavailable.")
    return None

def parse_hmdb_response(response, source):
    """Parses HMDB ID from different sources."""
    if source == "MetaboAnalyst":
        return response.get("hmdb_id", None)
    elif source == "CTS":
        return response[0].get("to", None) if response else None
    return None

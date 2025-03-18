import requests

CHEMSPIDER_API_KEY = "YOUR_CHEMSPIDER_API_KEY"
CHEMSPIDER_URL = "https://api.rsc.org/compounds/v1"

def get_chemspider_data(compound_name):
    """Fetch ChemSpider data using the API."""
    headers = {
        "apikey": CHEMSPIDER_API_KEY,
        "Content-Type": "application/json"
    }

    search_url = f"{CHEMSPIDER_URL}/filter/name"
    payload = {"name": compound_name}
    
    try:
        response = requests.post(search_url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if "results" in data and data["results"]:
                return {"chemspider_id": data["results"][0]}  # ✅ Always return a dictionary
            else:
                return {"error": "⚠️ No ChemSpider data found!"}  # ✅ Return dictionary, not string
        elif response.status_code == 403:
            return {"error": "❌ ChemSpider API key may be invalid or blocked!"}  # ✅ Dictionary format
        else:
            return {"error": f"❌ Error: {response.status_code}, {response.text}"}  # ✅ Dictionary format

    except requests.RequestException as e:
        return {"error": f"❌ ChemSpider request failed: {e}"}  # ✅ Dictionary format

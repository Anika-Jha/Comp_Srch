import requests

METABOANALYST_API_URL = "https://rest.xialab.ca/api/mapcompounds"

def get_hmdb_from_metaboanalyst(compound_name):
    """Fetch HMDB ID for a given compound using MetaboAnalyst API."""
    headers = {'Content-Type': "application/json"}
    payload = {"queryList": compound_name, "inputType": "name"}

    try:
        response = requests.post(METABOANALYST_API_URL, json=payload, headers=headers, timeout=10)
        response.raise_for_status()  # Raise error if API request fails
        
        data = response.json()
        
        if "HMDB_ID" in data and data["HMDB_ID"]:
            return data["HMDB_ID"][0]  # Return first HMDB ID found
        
        print(f"⚠️ No HMDB ID found for {compound_name} in MetaboAnalyst.")
        return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching HMDB from MetaboAnalyst API: {e}")
        return None

# Example Usage
if __name__ == "__main__":
    compound = "glucose"
    hmdb_id = get_hmdb_from_metaboanalyst(compound)
    print(f"🔍 MetaboAnalyst HMDB ID for {compound}: {hmdb_id}")

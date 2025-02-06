import requests

API_KEY = "YOUR_CHEMSPIDER_API_KEY"  # Replace with your ChemSpider API key

def get_chemspider_data(compound_name):
    """Fetches ChemSpider ID and synonyms for a given compound name."""
    url = f"https://api.rsc.org/compounds/v1/filter/name"
    headers = {"apikey": API_KEY, "Content-Type": "application/json"}
    data = {"name": compound_name}

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        try:
            result = response.json()
            if "queryId" in result:
                query_id = result["queryId"]
                return get_compound_details(query_id)
            else:
                return None
        except Exception as e:
            print(f"Error parsing ChemSpider response: {e}")
            return None
    else:
        print(f"ChemSpider request failed: {response.status_code}")
        return None

def get_compound_details(query_id):
    """Retrieves compound details using the query ID from ChemSpider."""
    url = f"https://api.rsc.org/compounds/v1/records/{query_id}"
    headers = {"apikey": API_KEY}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch compound details: {response.status_code}")
        return None

# Example usage:
if __name__ == "__main__":
    compound = "Glucose"
    data = get_chemspider_data(compound)
    print(data)

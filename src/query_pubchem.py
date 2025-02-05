import requests

PUBCHEM_BASE_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"

def get_pubchem_synonyms(compound_name):
    """Fetch synonyms for a compound from PubChem."""
    search_url = f"{PUBCHEM_BASE_URL}/compound/name/{compound_name}/synonyms/JSON"

    try:
        response = requests.get(search_url)
        if response.status_code == 200:
            data = response.json()
            synonyms = data["InformationList"]["Information"][0]["Synonym"]
            return synonyms[:5]  # Return first 5 synonyms for efficiency

        return None
    except requests.RequestException as e:
        print(f"Error fetching PubChem data: {e}")
        return None

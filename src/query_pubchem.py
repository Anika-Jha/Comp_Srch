import requests

# Base URL for PubChem PUG REST API
PUBCHEM_BASE_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"

def get_pubchem_synonyms(compound_name):
    """Fetch synonyms for a given compound from PubChem."""
    
    # Construct the API request URL
    search_url = f"{PUBCHEM_BASE_URL}/compound/name/{compound_name}/synonyms/JSON"

    try:
       
        response = requests.get(search_url)

        if response.status_code == 200:
            # Parse JSON response
            data = response.json()

            # Extract the list of synonyms
            synonyms = data["InformationList"]["Information"][0]["Synonym"]
            
            # Return only the first 5 synonyms for efficiency
            return synonyms[:5]

        # Return None if no synonyms are found
        return None

    except requests.RequestException as e:
        # Print error message in case of request failure
        print(f"Error fetching PubChem data: {e}")
        return None

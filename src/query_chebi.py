
import requests
#API
CHEBI_SEARCH_URL = "https://www.ebi.ac.uk/webservices/chebi/2.0/test/getLiteEntity?search={}&maximumResults=1&entitySearchMode=ALL"
CHEBI_ENTITY_URL = "https://www.ebi.ac.uk/webservices/chebi/2.0/test/getCompleteEntity?chebiId={}"

def get_chebi_hmdb_id(compound_name):
   
    
    search_url = CHEBI_SEARCH_URL.format(compound_name)
    
    try:
        search_response = requests.get(search_url, timeout=10)
        if search_response.status_code != 200:
            print(f" ChEBI API Error: {search_response.status_code}")
            return None

        search_data = search_response.json()
        
        # DEBUG: Log the full response
        print(f" DEBUG: Full ChEBI Search Response for {compound_name}: {search_data}")

        search_results = search_data.get("ListElement", [])
        if not search_results:
            return None  # No ChEBI entry found
        
        chebi_id = search_results[0]["chebiId"]
        
        # Query ChEBI for full entity details
        entity_url = CHEBI_ENTITY_URL.format(chebi_id)
        entity_response = requests.get(entity_url, timeout=10)

        if entity_response.status_code != 200:
            print(f" ChEBI Entity API Error: {entity_response.status_code}")
            return None

        entity_data = entity_response.json()
        
        # DEBUG: Log the entity response
        print(f" DEBUG: Full ChEBI Entity Response for {chebi_id}: {entity_data}")

        xrefs = entity_data.get("DatabaseLinks", [])
        for xref in xrefs:
            if xref["type"] == "HMDB":
                return xref["id"]  # Return the first matching HMDB ID

        return None
    except requests.RequestException as e:
        print(f" Error fetching HMDB from ChEBI: {e}")
        return None

# Example Usage
if __name__ == "__main__":
    compound = "glucose"
    hmdb_id = get_chebi_hmdb_id(compound)
    print(f" ChEBI HMDB ID for {compound}: {hmdb_id}")

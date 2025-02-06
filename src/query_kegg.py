import requests

KEGG_BASE_URL = "https://rest.kegg.jp"

def get_kegg_id(compound_name, synonyms=[]):
    """Search KEGG for the compound and return its KEGG ID. If not found, retry with synonyms."""
    
    def search_kegg(name):
        """Helper function to query KEGG and extract the KEGG ID."""
        search_url = f"{KEGG_BASE_URL}/find/compound/{name}"
        try:
            response = requests.get(search_url)
            if response.status_code == 200:
                lines = response.text.strip().split("\n")
                if lines:
                    for line in lines:
                        parts = line.split("\t")
                        if len(parts) < 2:  # 🛑 Avoid IndexError if KEGG response is incomplete
                            continue  
                        
                        kegg_id = parts[0].replace("cpd:", "")  # Remove "cpd:" prefix
                        names = parts[1].split("; ")

                        # Prioritize exact match
                        if name.lower() in [n.lower() for n in names]:
                            return kegg_id

                    # If no exact match, return first result (if available)
                    if lines:
                        return lines[0].split("\t")[0].replace("cpd:", "")

            return None
        except requests.RequestException as e:
            print(f"❌ Error fetching KEGG data: {e}")
            return None

    # 1️⃣ First, try with the original compound name
    kegg_id = search_kegg(compound_name)
    if kegg_id:
        return kegg_id

    # 2️⃣ If not found, retry with synonyms
    for synonym in synonyms:
        print(f"🔄 Retrying KEGG search with synonym: {synonym}")
        kegg_id = search_kegg(synonym)
        if kegg_id:
            return kegg_id

    return None  # No KEGG ID found even after retrying synonyms

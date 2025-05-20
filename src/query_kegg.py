import requests

KEGG_BASE_URL = "https://rest.kegg.jp"

def get_kegg_id(compound_name, synonyms=[]):
    """
    Search KEGG for the compound and return its KEGG ID.
    If not found using the name, retry using synonyms.
    """
    def search_kegg(name):
        """Helper function to query KEGG and extract the KEGG ID."""
        search_url = f"{KEGG_BASE_URL}/find/compound/{name}"
        try:
            response = requests.get(search_url)
            if response.status_code == 200:
                lines = response.text.strip().split("\n")
                for line in lines:
                    parts = line.split("\t")
                    if len(parts) < 2:
                        continue
                    kegg_id = parts[0].replace("cpd:", "")
                    kegg_names = parts[1].split("; ")

                    # Look for an exact name match
                    if name.lower() in [n.lower() for n in kegg_names]:
                        return kegg_id

                # No exact match, return first result as fallback
                if lines:
                    return lines[0].split("\t")[0].replace("cpd:", "")
        except requests.RequestException as e:
            print(f"❌ Error fetching KEGG data: {e}")
        return None

    # 1️⃣ Try the main compound name
    kegg_id = search_kegg(compound_name)
    if kegg_id:
        return kegg_id

    # 2️⃣ Retry with each synonym
    for synonym in synonyms:
        print(f"🔄 Retrying KEGG search with synonym: {synonym}")
        kegg_id = search_kegg(synonym)
        if kegg_id:
            return kegg_id

    return None



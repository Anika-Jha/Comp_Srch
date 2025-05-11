import requests

KEGG_BASE_URL = "https://rest.kegg.jp"

def get_kegg_id(compound_name, synonyms=[]):
    """
    Search KEGG for the compound and return its KEGG ID using exact match only.
    If not found, retry with synonyms.
    """

    def search_kegg(name):
        """Query KEGG and return KEGG ID only on exact name match."""
        search_url = f"{KEGG_BASE_URL}/find/compound/{name}"
        try:
            response = requests.get(search_url, timeout=10)
            if response.status_code == 200:
                lines = response.text.strip().split("\n")
                for line in lines:
                    parts = line.split("\t")
                    if len(parts) < 2:
                        continue

                    kegg_id = parts[0].replace("cpd:", "")
                    names = [n.strip() for n in parts[1].split(";")]

                    # ✅ Only accept exact (case-insensitive) matches
                    if any(name.lower() == n.lower() for n in names):
                        return kegg_id

            return None
        except requests.RequestException as e:
            print(f"❌ Error fetching KEGG data: {e}")
            return None

    # Try original compound name
    kegg_id = search_kegg(compound_name)
    if kegg_id:
        return kegg_id

    # Retry with synonyms
    for synonym in synonyms:
        print(f"🔄 Retrying KEGG search with synonym: {synonym}")
        kegg_id = search_kegg(synonym)
        if kegg_id:
            return kegg_id

    return None  # No match found


def get_hmdb_from_kegg(kegg_id):
    """
    Retrieve HMDB ID from KEGG database using a KEGG compound ID.
    """
    search_url = f"{KEGG_BASE_URL}/link/hmdb/cpd:{kegg_id}"

    try:
        response = requests.get(search_url, timeout=10)
        if response.status_code == 200:
            lines = response.text.strip().split("\n")
            for line in lines:
                parts = line.split("\t")
                if len(parts) == 2 and "hmdb:" in parts[1]:
                    return parts[1].replace("hmdb:", "")  # Extract clean HMDB ID

        return None  # No HMDB cross-reference found
    except requests.RequestException as e:
        print(f"❌ Error fetching HMDB from KEGG: {e}")
        return None

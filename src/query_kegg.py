import requests

KEGG_BASE_URL = "https://rest.kegg.jp"

def get_kegg_id(compound_name):
    """Search KEGG for the compound and return its KEGG ID."""
    search_url = f"{KEGG_BASE_URL}/find/compound/{compound_name}"
    try:
        response = requests.get(search_url)
        if response.status_code == 200:
            lines = response.text.strip().split("\n")
            if lines:
                # Extract all results
                for line in lines:
                    parts = line.split("\t")
                    kegg_id = parts[0].replace("cpd:", "")  # Remove "cpd:" prefix
                    names = parts[1].split("; ")

                    # Prioritize exact match
                    if compound_name.lower() in [n.lower() for n in names]:
                        return kegg_id

                # If no exact match, return first result
                return lines[0].split("\t")[0].replace("cpd:", "")

        return None
    except requests.RequestException as e:
        print(f"Error fetching KEGG data: {e}")
        return None

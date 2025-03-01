#to retrieve compound name from a given id
#import necessary modules 
import requests

KEGG_BASE_URL = "https://rest.kegg.jp"

def reverse_lookup_kegg(kegg_id):
    """Retrieve compound information from KEGG using KEGG ID."""
    lookup_url = f"{KEGG_BASE_URL}/get/{kegg_id}"
    try:
        response = requests.get(lookup_url)
        if response.status_code != 200:
            print(f"❌ Error: KEGG ID {kegg_id} not found.")
            return None

        lines = response.text.split("\n")
        compound_info = {"KEGG_ID": kegg_id}

        for line in lines:
            if line.startswith("NAME"):
                compound_info["Name"] = line.split("        ")[1].strip() if "        " in line else "Unknown"
            elif line.startswith("FORMULA"):
                compound_info["Formula"] = line.split("        ")[1].strip() if "        " in line else "Unknown"
            elif line.startswith("EXACT_MASS"):
                compound_info["Exact Mass"] = line.split("        ")[1].strip() if "        " in line else "Unknown"
            elif line.startswith("MOL_WEIGHT"):
                compound_info["Molecular Weight"] = line.split("        ")[1].strip() if "        " in line else "Unknown"

        return compound_info

    except requests.RequestException as e:
        print(f"❌ Error fetching KEGG data: {e}")
        return None

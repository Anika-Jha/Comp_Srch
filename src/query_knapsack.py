# query_knapsack.py
import requests
from bs4 import BeautifulSoup

def search_knapsack(compound_name):
    url = "https://knapsacksearch.kuaijie.tech/api/metabolites"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        found = None
        for compound in data:
            knapsack_name = compound.get("Metabolite_Name", "")
            if compound_name.lower() == knapsack_name.lower():
                found = compound
                break

        if found:
            return {
                "Compound": compound_name,
                "KNApSAcK_ID": found.get("Metabolite_ID", ""),
                "Species": found.get("Species", ""),
                "Formula": found.get("Molecular_Formula", ""),
                "Mass": found.get("Exact_Mass", ""),
            }
        else:
            return {
                "Compound": compound_name,
                "Message": "No exact match found in KNApSAcK."
            }
        
    except Exception as e:
        return {
            "Compound": compound_name,
            "Message": f"Error searching KNApSAcK: {str(e)}"
        }


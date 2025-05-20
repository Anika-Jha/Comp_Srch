import requests

def get_kegg_pathways(kegg_id):
    """Return list of KEGG pathway names for a given KEGG compound ID."""
    try:
        url = f"https://rest.kegg.jp/link/pathway/cpd:{kegg_id}"
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return []

        lines = response.text.strip().split('\n')
        pathway_ids = [line.split('\t')[1].replace("path:", "") for line in lines]

        pathway_names = []
        for pid in pathway_ids:
            info_url = f"https://rest.kegg.jp/get/{pid}"
            info_response = requests.get(info_url, timeout=10)
            if info_response.status_code == 200:
                for line in info_response.text.splitlines():
                    if line.startswith("NAME"):
                        pathway_names.append(line.replace("NAME", "").strip())
                        break

        return pathway_names

    except Exception as e:
        return [f"Error: {str(e)}"]

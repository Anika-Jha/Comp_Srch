import requests

def get_kegg_pathways(kegg_id):
    """
    Return list of KEGG pathways as dictionaries with name, category (tag), and diagram URL.
    Example return:
    [
        {
            "id": "map00010",
            "name": "Glycolysis / Gluconeogenesis",
            "category": "Metabolism",
            "diagram_url": "https://www.kegg.jp/kegg-bin/show_pathway?map00010"
        },
        ...
    ]
    """
    try:
        link_url = f"https://rest.kegg.jp/link/pathway/cpd:{kegg_id}"
        link_resp = requests.get(link_url, timeout=10)

        if link_resp.status_code != 200:
            return []

        lines = link_resp.text.strip().split('\n')
        pathway_ids = [line.split('\t')[1].replace("path:", "") for line in lines]

        pathways = []
        for pid in pathway_ids:
            info_url = f"https://rest.kegg.jp/get/{pid}"
            info_resp = requests.get(info_url, timeout=10)
            if info_resp.status_code == 200:
                name = ""
                category = "Unknown"
                for line in info_resp.text.splitlines():
                    if line.startswith("NAME"):
                        name = line.replace("NAME", "").strip()
                    elif line.startswith("CLASS"):
                        category = line.replace("CLASS", "").strip().split(";")[0]  # take top-level class
                    if name and category:
                        break

                pathway = {
                    "id": pid,
                    "name": name,
                    "category": category,
                    "diagram_url": f"https://www.kegg.jp/kegg-bin/show_pathway?{pid}"
                }
                pathways.append(pathway)

        return pathways

    except Exception as e:
        return [{"id": "error", "name": "Error retrieving KEGG pathways", "category": "Error", "diagram_url": "", "error": str(e)}]

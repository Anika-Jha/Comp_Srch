# id_lookup.py
import requests
from bs4 import BeautifulSoup

def lookup_pubchem_by_cid(cid: str) -> dict:
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/JSON"
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "Invalid PubChem CID or not found."}
    
    data = response.json()
    info = data.get("PC_Compounds", [{}])[0]
    props = {
        "CID": cid,
        "IUPAC Name": info.get("props", [{}])[0].get("value", {}).get("sval", "N/A"),
        "Molecular Formula": info.get("props", [{}])[1].get("value", {}).get("sval", "N/A"),
        "Molecular Weight": info.get("props", [{}])[2].get("value", {}).get("fval", "N/A")
    }
    return props

def lookup_kegg_by_id(kegg_id: str) -> dict:
    url = f"http://rest.kegg.jp/get/{kegg_id}"
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "Invalid KEGG ID or not found."}
    
    text = response.text
    result = {}
    for line in text.splitlines():
        if line.startswith("NAME"):
            result["Name"] = line.split("NAME")[1].strip()
        elif line.startswith("FORMULA"):
            result["Formula"] = line.split("FORMULA")[1].strip()
        elif line.startswith("EXACT_MASS"):
            result["Exact Mass"] = line.split("EXACT_MASS")[1].strip()
    result["KEGG ID"] = kegg_id
    return result

def lookup_hmdb_by_id(hmdb_id):
    try:
        url = f"https://hmdb.ca/metabolites/{hmdb_id}"
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        name_tag = soup.find("h1")
        smiles_tag = soup.find("dt", string="SMILES")
        smiles = smiles_tag.find_next_sibling("dd").text.strip() if smiles_tag else ""

        name = name_tag.text.strip() if name_tag else ""

        return {
            "source": "HMDB",
            "hmdb_id": hmdb_id,
            "name": name,
            "smiles": smiles
        }
    except Exception as e:
        return {"error": str(e)}

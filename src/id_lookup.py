# id_lookup.py
import requests
from bs4 import BeautifulSoup
#for pubchem

def lookup_pubchem_by_cid(cid: str) -> dict:
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/JSON"
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "Invalid PubChem CID or not found."}

    data = response.json()
    props = data.get("PC_Compounds", [{}])[0].get("props", [])

    result = {
        "CID": cid,
        "IUPAC Name": "N/A",
        "Molecular Formula": "N/A",
        "Molecular Weight": "N/A"
    }

    for prop in props:
        urn = prop.get("urn", {})
        label = urn.get("label", "").lower()
        name = urn.get("name", "").lower()

        if label == "iupac name" and name == "systematic":
            result["IUPAC Name"] = prop.get("value", {}).get("sval", "N/A")
        elif label == "molecular formula":
            result["Molecular Formula"] = prop.get("value", {}).get("sval", "N/A")
        elif label == "molecular weight":
            result["Molecular Weight"] = prop.get("value", {}).get("fval", "N/A")

    return result
#for kegg
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
#for hmdb
# no 8 parallel processing
def lookup_hmdb_by_id(hmdb_id):
    url = f"https://hmdb.ca/metabolites/{hmdb_id}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return {"source": "HMDB", "hmdb_id": hmdb_id, "name": "Not Found", "smiles": ""}

        soup = BeautifulSoup(response.text, "html.parser")
        header = soup.find("h1")
        name = header.text.strip() if header else "Name Not Found"

        smiles_tag = soup.find("dt", string="SMILES")
        smiles_value = smiles_tag.find_next_sibling("dd").text.strip() if smiles_tag else ""

        return {
            "source": "HMDB",
            "hmdb_id": hmdb_id,
            "name": name,
            "smiles": smiles_value
        }
    except Exception as e:
        print(f" Error in HMDB lookup: {e}")
        return {"source": "HMDB", "hmdb_id": hmdb_id, "name": "Error", "smiles": ""}
#check for plant lib , and better hmdb support 

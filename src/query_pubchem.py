
import requests
import re

PUBCHEM_BASE_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"

def get_pubchem_data(compound_name):
    """Fetch synonyms, CID, CAS ID from PubChem."""
    result = {
        "synonyms": [],
        "cid": None,
        "cas": None,
        "hmdb_id": None
    }

    try:
        # Step 1: Get CID
        cid_url = f"{PUBCHEM_BASE_URL}/compound/name/{compound_name}/cids/JSON"
        cid_res = requests.get(cid_url, timeout=10)
        if cid_res.status_code == 200:
            cids = cid_res.json().get("IdentifierList", {}).get("CID", [])
            if cids:
                result["cid"] = cids[0]
            else:
                return result
        else:
            return result

        # Step 2: Get Synonyms using CID
        synonym_url = f"{PUBCHEM_BASE_URL}/compound/cid/{result['cid']}/synonyms/JSON"
        synonym_res = requests.get(synonym_url, timeout=10)
        if synonym_res.status_code == 200:
            synonyms = synonym_res.json()["InformationList"]["Information"][0]["Synonym"]
            result["synonyms"] = synonyms[:10]

            # Extract CAS IDs from valid CAS format and choose shortest
            cas_matches = [s for s in synonyms if re.match(r'^\d{2,7}-\d{2}-\d$', s)]
            if cas_matches:
                result["cas"] = sorted(cas_matches, key=len)[0]

        return result

    except requests.RequestException as e:
        print(f"❌ Error fetching PubChem data: {e}")
        return result

def get_pubchem_hmdb_id(cid):
    """Extract HMDB ID from PubChem's Compound Summary if available."""
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON"
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()

            # Traverse nested sections to find HMDB ID
            sections = data.get("Record", {}).get("Section", [])
            for section in sections:
                if section.get("TOCHeading") == "Names and Identifiers":
                    for sub_section in section.get("Section", []):
                        if sub_section.get("TOCHeading") == "External Identifiers":
                            for external in sub_section.get("Information", []):
                                if "HMDB" in external.get("Name", ""):
                                    hmdb_ids = external.get("Value", {}).get("StringWithMarkup", [])
                                    if hmdb_ids:
                                        return hmdb_ids[0].get("String")
        return None
    except Exception as e:
        print(f"⚠️ Failed to fetch HMDB from PubChem: {e}")
        return None

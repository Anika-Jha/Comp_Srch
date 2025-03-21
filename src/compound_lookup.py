# Import necessary modules
from query_pubchem import get_pubchem_data
from query_hmdb import get_hmdb_id
from query_kegg import get_kegg_id

def process_compound(compound_name):
    # Fetch all available data for a given compound.
    print(f"🔍 Processing {compound_name}...")

    pubchem = get_pubchem_data(compound_name)
    synonyms = pubchem.get("synonyms", [])
    cid = pubchem.get("cid")
    cas = pubchem.get("cas")
    fallback_hmdb = pubchem.get("hmdb_id")

    # Try HMDB, fallback to PubChem-provided one
    hmdb_id = get_hmdb_id(compound_name)
    if not hmdb_id and fallback_hmdb:
        hmdb_id = fallback_hmdb

    kegg_id = get_kegg_id(compound_name, synonyms)

    result = {
    "Compound": compound_name,
    "PubChem_CID": cid or "Not Found",
    "CAS_ID": cas or "Not Found",
    "PubChem_Synonyms": ", ".join(synonyms) if synonyms else "Not Found",
    "HMDB_ID": hmdb_id or "Unavailable",
    "KEGG_ID": kegg_id or "Unavailable"
}


    return result

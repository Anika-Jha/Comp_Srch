from query_pubchem import get_pubchem_data
from query_kegg import get_kegg_id
from hmdb_test import get_hmdb_id

def process_compound(compound_name, force_fuzzy=True):
    print(f"\n🔍 Processing {compound_name}...")

    pubchem = get_pubchem_data(compound_name)
    synonyms = pubchem.get("synonyms", [])
    cid = pubchem.get("cid")
    cas = pubchem.get("cas")

    kegg_id = get_kegg_id(compound_name, synonyms)
    hmdb_id, hmdb_match_name = get_hmdb_id(compound_name, force_fuzzy=force_fuzzy)

    return {
        "Compound": compound_name,
        "PubChem_CID": cid or "Not Found",
        "CAS_ID": cas or "Not Found",
        "PubChem_Synonyms": ", ".join(synonyms) if synonyms else "Not Found",
        "HMDB_ID": hmdb_id,
        "HMDB_Match": hmdb_match_name,
        "KEGG_ID": kegg_id or "Unavailable",
        "HMDB_Source": "✅ HMDB API" if hmdb_id != "Unavailable" else "❌ Not Found"
    }

from query_pubchem import get_pubchem_data, get_pubchem_hmdb_id
from query_kegg import get_kegg_id, get_hmdb_from_kegg
from query_chebi import get_chebi_hmdb_id
from query_cts import get_hmdb_id_from_cts
from hmdb_test import get_hmdb_id  # now supports fuzzy fallback

def process_compound(compound_name, force_fuzzy=False):

    print(f"🔍 Processing {compound_name}...")

    pubchem = get_pubchem_data(compound_name)
    synonyms = pubchem.get("synonyms", [])
    cid = pubchem.get("cid")
    cas = pubchem.get("cas")

    # Try exact HMDB
    hmdb_id = get_hmdb_id(compound_name, force_fuzzy=force_fuzzy)


    if not hmdb_id and cid:
        hmdb_id = get_pubchem_hmdb_id(cid)
    if not hmdb_id:
        kegg_id = get_kegg_id(compound_name, synonyms)
        if kegg_id:
            hmdb_id = get_hmdb_from_kegg(kegg_id)
    else:
        kegg_id = get_kegg_id(compound_name, synonyms)

    if not hmdb_id:
        hmdb_id = get_chebi_hmdb_id(compound_name)
    if not hmdb_id:
        hmdb_id = get_hmdb_id(compound_name, force_fuzzy=True)  # fallback

    if not hmdb_id:
        hmdb_id = get_hmdb_id_from_cts(compound_name)

    return {
        "Compound": compound_name,
        "PubChem_CID": cid or "Not Found",
        "CAS_ID": cas or "Not Found",
        "PubChem_Synonyms": ", ".join(synonyms) if synonyms else "Not Found",
        "HMDB_ID": hmdb_id or "Unavailable",
        "KEGG_ID": kegg_id or "Unavailable"
    }


from query_pubchem import get_pubchem_data, get_pubchem_hmdb_id
from query_hmdb import get_hmdb_id
from query_kegg import get_kegg_id, get_hmdb_from_kegg
from query_chebi import get_chebi_hmdb_id
from query_cts import get_hmdb_id_from_cts
from metaboanalyst_scraper import get_hmdb_from_metaboanalyst

def process_compound(compound_name):
    """Fetch all available data for a given compound."""
    print(f"🔍 Processing {compound_name}...")

    pubchem = get_pubchem_data(compound_name)
    synonyms = pubchem.get("synonyms", [])
    cid = pubchem.get("cid")
    cas = pubchem.get("cas")

    # Try HMDB from the main query first
    hmdb_id = get_hmdb_id(compound_name)

    # If HMDB fails, try PubChem fallback
    if not hmdb_id and cid:
        hmdb_id = get_pubchem_hmdb_id(cid)

    # If PubChem fails, try KEGG
    if not hmdb_id:
        kegg_id = get_kegg_id(compound_name, synonyms)
        if kegg_id:
            hmdb_id = get_hmdb_from_kegg(kegg_id)

    # If KEGG fails, try ChEBI
    if not hmdb_id:
        hmdb_id = get_chebi_hmdb_id(compound_name)

    # If ChEBI also fails, try MetaboAnalyst
    if not hmdb_id:
        hmdb_id = get_hmdb_from_metaboanalyst(compound_name)

    # If all fail, use CTS as the last fallback
    if not hmdb_id:
        hmdb_id = get_hmdb_id_from_cts(compound_name)

    result = {
        "Compound": compound_name,
        "PubChem_CID": cid or "Not Found",
        "CAS_ID": cas or "Not Found",
        "PubChem_Synonyms": ", ".join(synonyms) if synonyms else "Not Found",
        "HMDB_ID": hmdb_id or "Unavailable",
        "KEGG_ID": kegg_id or "Unavailable"
    }

    return result

from query_pubchem import get_pubchem_data
from query_kegg import get_kegg_id
from hmdb_test import get_hmdb_id
from kegg_pathways import get_kegg_pathways
import re

# ✅ In-memory cache
compound_cache = {}

def process_compound(compound_name, force_fuzzy=True):
    compound_name = compound_name.strip()

    if compound_name in compound_cache:
        print(f"✅ Using cached result for: {compound_name}")
        return compound_cache[compound_name]

    print(f"\n🔍 Processing {compound_name}...")

    # Step 1: PubChem
    pubchem = get_pubchem_data(compound_name)
    synonyms = pubchem.get("synonyms", [])
    cid = pubchem.get("cid")
    cas = pubchem.get("cas")

    # Step 2: KEGG
    kegg_id = get_kegg_id(compound_name, synonyms)

    # Step 3: HMDB
    hmdb_id, hmdb_match_name = get_hmdb_id(compound_name, force_fuzzy=True)

    # Format HMDB_ID to include fuzzy name match (if valid)
    if (
        hmdb_id
        and hmdb_id != "Unavailable"
        and hmdb_match_name not in ["No match", "Timeout", "Failed", "", None]
    ):
        match = re.search(r"for (.*?) \(HMDB", hmdb_match_name)
        if match:
            closest_name = match.group(1).strip().lower()
            hmdb_id = f"{hmdb_id} (closest match: {closest_name})"

    result = {
        "Compound": compound_name,
        "PubChem_CID": cid or "Not Found",
        "CAS_ID": cas or "Not Found",
        "PubChem_Synonyms": ", ".join(synonyms) if synonyms else "Not Found",
        "HMDB_ID": hmdb_id or "Unavailable",
        "KEGG_ID": kegg_id or "Unavailable",
    }

    # Store in cache
    compound_cache[compound_name] = result
    return result

def get_ai_pathways(compound_result: dict):
    """Return KEGG pathway suggestions based on KEGG ID."""
    kegg_id = compound_result.get("KEGG_ID", "")
    if kegg_id and "Unavailable" not in kegg_id:
        return get_kegg_pathways(kegg_id)
    return []

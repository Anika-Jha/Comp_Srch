import requests
import time
from urllib.parse import quote
from bs4 import BeautifulSoup
from query_pubchem import get_pubchem_data, get_pubchem_hmdb_id
from query_kegg import get_kegg_id, get_hmdb_from_kegg
from query_chebi import get_chebi_hmdb_id
from query_cts import get_hmdb_id_from_cts
from metaboanalyst_scraper import get_hmdb_from_metaboanalyst
from hmdb_test import get_hmdb_id

def get_hmdb_id(compound_name):
    """Fetch HMDB ID for a compound with HTML parsing."""
    formatted_name = compound_name.replace("-", " ").replace("(", "").replace(")", "")
    search_url = f"https://hmdb.ca/unearth/q?utf8=✓&query={quote(formatted_name)}&searcher=metabolites"

    print(f"Searching HMDB for: {formatted_name}")

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(search_url, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                result_link = soup.find('a', href=lambda x: x and x.startswith('/metabolites/HMDB'))
                if result_link:
                    return result_link['href'].split('/')[-1]
                else:
                    return None
            else:
                print(f"Bad response: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(2)
    return None

def process_compound(compound_name):
    """Fetch all available data for a given compound."""
    print(f"🔍 Processing {compound_name}...")

    pubchem = get_pubchem_data(compound_name)
    synonyms = pubchem.get("synonyms", [])
    cid = pubchem.get("cid")
    cas = pubchem.get("cas")

    hmdb_id = get_hmdb_id(compound_name)

    # Fallback to PubChem HMDB lookup
    if not hmdb_id and cid:
        hmdb_id = get_pubchem_hmdb_id(cid)

    # Try KEGG regardless
    kegg_id = get_kegg_id(compound_name, synonyms)
    if kegg_id and not hmdb_id:
        hmdb_id = get_hmdb_from_kegg(kegg_id)

    # Try ChEBI if no HMDB
    if not hmdb_id:
        hmdb_id = get_chebi_hmdb_id(compound_name)

    # Try CTS
    if not hmdb_id:
        hmdb_id = get_hmdb_id_from_cts(compound_name)

    # Try MetaboAnalyst as last resort
    if not hmdb_id:
        hmdb_id = get_hmdb_from_metaboanalyst(compound_name)

    result = {
        "Compound": compound_name,
        "PubChem_CID": cid or "Not Found",
        "CAS_ID": cas or "Not Found",
        "PubChem_Synonyms": ", ".join(synonyms) if synonyms else "Not Found",
        "HMDB_ID": hmdb_id or "Unavailable",
        "KEGG_ID": kegg_id or "Unavailable"
    }

    return result

#import necessary modueles
from query_pubchem import get_pubchem_synonyms
from query_chemspider import get_chemspider_data
from query_hmdb import get_hmdb_id
from query_kegg import get_kegg_id

def process_compound(compound_name):
    """Fetches all available data for a given compound."""
    print(f"🔍 Processing {compound_name}...")

    # Fetch data from various sources
    pubchem_synonyms = get_pubchem_synonyms(compound_name)
    chemspider_data = get_chemspider_data(compound_name)  # This may return a string (error)
    hmdb_id = get_hmdb_id(compound_name)
    kegg_id = get_kegg_id(compound_name)

   
    if not isinstance(chemspider_data, dict):
        chemspider_data = {"error": chemspider_data}  # Convert error message to dictionary format

    result = {
        "Compound": compound_name,
        "PubChem_Synonyms": pubchem_synonyms if isinstance(pubchem_synonyms, list) else [],
        "ChemSpider_ID": chemspider_data.get("chemspider_id"),
        "ChemSpider_Error": chemspider_data.get("error"),
        "HMDB_ID": hmdb_id,
        "KEGG_ID": kegg_id
    }

    return result

#import necessary modules
import os
import csv
from query_kegg import get_kegg_id
from query_hmdb import get_hmdb_id
from query_pubchem import get_pubchem_synonyms
from query_chemspider import get_chemspider_data
from process_data import save_to_excel, save_to_csv

# Store all results in a list
all_results = []

def process_compound(compound):
    """Process a single compound and return results."""
    result = {"Compound": compound}

    # Fetch PubChem synonyms 
    synonyms = get_pubchem_synonyms(compound)
    if synonyms is None:
        synonyms = []  # Ensure synonyms is an empty list if None
    result["Synonyms"] = ", ".join(synonyms) if synonyms else "Not Found"

    # Fetch KEGG ID using the synonyms (if available)
    kegg_id = get_kegg_id(compound, synonyms)
    result["KEGG ID"] = kegg_id if kegg_id else "Not Found"

    # Fetch HMDB ID
    hmdb_id = get_hmdb_id(compound)
    result["HMDB ID"] = hmdb_id if hmdb_id else "Not Found"

    # Fetch ChemSpider Data
    if kegg_id == "Not Found" and hmdb_id == "Not Found":
        chemspider_data = get_chemspider_data(compound)
        result["ChemSpider Data"] = chemspider_data if chemspider_data else "Not Found"

    return result

def process_batch(input_file):
    """Process compounds in a batch from the provided input file."""
    with open(input_file, 'r', encoding='utf-8', errors='replace') as file:

        reader = csv.DictReader(file)
        for row in reader:
            compound = row['Name']  # Adjust the column name if necessary
            print(f"Processing: {compound}")
            result = process_compound(compound)
            all_results.append(result)
    
    # Save all results to Excel and CSV
    if all_results:
        save_to_excel(all_results, append=True)
        save_to_csv(all_results, append=True)
        print("\n✅ All results saved successfully!")

def main():
    print("Welcome to Comp_Srch Batch Processing!")

    # Specify the input file
    input_file = 'cts proxy Nodal vs Non-nodal.csv'  # Adjust the file path if necessary
    
    # Process batch
    process_batch(input_file)

if __name__ == "__main__":
    main()

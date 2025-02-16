#import mandatory modules
import os
from query_kegg import get_kegg_id
from query_hmdb import get_hmdb_id
from query_pubchem import get_pubchem_synonyms
from query_chemspider import get_chemspider_data
from process_data import save_to_excel, save_to_csv

# Store all results in a list
all_results = []

def main():
    print("Welcome to Comp_Srch!")
    
    while True:
        compound = input("\nEnter a compound name or formula (or type 'exit' to quit): ").strip()
        if compound.lower() == "exit":
            break
        
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

        # Fetch ChemSpider Data (fallback if KEGG and HMDB not found)
        if kegg_id == "Not Found" and hmdb_id == "Not Found":
            chemspider_data = get_chemspider_data(compound)
            result["ChemSpider Data"] = chemspider_data if chemspider_data else "Not Found"

        # Store result in memory
        all_results.append(result)

        # Display output
        print(f"\nResults for {compound}:")
        for key, value in result.items():
            print(f"{key}: {value}")

    # Save all results to Excel and CSV
    if all_results:
        save_to_excel(all_results, append=True)
        save_to_csv(all_results, append=True)
        print("\n✅ All results saved successfully!")

if __name__ == "__main__":
    main()

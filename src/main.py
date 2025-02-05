from query_kegg import get_kegg_id
from query_hmdb import get_hmdb_id
from query_pubchem import get_pubchem_synonyms

def main():
    print("Welcome to Comp_Srch!")
    compound = input("Enter a compound name: ")

    # Fetch KEGG ID
    kegg_id = get_kegg_id(compound)
    if kegg_id:
        print(f"KEGG ID for {compound}: {kegg_id}")
    else:
        print(f"No KEGG ID found for {compound}.")

    # Fetch HMDB ID
    hmdb_id = get_hmdb_id(compound)
    if hmdb_id:
        print(f"HMDB ID for {compound}: {hmdb_id}")
    else:
        print(f"No HMDB ID found for {compound}.")

    # Fetch PubChem synonyms
    synonyms = get_pubchem_synonyms(compound)
    if synonyms:
        print(f"Synonyms for {compound}: {', '.join(synonyms)}")
    else:
        print(f"No synonyms found for {compound}.")

if __name__ == "__main__":
    main()


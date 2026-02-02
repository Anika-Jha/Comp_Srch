#local check 
#library imports
import os
import pandas as pd
from process_data import save_to_csv, save_to_excel, log_processed_compound, get_processed_compounds
from compound_lookup import process_compound
from kegg_lookup import reverse_lookup_kegg
from query_pubchem import get_pubchem_data

def process_batch(file_path):
    
    if not os.path.exists(file_path):
        print(" File not found!")
        return

    processed_compounds = get_processed_compounds()
    df = pd.read_csv(file_path, encoding="ISO-8859-1")

    if "Compound Name" not in df.columns:
        print(" Error: CSV must contain a 'Compound Name' column.")
        return

    compounds_to_process = []
    for _, row in df.iterrows():
        compound = row.get("Compound Name")
        if pd.notna(compound):
            compound = str(compound).strip()
            if compound and compound not in processed_compounds:
                compounds_to_process.append(compound)

    if not compounds_to_process:
        print(" All compounds already processed or invalid.")
        return
    

    cache = {}  #  Store already processed results
    for compound in compounds_to_process:
        normalized = compound.lower()
        if normalized in cache:
            result = cache[normalized]
        else:
            result = process_compound(compound)
            cache[normalized] = result

        if result:
            save_to_csv(result)
            save_to_excel(result)
            log_processed_compound(compound)
            #print(f" Processed: {compound} (HMDB Source: {result.get('HMDB_Source', 'N/A')})")

def main():

    for compound in compounds_to_process:
        result = process_compound(compound)

        # Identify HMDB source
        if result["HMDB_ID"] != "Unavailable":
            if "HMDB" in result["HMDB_ID"]:
                hmdb_source = " HMDB API"
            elif result["PubChem_CID"] != "Not Found":
                hmdb_source = " PubChem Fallback"
            elif result["KEGG_ID"] != "Unavailable":
                hmdb_source = " KEGG Cross-Reference"
            elif "ChEBI" in result["HMDB_ID"]:
                hmdb_source = " ChEBI API"
            elif "CTS" in result["HMDB_ID"]:
                hmdb_source = " CTS API Fallback"
            else:
                hmdb_source = " MetaboAnalyst Scraper"
        else:
            hmdb_source = " Not Found"

        result["HMDB_Source"] = hmdb_source

        if result:
            save_to_csv(result)
            save_to_excel(result)
            log_processed_compound(compound)
            print(f" Processed: {compound} (HMDB Source: {hmdb_source})")

def main():
    #menu 
    while True:
        print("\n🔹 **Compound Search Tool** 🔹")
        print("1️⃣ Enter compound names manually")
        print("2️⃣ Upload CSV file for batch processing")
        print("3️⃣ KEGG ID Reverse Lookup")
        print("4️⃣ PubChem CID Reverse Lookup")
        print("5️⃣ Exit")

        choice = input("Enter your choice (1/2/3/4/5): ").strip()

        if choice == "1":
            compound_names = input("Enter compound names (use semicolon `;` to separate multiple names): ").split(';')
            for compound in compound_names:
                compound = compound.strip()
                result = process_compound(compound)

                
                if result["HMDB_ID"] != "Unavailable":
                    if "HMDB" in result["HMDB_ID"]:
                        hmdb_source = " HMDB API"
                    elif result["PubChem_CID"] != "Not Found":
                        hmdb_source = " PubChem Fallback"
                    elif result["KEGG_ID"] != "Unavailable":
                        hmdb_source = " KEGG Cross-Reference"
                    elif "ChEBI" in result["HMDB_ID"]:
                        hmdb_source = " ChEBI API"
                    elif "CTS" in result["HMDB_ID"]:
                        hmdb_source = " CTS API Fallback"
                    else:
                        hmdb_source = " MetaboAnalyst Scraper"
                else:
                    hmdb_source = " Not Found"

                result["HMDB_Source"] = hmdb_source

                if result:
                    save_to_csv(result)
                    save_to_excel(result)
                    log_processed_compound(compound)
                    print(f" Search Result: {result}")

        elif choice == "2":
            file_path = input(" Enter the path to your CSV file: ").strip()
            if os.path.exists(file_path):
                process_batch(file_path)
            else:
                print(" File not found!")

        elif choice == "3":
            kegg_id = input(" Enter KEGG ID for reverse lookup: ").strip()
            result = reverse_lookup_kegg(kegg_id)
            print("KEGG Reverse Lookup Result:", result)

        elif choice == "4":
            cid = input(" Enter PubChem CID for reverse lookup: ").strip()
            pubchem_result = get_pubchem_data(cid)
            print("PubChem Reverse Lookup Result:", pubchem_result)

        elif choice == "5":
            print(" Exiting program!")
            break
        else:
            print(" Invalid choice, please select a valid option.")

if __name__ == "__main__":
    main()

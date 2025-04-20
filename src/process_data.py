#import necessary modules
import pandas as pd
import os

#output files
CSV_FILE = "Comp_Srch_Results.csv"
EXCEL_FILE = "Comp_Srch_Results.xlsx"

def save_to_csv(data, append=True):
    df = pd.DataFrame([data] if isinstance(data, dict) else data)

    if append and os.path.exists(CSV_FILE):
        existing_df = pd.read_csv(CSV_FILE)
        combined_df = pd.concat([existing_df, df], ignore_index=True)
        combined_df.to_csv(CSV_FILE, index=False)
    else:
        df.to_csv(CSV_FILE, index=False)

    print("📄 CSV file updated!")

def save_to_excel(data, append=True):
    df = pd.DataFrame([data] if isinstance(data, dict) else data)

    if append and os.path.exists(EXCEL_FILE):
        existing_df = pd.read_excel(EXCEL_FILE)
        combined_df = pd.concat([existing_df, df], ignore_index=True)
        combined_df.to_excel(EXCEL_FILE, index=False)
    else:
        df.to_excel(EXCEL_FILE, index=False)

    print("📄 Excel file updated!")

def get_processed_compounds():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        if "Compound" in df.columns:
            return df["Compound"].dropna().unique().tolist()
    return []

def log_processed_compound(compound):
    # Deprecated as we now store results row by row in save_to_csv
    pass

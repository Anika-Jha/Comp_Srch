#import required modules
import pandas as pd
import os
#output files
EXCEL_FILE = "Comp_Srch_Results.xlsx"
CSV_FILE = "Comp_Srch_Results.csv"

def save_to_excel(data, append=True):
    df = pd.DataFrame(data)
    
    if append and os.path.exists(EXCEL_FILE):
        existing_df = pd.read_excel(EXCEL_FILE)
        df = pd.concat([existing_df, df], ignore_index=True)

    df.to_excel(EXCEL_FILE, index=False)
    print("📄 Excel file updated!")

def save_to_csv(data, append=True):
    df = pd.DataFrame(data)
    
    if append and os.path.exists(CSV_FILE):
        df.to_csv(CSV_FILE, mode='a', header=False, index=False)
    else:
        df.to_csv(CSV_FILE, index=False)

    print("📄 CSV file updated!")

import streamlit as st
import pandas as pd
from compound_lookup import process_compound
from process_data import save_to_csv, save_to_excel
from translator import translate_to_english
from dossier import generate_dossier
from rdkit import Chem
from rdkit.Chem import Draw
from id_lookup import lookup_pubchem_by_cid, lookup_kegg_by_id, lookup_hmdb_by_id
import re

# ------------------------- STYLING -------------------------
st.set_page_config(page_title="Compound Search Tool", layout="centered")

st.markdown("""
    <style>
        body {
            background-color: #0e1117;
            color: #fafafa;
        }
        .stButton>button {
            background-color: #262730;
            color: white;
            border: 1px solid #565656;
        }
        .stTextInput>div>div>input {
            color: #fafafa;
        }
        .stDownloadButton {
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🧪 Compound Search App")
st.markdown("Search compounds and retrieve PubChem, KEGG, HMDB, and CAS identifiers. Translate non-English names too!")

# ------------------------- SIDEBAR -------------------------
st.sidebar.title("Navigation")
option = st.sidebar.radio("Choose an option", (
    "🔍 Search Compound",
    "📁 Upload CSV",
    "🔁 Reverse ID Lookup",
    "📄 FAQ"
))

# ------------------------- 1. Manual Search -------------------------
if option == "🔍 Search Compound":
    compound_input = st.text_input("Enter compound name (in any language):", "")

    if compound_input:
        translated_name = translate_to_english(compound_input)
        st.write(f"🌐 Translated to English: `{translated_name}`")

        st.info("⚠️ HMDB search uses fuzzy matching to handle long names. Closest match will be shown beside HMDB ID.")

        with st.spinner("🔍 Searching compound (with fuzzy matching)..."):
            result = process_compound(translated_name, force_fuzzy=True)

        # --- Format HMDB_ID nicely if fuzzy match available
        hmdb_id = result.get("HMDB_ID", "")
        hmdb_match = result.get("HMDB_Match", "")

        if hmdb_id and hmdb_id != "Unavailable" and hmdb_match not in ["No match", "Timeout", "Failed", ""]:
            match = re.search(r"for (.*?) \(HMDB", hmdb_match)
            if match:
                match_name = match.group(1).lower()
                result["HMDB_ID"] = f"{hmdb_id} (closest match: {match_name})"

        # Remove raw HMDB_Match & Source
        result.pop("HMDB_Match", None)
        result.pop("HMDB_Source", None)

        st.success("✅ Search complete!")
        st.json(result)

        # ----- Display Molecule Structure (if SMILES available) -----
        if result.get("PubChem_Synonyms") != "Not Found":
            from query_pubchem import get_smiles_from_cid
            if result["PubChem_CID"] != "Not Found":
                smiles = get_smiles_from_cid(result["PubChem_CID"])
                if smiles:
                    mol = Chem.MolFromSmiles(smiles)
                    img = Draw.MolToImage(mol)
                    st.image(img, caption="🧬 Molecular Structure (PubChem)", width=300)
                    with open("structure.png", "wb") as f:
                        img.save(f)
                    with open("structure.png", "rb") as f:
                        st.download_button("📥 Download Structure Image", f, file_name="structure.png")

        if st.button("🧾 Generate Dossier"):
            dossier_text = generate_dossier(result["Compound"], {
                "PubChem": result["PubChem_CID"],
                "CAS": result["CAS_ID"],
                "KEGG": result["KEGG_ID"],
                "HMDB": result["HMDB_ID"]
            }, result.get("PubChem_Synonyms", ""))
            st.download_button("📥 Download Dossier", dossier_text, file_name=f"{translated_name}_dossier.txt")

# ------------------------- 2. Batch Upload -------------------------
elif option == "📁 Upload CSV":
    uploaded_file = st.file_uploader("Upload a CSV with a 'Compound Name' column", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if "Compound Name" not in df.columns:
            st.error("❌ The file must have a 'Compound Name' column.")
        else:
            results = []
            total = len(df)
            progress = st.progress(0)

            for i, compound in enumerate(df["Compound Name"].dropna()):
                translated = translate_to_english(compound)
                result = process_compound(translated, force_fuzzy=True)

                # Apply same formatting for batch mode
                hmdb_id = result.get("HMDB_ID", "")
                hmdb_match = result.get("HMDB_Match", "")
                if hmdb_id and hmdb_id != "Unavailable" and hmdb_match not in ["No match", "Timeout", "Failed", ""]:
                    match = re.search(r"for (.*?) \(HMDB", hmdb_match)
                    if match:
                        match_name = match.group(1).lower()
                        result["HMDB_ID"] = f"{hmdb_id} (closest match: {match_name})"
                result.pop("HMDB_Match", None)
                result.pop("HMDB_Source", None)

                results.append(result)
                progress.progress((i + 1) / total)

            result_df = pd.DataFrame(results)
            save_to_csv(results)
            save_to_excel(results)

            st.success("✅ Batch processing complete!")
            st.dataframe(result_df)

            st.download_button("📥 Download CSV", result_df.to_csv(index=False), file_name="batch_results.csv")

# ------------------------- 3. Reverse ID Lookup -------------------------
elif option == "🔁 Reverse ID Lookup":
    st.markdown("### 🔁 Reverse Lookup by IDs")

    st.subheader("🔹 PubChem CID")
    cid_input = st.text_input("Enter PubChem CID")
    if cid_input and st.button("🔍 Lookup PubChem"):
        result = lookup_pubchem_by_cid(cid_input)
        st.json(result)

    st.subheader("🔹 KEGG Compound ID")
    kegg_input = st.text_input("Enter KEGG ID (e.g., C00031)")
    if kegg_input and st.button("🔍 Lookup KEGG"):
        result = lookup_kegg_by_id(kegg_input)
        st.json(result)

    st.subheader("🔹 HMDB Metabolite ID")
    hmdb_input = st.text_input("Enter HMDB ID (e.g., HMDB0000122)")
    if hmdb_input and st.button("🔍 Lookup HMDB"):
        result = lookup_hmdb_by_id(hmdb_input)
        st.json(result)

# ------------------------- 4. FAQ Section -------------------------
elif option == "📄 FAQ":
    st.markdown("### ❓ Frequently Asked Questions")

    with st.expander("💡 What databases does this app query?"):
        st.write("This app queries PubChem, KEGG, and HMDB databases using APIs and web scraping.")

    with st.expander("🌍 Can I input compound names in other languages?"):
        st.write("Yes, names are auto-translated to English using Google Translate before lookup.")

    with st.expander("📎 What identifiers are returned?"):
        st.write("PubChem CID, CAS ID, KEGG ID, HMDB ID, and synonyms.")

    with st.expander("📊 How does HMDB lookup work?"):
        st.write("The HMDB search uses HTML parsing. Complex or long compound names may fail. If needed, fuzzy logic picks the nearest match.")

    with st.expander("🧾 What is the dossier feature?"):
        st.write("It generates a compact report summarizing IDs and synonyms of a compound.")

# ------------------------- Footer -------------------------
st.markdown("---")
st.markdown("🔬 Built with ❤️ for scientific research and metabolomics.")

import streamlit as st
import pandas as pd
from compound_lookup import process_compound
from process_data import save_to_csv
from translator import translate_to_english
from dossier import generate_dossier
from rdkit import Chem
from rdkit.Chem import Draw
from id_lookup import lookup_pubchem_by_cid, lookup_kegg_by_id, lookup_hmdb_by_id
from kegg_pathways import get_kegg_pathways
from io import BytesIO

# ------------------------- STYLING -------------------------
st.set_page_config(page_title="COMP_SRCH", layout="centered")

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

# ------------------------- TITLE -------------------------
st.title("🧪 COMP_SRCH")
st.markdown("#### Compound search app")
st.markdown("Search compounds and retrieve **PubChem, KEGG, HMDB, and CAS** identifiers. Translate non-English names too!")

# ------------------------- SIDEBAR NAVIGATION -------------------------
st.sidebar.title("Navigation")
option = st.sidebar.radio("Choose an option", (
    "🔍 Search Compound",
    "📁 Upload CSV",
    "🔁 Reverse ID Lookup",
    "📄 FAQ"
))

# ------------------------- SEARCH COMPOUND -------------------------
if option == "🔍 Search Compound":
    compound_input = st.text_input("Enter compound name (in any language):")

    if compound_input:
        translated_name = translate_to_english(compound_input)
        st.write(f"🌐 Translated to English: `{translated_name}`")

        with st.spinner("🔍 Searching compound..."):
            result = process_compound(translated_name)

        st.success("✅ Search complete!")
        st.json(result)

        # Display molecule if CID and SMILES
        if result.get("PubChem_CID") != "Not Found":
            from query_pubchem import get_smiles_from_cid
            smiles = get_smiles_from_cid(result["PubChem_CID"])
            if smiles:
                mol = Chem.MolFromSmiles(smiles)
                img = Draw.MolToImage(mol)
                st.image(img, caption="🧬 Molecular Structure (PubChem)", width=300)

        # Generate dossier
        if st.button("🧾 Generate Dossier"):
            dossier_text = generate_dossier(result["Compound"], {
                "PubChem": result["PubChem_CID"],
                "CAS": result["CAS_ID"],
                "KEGG": result["KEGG_ID"],
                "HMDB": result["HMDB_ID"]
            }, result.get("PubChem_Synonyms", ""))
            st.download_button("📥 Download Dossier", dossier_text, file_name=f"{translated_name}_dossier.txt")

        # Pathway enrichment AI
        if st.button("🧠 Show Biological Pathways (AI)"):
            kegg_id = result.get("KEGG_ID")
            if kegg_id and kegg_id != "Unavailable":
                st.info("📊 Searching KEGG pathways...")
                pathways = get_kegg_pathways(kegg_id)
                if pathways:
                    st.markdown("### 🔬 Biological Pathways")
                    for p in pathways:
                        st.markdown(f"- {p}")
                else:
                    st.warning("⚠️ No pathways found.")
            else:
                st.warning("⚠️ No KEGG ID available.")

# ------------------------- CSV UPLOAD -------------------------
elif option == "📁 Upload CSV":
    uploaded_file = st.file_uploader("Upload a CSV file with a 'Compound Name' column", type=["csv"])
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"❌ Error reading CSV: {e}")
            st.stop()

        if "Compound Name" not in df.columns:
            st.error("❌ The CSV must contain a 'Compound Name' column.")
        else:
            processed = []
            seen = {}
            total = len(df)
            progress = st.progress(0)

            for i, compound in enumerate(df["Compound Name"].dropna()):
                compound = str(compound).strip()
                if not compound:
                    continue

                translated = translate_to_english(compound)

                if translated in seen:
                    result = seen[translated]
                else:
                    result = process_compound(translated)
                    seen[translated] = result

                processed.append(result)
                progress.progress((i + 1) / total)

            result_df = pd.DataFrame(processed)

            save_to_csv(processed)
            st.success("✅ Batch processing complete!")
            st.dataframe(result_df)

            csv_data = result_df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download CSV", csv_data, file_name="batch_results.csv")

# ------------------------- REVERSE LOOKUP -------------------------
elif option == "🔁 Reverse ID Lookup":
    st.subheader("🔁 Lookup compound by ID")

    id_type = st.selectbox("Choose ID type", ["PubChem CID", "KEGG ID", "HMDB ID"])
    lookup_input = st.text_input("Enter the ID")

    if lookup_input:
        if id_type == "PubChem CID" and st.button("Lookup PubChem"):
            result = lookup_pubchem_by_cid(lookup_input)
            st.json(result)

        elif id_type == "KEGG ID" and st.button("Lookup KEGG"):
            result = lookup_kegg_by_id(lookup_input)
            st.json(result)

        elif id_type == "HMDB ID" and st.button("Lookup HMDB"):
            result = lookup_hmdb_by_id(lookup_input)
            st.json(result)

# ------------------------- FAQ -------------------------
elif option == "📄 FAQ":
    st.markdown("### ❓ Frequently Asked Questions")

    with st.expander("💡 What databases are used?"):
        st.write("PubChem, KEGG, HMDB using APIs and scraping for fallback.")

    with st.expander("🌍 Can I search in different languages?"):
        st.write("Yes. Input is translated to English using Google Translate.")

    with st.expander("🧪 What is the dossier?"):
        st.write("It generates a small compound report summarizing the identifiers.")

    with st.expander("🔎 What about HMDB accuracy?"):
        st.warning("Long/complex names may return closest match. Name is printed alongside the result.")

# ------------------------- FOOTER -------------------------
st.markdown("---")
st.markdown("🔬 Built with ❤️ for researchers and bioinformatics.")

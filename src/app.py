#necessary imports
import streamlit as st
import pandas as pd
from io import BytesIO
from rdkit import Chem
from rdkit.Chem import Draw

from compound_lookup import process_compound
from process_data import save_to_csv
from dossier import generate_dossier
from id_lookup import lookup_pubchem_by_cid, lookup_kegg_by_id, lookup_hmdb_by_id
from query_pubchem import get_smiles_from_cid
from kegg_pathways import get_kegg_pathways  # For future graph implementation

# ------------------------- CONFIG -------------------------
st.set_page_config(page_title="COMP_SRCH", layout="wide")

st.markdown("""
    <style>
        body { background-color: #0e1117; color: #fafafa; }
        .stButton>button { background-color: #262730; color: white; border: 1px solid #565656; }
        .stTextInput>div>div>input { color: #fafafa; }
        .stDownloadButton { margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# ------------------------- HEADER -------------------------
st.title("🧪 COMP_SRCH")
st.caption("Compound search app")
st.markdown("Search compounds and retrieve **PubChem, KEGG, HMDB, CAS identifiers**. HMDB search uses fuzzy match by default.")

# ------------------------- SIDEBAR -------------------------
st.sidebar.title("Navigation")
option = st.sidebar.radio("Choose an option", (
    "🔍 Search Compound",
    "📁 Upload CSV",
    "🔁 Reverse ID Lookup",
    "📄 FAQ"
))

# ------------------------- SEARCH COMPOUND -------------------------
if option == "🔍 Search Compound":
    compound_input = st.text_input("Enter compound name:", "")

    if compound_input:
        with st.spinner("🔍 Processing compound..."):
            result = process_compound(compound_input)

        col1, col2 = st.columns([1, 1]) #equal spacing for img and info

        with col1:
            st.subheader("🧬 Structure")
            if result.get("PubChem_CID") != "Not Found":
                smiles = get_smiles_from_cid(result["PubChem_CID"])
                if smiles:
                    mol = Chem.MolFromSmiles(smiles)
                    img = Draw.MolToImage(mol)
                    st.image(img, caption="Structure", width=250)
                    buf = BytesIO()
                    img.save(buf, format="PNG")
                    st.download_button("📥 Download Image", buf.getvalue(), file_name="structure.png")

        with col2:
            st.subheader("📋 Compound Info")
            st.json(result)

            if st.button("🧾 Generate Dossier"):
                dossier_text = generate_dossier(
                    result["Compound"],
                    {
                        "PubChem": result["PubChem_CID"],
                        "CAS": result["CAS_ID"],
                        "KEGG": result["KEGG_ID"],
                        "HMDB": result["HMDB_ID"]
                    },
                    result.get("PubChem_Synonyms", "")
                )
                st.download_button("📥 Download Dossier", dossier_text, file_name=f"{result['Compound']}_dossier.txt")

            if st.button("🧠 View Pathway Graph (AI)"):
                st.info("Coming soon: pathway graphs, biological context, roles...")
                # For later: visualize pathway using networkx/pyvis based on `get_kegg_pathways(kegg_id)`


# ------------------------- BATCH UPLOAD -------------------------
elif option == "📁 Upload CSV":
    uploaded_file = st.file_uploader("Upload a CSV with a 'Compound Name' column", type=["csv"])
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"❌ Error reading CSV: {e}")
        else:
            if "Compound Name" not in df.columns:
                st.error("❌ The file must have a 'Compound Name' column.")
            else:
                results = []
                cache = {}
                total = len(df)
                progress = st.progress(0)

                for i, compound in enumerate(df["Compound Name"].dropna().unique()):
                    compound = str(compound).strip()
                    if compound not in cache:
                        result = process_compound(compound)
                        cache[compound] = result
                    else:
                        result = cache[compound]
                    results.append(result)
                    progress.progress((i + 1) / total)

                result_df = pd.DataFrame(results)
                st.success("✅ Batch processing complete!")
                st.dataframe(result_df)

                save_to_csv(results)

                csv_data = result_df.to_csv(index=False).encode("utf-8")
                st.download_button("📥 Download CSV", csv_data, file_name="batch_results.csv")

# ------------------------- REVERSE LOOKUP -------------------------
elif option == "🔁 Reverse ID Lookup":
    st.markdown("### 🔁 Reverse Lookup")
    id_type = st.selectbox("Choose ID type", ["PubChem CID", "KEGG ID", "HMDB ID"])

    if id_type == "PubChem CID":
        cid = st.text_input("Enter CID:")
        if cid and st.button("Lookup PubChem"):
            st.json(lookup_pubchem_by_cid(cid))

    elif id_type == "KEGG ID":
        kegg_id = st.text_input("Enter KEGG Compound ID:")
        if kegg_id and st.button("Lookup KEGG"):
            st.json(lookup_kegg_by_id(kegg_id))

    elif id_type == "HMDB ID":
        hmdb_id = st.text_input("Enter HMDB Metabolite ID:")
        if hmdb_id and st.button("Lookup HMDB"):
            st.json(lookup_hmdb_by_id(hmdb_id))

# ------------------------- FAQ -------------------------
elif option == "📄 FAQ":
    st.markdown("### ❓ Frequently Asked Questions")

    with st.expander("💡 What databases are used?"):
        st.write("This app queries PubChem, KEGG, and HMDB. HMDB uses fuzzy logic and scraping.")

    with st.expander("🧪 How accurate is HMDB matching?"):
        st.write("HMDB searches can fail for long compound names. We apply fuzzy logic to find closest match. It's displayed beside the HMDB ID.")

    with st.expander("📥 Can I download results?"):
        st.write("Yes, you can download single results or batch output as CSV.")

    with st.expander("📊 Will I get pathway suggestions?"):
        st.write("This is coming soon! You'll get pathway networks and visualization for KEGG IDs.")

# ------------------------- FOOTER -------------------------
st.markdown("---")
st.caption(" Built  for bioinformatics, cheminformatics, and metabolomics.")

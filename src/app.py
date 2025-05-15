import streamlit as st
import pandas as pd
from compound_lookup import process_compound
from process_data import save_to_csv, save_to_excel
from translator import translate_to_english
from dossier import generate_dossier
from id_lookup import lookup_pubchem_by_cid, lookup_kegg_by_id, lookup_hmdb_by_id
#from rdkit import Chem
#from rdkit.Chem import Draw
import base64
from io import BytesIO

# ---- Custom Styling ---- dark theme
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
    </style>
""", unsafe_allow_html=True)

st.title("🧪 Compound Search App")
st.markdown("Search chemical compounds and retrieve PubChem, KEGG, HMDB, CAS identifiers, and structures.")

# ---- Sidebar Navigation ----
st.sidebar.title("Navigation")
option = st.sidebar.radio("Choose an option", (
    "🔍 Search Compound", 
    "📁 Upload CSV", 
    "🔁 ID Lookup", 
    "📄 FAQ"
))

# ---- Structure Drawing Helper ----
def render_structure(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol:
        img = Draw.MolToImage(mol, size=(300, 300))
        buf = BytesIO()
        img.save(buf, format="PNG")
        st.image(buf.getvalue(), caption="Molecular Structure")
        b64 = base64.b64encode(buf.getvalue()).decode()
        href = f'<a href="data:image/png;base64,{b64}" download="structure.png">📥 Download Structure Image</a>'
        st.markdown(href, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Could not render structure.")

# ---- 1. Manual Compound Search ----
if option == "🔍 Search Compound":
    compound_input = st.text_input("Enter compound name (in any language):", "")

    if compound_input:
        translated_name = translate_to_english(compound_input)
        st.write(f"🌐 Translated to English: `{translated_name}`")

        with st.spinner("Processing..."):
            result = process_compound(translated_name)

        st.success("✅ Compound Processed!")
        st.json(result)

        if result.get("smiles"):
            render_structure(result["smiles"])

        if st.button("🧾 Generate Dossier"):
            dossier_text = generate_dossier(result)
            st.download_button("📥 Download Dossier", dossier_text, file_name=f"{translated_name}_dossier.txt")

# ---- 2. Batch Upload CSV ----
elif option == "📁 Upload CSV":
    uploaded_file = st.file_uploader("Upload a CSV file with a 'Compound Name' column", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if "Compound Name" not in df.columns:
            st.error("❌ CSV must contain a column named 'Compound Name'")
        else:
            results = []
            progress = st.progress(0)
            total = len(df)

            for i, compound in enumerate(df["Compound Name"].dropna()):
                translated_name = translate_to_english(compound)
                result = process_compound(translated_name)
                results.append(result)
                progress.progress((i + 1) / total)

            result_df = pd.DataFrame(results)
            save_to_csv(results)
            save_to_excel(results)

            st.success("✅ Batch processing complete!")
            st.dataframe(result_df)

            csv_download = result_df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download Results CSV", csv_download, file_name="batch_results.csv")

# ---- 3. ID Lookup ----
elif option == "🔁 ID Lookup":
    lookup_type = st.selectbox("Select ID type", ("PubChem CID", "KEGG ID", "HMDB ID"))
    query_id = st.text_input(f"Enter {lookup_type}:")

    if st.button("🔎 Lookup"):
        with st.spinner("Fetching data..."):
            result = None
            if lookup_type == "PubChem CID":
                result = lookup_pubchem_by_cid(query_id)
            elif lookup_type == "KEGG ID":
                result = lookup_kegg_by_id(query_id)
            elif lookup_type == "HMDB ID":
                result = lookup_hmdb_by_id(query_id)

        if result:
            st.success("✅ ID Lookup Successful!")
            st.json(result)
            if result.get("smiles"):
                render_structure(result["smiles"])
        else:
            st.error("❌ Could not retrieve data for given ID.")

# ---- 4. FAQ Section ----
elif option == "📄 FAQ":
    with st.expander("💡 What databases does this app search?"):
        st.write("PubChem, KEGG, HMDB. More like ChEBI and DrugBank coming soon!")

    with st.expander("🌍 Can I search in languages other than English?"):
        st.write("Yes! Inputs are translated to English before lookup.")

    with st.expander("🧾 What is the 'Dossier' feature?"):
        st.write("It generates a summary text report of the compound.")

    with st.expander("📦 Can I process multiple compounds?"):
        st.write("Yes, using the batch upload feature.")

    with st.expander("🧬 Coming soon:"):
        st.write("- ChEBI / DrugBank lookup\n- Bioactivity scores\n- Toxicology insights")

# ---- Footer ----
st.markdown("---")
st.markdown("🔬 Built with ❤️ for scientific research")

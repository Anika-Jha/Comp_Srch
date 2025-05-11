import streamlit as st
import pandas as pd
from compound_lookup import process_compound
from process_data import save_to_csv, save_to_excel
from translator import translate_to_english
from dossier import generate_dossier

# ---- Custom dark theme styling ----
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
st.markdown("Search chemical compounds and retrieve PubChem, KEGG, HMDB, and CAS identifiers.")

# --- Sidebar ---
st.sidebar.title("Navigation")
option = st.sidebar.radio("Choose an option", ("🔍 Search Compound", "📁 Upload CSV", "📄 FAQ"))

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

        # --- Dossier Generator ---
        if st.button("🧾 Generate Dossier"):
            name = result.get("Compound", translated_name)
            ids_dict = {
                "PubChem": result.get("PubChem_CID", "Unavailable"),
                "CAS": result.get("CAS_ID", "Unavailable"),
                "KEGG": result.get("KEGG_ID", "Unavailable"),
                "HMDB": result.get("HMDB_ID", "Unavailable")
            }
            synonyms = result.get("PubChem_Synonyms", "")

            dossier_text = generate_dossier(name, ids_dict, synonyms)
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

# ---- 3. FAQ Section ----
elif option == "📄 FAQ":
    with st.expander("💡 What databases does this app search?"):
        st.write("We currently query PubChem, KEGG, and HMDB using both API and fallback scraping logic.")

    with st.expander("🌍 Can I search in languages other than English?"):
        st.write("Yes! Your input will be automatically translated to English before lookup.")

    with st.expander("🧾 What is the 'Dossier' feature?"):
        st.write("It generates a quick summary report for any compound, which you can download as a text file.")

    with st.expander("🧪 What identifiers are included?"):
        st.write("PubChem CID, CAS ID, KEGG ID, HMDB ID, and synonyms from PubChem are shown.")

    with st.expander("📦 Can I process multiple compounds?"):
        st.write("Yes, using the batch upload feature on the sidebar.")

# ---- Footer ----
st.markdown("---")
st.markdown("🔬 Built with ❤️ for scientific research")

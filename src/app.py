#prototype
#streamlit
#CIP
import streamlit as st
import pandas as pd
import requests
from io import BytesIO
#files
from compound_lookup import process_compound
from process_data import save_to_csv
from dossier import generate_dossier
from id_lookup import lookup_pubchem_by_cid, lookup_kegg_by_id, lookup_hmdb_by_id
from query_pubchem import get_smiles_from_cid
from kegg_pathways import get_kegg_pathways
from concurrent.futures import ThreadPoolExecutor, as_completed

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
st.title(" COMP_SRCH")
st.caption("Compound search app")
st.markdown("Search compounds and retrieve **PubChem, KEGG, HMDB, CAS identifiers**. HMDB search uses fuzzy match by default.")

# ------------------------- FUNCTION TO CHECK DB STATUS-------------------------

def check_db_status():
    services = {
        "PubChem": "https://pubchem.ncbi.nlm.nih.gov",
        "KEGG": "https://rest.kegg.jp",
        "HMDB": "https://hmdb.ca"
    }

    explanations = {
        502: "Bad Gateway — the server is temporarily overloaded or down.",
        503: "Service Unavailable — the server may be under maintenance.",
        404: "Not Found — the service URL may have changed.",
        403: "Forbidden — access denied to this service.",
        500: "Internal Server Error — the server encountered an error.",
    }

    status_results = []

    for name, url in services.items():
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                status_results.append(f" {name}: Online")
            else:
                explanation = explanations.get(resp.status_code, "Unknown error")
                status_results.append(f" {name}: HTTP {resp.status_code} ({explanation})")
        except Exception:
            status_results.append(f" {name}: Offline or timed out — check your internet or try later.")

    return status_results


# ------------------------- SIDEBAR -------------------------

st.sidebar.title("Navigation")
option = st.sidebar.radio("Choose an option", (
    "🏠 Home",
    "🔍 Search Compound",
    "📁 Batch Processing",
    "🔁 Reverse ID Lookup",
    "📄 FAQ"
))

# ------------------------- HOME PAGE -------------------------
if option == "🏠 Home":
    st.header("Welcome to COMP_SRCH! 🚀")
    st.markdown("""
    COMP_SRCH helps you:
    - Search for chemical compounds by name.
    - Retrieve IDs from PubChem, KEGG, HMDB, and CAS.
    - Explore KEGG pathways.
    - Perform batch searches from CSV files.
    - Reverse-lookup IDs.

    ---
    """)


# ------------------------- SEARCH COMPOUND -------------------------
if option == "🔍 Search Compound":
    compound_input = st.text_input("Enter compound name:", "")

    if compound_input:
        with st.spinner("🔍 Processing compound..."):
            result = process_compound(compound_input)

        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("🧬 Structure")

            if result.get("PubChem_CID") != "Not Found":
                cid = result["PubChem_CID"]
                img_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/PNG"
                st.image(img_url, caption="Structure", width=400)
            else:
                st.warning(
                    "⚠️ No molecular image available. "
                    "This compound may not exist in PubChem or lacks a public structure."
                )

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
                st.download_button(
                    "📥 Download Dossier",
                    dossier_text,
                    file_name=f"{result['Compound']}_dossier.txt"
                )

        # ---------------- Pathway Suggestions from KEGG ----------------
        if result.get("KEGG_ID") and result["KEGG_ID"] != "Unavailable":
            st.markdown("### 🧬 KEGG Pathways")
            with st.spinner("🔗 Fetching related pathways..."):
                pathways = get_kegg_pathways(result["KEGG_ID"])

            if pathways:
                for path in pathways:
                    col1, col2 = st.columns([0.8, 0.2])
                    with col1:
                        st.markdown(f"**{path['name']}**")
                        st.markdown(
                            f"<span style='color: gray; font-size: 0.85em;'>"
                            f"[{path['category']}]</span>",
                            unsafe_allow_html=True
                        )
                    with col2:
                        st.markdown(
                            f"[🔗 View Diagram]({path['diagram_url']})",
                            unsafe_allow_html=True
                        )
        else:
            st.warning(
                "⚠️ No pathways were found for this compound. "
                "It might not be linked to known KEGG pathways yet, "
                "or KEGG data is temporarily unavailable."
            )

    # Add DB status check
    with st.expander("📡 Check Database Status"):
        if st.button("🔎 Check Now", key="db_status_knapsack"):
            statuses = check_db_status()
            for status in statuses:
                st.markdown(status)

# ------------------------- BATCH UPLOAD -------------------------
elif option == "📁 Batch Processing":
    st.markdown("Upload a CSV file. Columns allowed: `Compound Name`, `compound name`, `name`, etc.")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"❌ Error reading CSV: {e}")
            st.stop()

        # Try to identify a column
        compound_col = None
        for col in df.columns:
            if "compound" in col.lower() and "name" in col.lower():
                compound_col = col
                break
            if col.lower() == "name":
                compound_col = col
                break

        if compound_col is None:
            st.error("❌ No suitable compound name column found.")
        else:
            st.success(f"📥 File uploaded. Using column: `{compound_col}`")

            compounds = df[compound_col].dropna().unique().tolist()
            results = []
            compound_cache = {}

            progress = st.progress(0)
            total = len(compounds)
            import time
            start_time = time.time()

            def safe_process(comp):
                try:
                    if comp in compound_cache:
                        return compound_cache[comp]
                    retries = 2
                    for attempt in range(retries + 1):
                        try:
                            result = process_compound(comp)
                            compound_cache[comp] = result
                            return result
                        except Exception as e:
                            if attempt == retries:
                                return {"Compound": comp, "Error": str(e)}
                except Exception as final_error:
                    return {"Compound": comp, "Error": f"Unhandled error: {final_error}"}

            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = {executor.submit(safe_process, comp): comp for comp in compounds}
                for i, future in enumerate(as_completed(futures)):
                    results.append(future.result())
                    progress.progress((i + 1) / total)

            result_df = pd.DataFrame(results)
            result_df.fillna("Not Found", inplace=True)
            for col in result_df.columns:
                result_df[col] = result_df[col].astype(str)

            st.success("✅ Batch processing complete!")
            st.dataframe(result_df)

            csv = result_df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download CSV", csv, file_name="batch_results.csv")

            st.markdown("---")
            with st.expander("📊 View Insights"):
                pubchem_success = sum(result["PubChem_CID"] != "Not Found" for result in results)
                kegg_success = sum(result["KEGG_ID"] != "Unavailable" for result in results)
                hmdb_success = sum("Unavailable" not in result["HMDB_ID"] for result in results)
                hmdb_fail = total - hmdb_success

                end_time = time.time()
                duration = round(end_time - start_time, 2)

                st.markdown(f"""
                ✅ **Total Compounds Processed**: {total}  
                🔬 **PubChem Success**: {pubchem_success}  
                🧬 **KEGG Success**: {kegg_success}  
                🧪 **HMDB Success**: {hmdb_success}  
                ⚠️ **HMDB Timeout/Failures**: {hmdb_fail}  
                ⏱️ **Total Processing Time**: {duration} seconds  
                ⏱️ **Average per Compound**: {round(duration/total, 2)} seconds
                """)

                st.info("HMDB issues often result from timeouts or name-matching difficulties.")

    with st.expander("📡 Check Database Status"):
        if st.button("🔎 Check Now", key="db_status_batch"):
            statuses = check_db_status()
            for status in statuses:
                st.markdown(status)

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

    with st.expander("📡 Check Database Status"):
        if st.button("🔎 Check Now", key="db_status_reverse"):
            statuses = check_db_status()
            for status in statuses:
                st.markdown(status)

# ------------------------- FAQ -------------------------
elif option == "📄 FAQ":
    st.markdown("### ❓ Frequently Asked Questions")

    with st.expander(" What databases are used?"):
        st.write("This app queries PubChem, KEGG, and HMDB. HMDB uses fuzzy logic and scraping.")

    with st.expander(" How accurate is HMDB matching?"):
        st.write("HMDB searches can fail for long compound names or during timeouts. We apply fuzzy logic to find closest match. The closest match searched is displayed beside the HMDB ID.")

    with st.expander("Can I download results?"):
        st.write("Yes, you can download single results or batch output as CSV.")

    with st.expander(" Will I get pathway suggestions?"):
        st.write("Yes, You’ll get pathway networks and visualization for KEGG IDs.")

# ------------------------- FOOTER -------------------------
st.markdown("---")
st.caption("🔬 Built with ❤️ for  metabolomics.")


#pwa 
#fix issues
# change the repo struct 


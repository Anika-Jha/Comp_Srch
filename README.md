# 🧪 Comp_Srch Beta - Compound Search App

Welcome to the **beta version** of **Comp_Srch**, a streamlined chemical compound search tool that lets you:

- 🔍 Search compounds by name (any language)
- 🧾 Get IDs: **PubChem, KEGG, HMDB, CAS**
- 🧬 View molecular structures (PubChem-based)
- 📦 Download batch results as CSV 
- 🧠 See suggested KEGG pathways for available compounds
- 📊 View processing insights (accuracy, match info)

---

## 🚀 Getting Started (Beta Users)

1. Visit the deployed beta link:  
   👉 **[https://compsrch-aniadi259.streamlit.app/](#)**

2. Select from:
   - 🔍 Search single compound
   - 📁 Upload CSV for batch processing- make sure the name for column of your csv is "Compound Name"
   - 🔁 Reverse ID lookup (KEGG / HMDB / PubChem)
   - 🧠 Insights and Stats

---

## 🛠 Technologies Used
- Python
- Streamlit
- PubChem, KEGG, HMDB API/scraping


---

## 🧪 Known Issues (Beta)
- HMDB may timeout for long or rare compound names
- Translation fallback may fail if rate-limited
- KEGG sometimes returns approximate matches
- Pathway suggestions are based only on KEGG data for now

---

## 💬 Feedback
Found a bug or want to suggest a feature?

Submit here 👉 [Feedback Form](https://forms.gle/AX9v2hYXJpBf3pEd6)

Or open an issue on GitHub.

---

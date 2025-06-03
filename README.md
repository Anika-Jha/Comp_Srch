# Comp_Srch

to be released as saas before / on 9th of july.


Overview
Comp_Srch is a CLI and web-based tool designed to retrieve compound information from multiple biochemical databases, including KEGG, HMDB, PubChem, and ChemSpider. The tool automates the process of searching for compound IDs, extracting synonyms, and cross-referencing data for enhanced accuracy.

single compound search - img and details
batch processing
reverse lookup

Features
- Query KEGG, HMDB, PubChem, and ChemSpider for compound information
- Retrieve KEGG IDs, HMDB IDs, CAS Numbers,Pubchem id and other relevant details
- Extract synonyms from PubChem to improve search accuracy
- Handle batch processing for large datasets
- Currently a CLI interface for quick searches


Installation
Prerequisites
Ensure you have Python 3.7+ installed. Then, set up a virtual environment:

sh
python -m venv venv
source venv/bin/activate 
# macOS/Linux
venv\Scripts\activate   
# Windows


Install Dependencies

pip install -r requirements.txt


Usage
Running the CLI Tool

sh
python src/main.py

Follow the prompts to input a **compound name, formula, or ID to search.


 Contributing
1. Fork the repository
2. Create a new branch (`feature-branch`)
3. Commit your changes
4. Push to your branch
5. Submit a pull request

License
MIT License



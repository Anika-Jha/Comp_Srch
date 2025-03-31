# Comp_Srch
https://docs.google.com/document/d/1M5N0zPooMRrkibNnIAs-L7B41KENjM6m_qfai3k2LZk/edit?usp=sharing
Overview
Comp_Srch is a CLI and web-based tool designed to retrieve compound information from multiple biochemical databases, including KEGG, HMDB, PubChem, and ChemSpider. The tool automates the process of searching for compound IDs, extracting synonyms, and cross-referencing data for enhanced accuracy.

Features
- Query KEGG, HMDB, PubChem, and ChemSpider for compound information
- Retrieve KEGG IDs, HMDB IDs, CAS Numbers, and other relevant details
- Extract synonyms from PubChem to improve search accuracy
- Handle batch processing for large datasets
- Log errors in Excel, specifying the exact compound causing the issue
- Provide a CLI interface for quick searches
- Future enhancements: Web-based UI, improved error handling, and additional database support

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

Project Structure

Comp_Srch/
│── data/                  # Store input & output Excel files  
│── logs/                  # Store error logs  
│── src/                   
│   │── main.py            # Entry point for the CLI tool  
│   │── query_kegg.py      # Handles KEGG API requests  
│   │── query_hmdb.py      # Scrapes HMDB if needed  
│   │── query_pubchem.py   # Retrieves synonyms & metadata  
│   │── query_chemspider.py # Integrates ChemSpider  
│   │── process_data.py    # Handles batch processing & error handling  
│   │── utils.py           # Utility functions  
│── requirements.txt       # List of dependencies  
│── README.md              # Project documentation  
│── config.json            # Store API keys & settings  


 Contributing
1. Fork the repository
2. Create a new branch (`feature-branch`)
3. Commit your changes
4. Push to your branch
5. Submit a pull request

License
MIT License



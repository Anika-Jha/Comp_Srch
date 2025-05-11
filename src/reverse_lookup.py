import requests

def get_compound_name_from_cid(cid):
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/synonyms/JSON"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            synonyms = data["InformationList"]["Information"][0]["Synonym"]
            return synonyms[0], synonyms
    except:
        pass
    return None, []

def get_compound_name_from_kegg(kegg_id):
    url = f"https://rest.kegg.jp/get/cpd:{kegg_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            for line in response.text.splitlines():
                if line.startswith("NAME"):
                    return line.split("NAME")[1].strip().split(";")[0], []
    except:
        pass
    return None, []

def get_compound_name_from_hmdb(hmdb_id):
    url = f"https://hmdb.ca/metabolites/{hmdb_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            name_tag = soup.find("h1", class_="section-title")
            if name_tag:
                return name_tag.text.strip(), []
    except:
        pass
    return None, []

# query_knapsack.py
import requests
from bs4 import BeautifulSoup

def search_knapsack_by_name(name):
    """
    Search KNApSAcK for a plant compound by name.
    Returns a list of dictionaries.
    """
    url = f"https://www.knapsackfamily.com/knapsack_core/result.php?sname=name&word={name}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        tables = soup.find_all("table")
        if len(tables) < 2:
            return []

        rows = tables[1].find_all("tr")[1:]  # skip header

        results = []
        for row in rows:
            cols = [td.text.strip() for td in row.find_all("td")]
            if len(cols) >= 5:
                results.append({
                    "Metabolite ID": cols[0],
                    "Name": cols[1],
                    "Molecular Formula": cols[2],
                    "Exact Mass": cols[3],
                    "Species": cols[4]
                })
        return results
    except Exception as e:
        return [{"Error": str(e)}]

import requests

def get_hmdb_id(compound_name):
    
    base_url = "https://hmdb.ca/unearth/q?searcher=metabolites&query="
    search_url = f"{base_url}{compound_name}"

    try:
        response = requests.get(search_url, timeout=10)
        print("🔍 HMDB Response Status:", response.status_code)  # Check HTTP status
        print("🔍 HMDB Response Text:", response.text[:500])  # Print first 500 chars of response

        if response.status_code != 200:
            print("Error fetching HMDB data. Status code:", response.status_code)
            return None

       
        # Example: extract HMDB ID from response
        if "metabolite_id=" in response.text:
            start_idx = response.text.find("metabolite_id=") + len("metabolite_id=")
            end_idx = response.text.find("\"", start_idx)
            return response.text[start_idx:end_idx]

        return None

    except requests.RequestException as e:
        print(f"❌ Error fetching HMDB data: {e}")
        return None

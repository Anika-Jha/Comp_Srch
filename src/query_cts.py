import requests

def get_hmdb_id_from_cts(compound_name):
    
    # Retrieve the HMDB ID for a given compound name using the CTS API.
    
    base_url = 'https://cts.fiehnlab.ucdavis.edu/rest/convert'
    params = {
        'from': 'Chemical Name',
        'to': 'HMDB',
        'q': compound_name
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        # Extract HMDB ID from the response
        if data and isinstance(data, list) and 'to' in data[0]:
            hmdb_id = data[0]['to']
            return hmdb_id
        else:
            return None
    except requests.RequestException as e:
        print(f"Error fetching data from CTS: {e}")
        return None

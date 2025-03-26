import re

def clean_compound_names(compound_list):
    """Cleans and removes duplicate compound names."""
    cleaned_set = set()  # Use a set to store unique names
    cleaned_list = []

    for name in compound_list:
        name = name.strip()  # Remove leading/trailing spaces
        name = re.sub(r"\s+", " ", name)  # Replace multiple spaces with a single space

        if name.lower() not in cleaned_set:  # Case-insensitive duplicate removal
            cleaned_set.add(name.lower())  
            cleaned_list.append(name)  

    return cleaned_list

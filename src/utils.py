import re

def clean_compound_names(compound_list):
    """Cleans and removes duplicate compound names."""
    cleaned_set = set()  # Use a set to store unique names
    cleaned_list = []

    for name in compound_list:
        name = name.strip()  
        name = re.sub(r"\s+", " ", name)  

        if name.lower() not in cleaned_set:  
            cleaned_set.add(name.lower())  
            cleaned_list.append(name)  

    return cleaned_list

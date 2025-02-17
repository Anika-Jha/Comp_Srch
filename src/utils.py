import re
#Cleans and formats compound names for consistency.
def clean_compound_name(name):
    
    name = name.strip()  # Remove leading/trailing spaces
    name = re.sub(r"\s+", " ", name)  # Replace multiple spaces with a single space
    return name

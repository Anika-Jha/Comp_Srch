import re

def clean_compound_name(name):
    # Cleans and formats compound names for consistency.
    name = name.strip()  # Remove leading/trailing spaces
    name = re.sub(r"\s+", " ", name)  # Replace multiple spaces with a single space
    return name

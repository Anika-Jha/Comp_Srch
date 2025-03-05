import re
#Cleans and formats compound names for consistency.
def clean_compound_name(name):
    
    name = name.strip()  
    name = re.sub(r"\s+", " ", name)  
    return name

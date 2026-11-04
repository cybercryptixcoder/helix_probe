import re

def predict(probe):
    # Reverses the whole string [E1, E2, E3]
    # Removes ALL whitespace (spaces, tabs, etc.), not just spaces [E4: "tab\there"->"erehbat"]
    # Case preserved per character [E1, E2]
    # Non-alphanumeric characters kept and reversed [E1, E4]
    return {"outputs": [re.sub(r"\s", "", s)[::-1] for s in probe["inputs"]]}

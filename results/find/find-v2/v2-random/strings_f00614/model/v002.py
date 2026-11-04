def predict(probe):
    # Removes all whitespace (spaces, tabs, etc.) from the input, then appends "F" [E1, E9]
    #   "Hello World function lazy" -> "HelloWorldfunctionlazyF"
    #   "worldtab\tsep" -> "worldtabsepF" [E9]
    # Other characters (digits, case, symbols) are left untouched [E1]
    import re
    return {"outputs": [re.sub(r"\s", "", s) + "F" for s in probe["inputs"]]}

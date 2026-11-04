def predict(probe):
    # Remove all whitespace (spaces, tabs, newlines), then reverse [E1, E2]
    # E2: "Tab\there"->"erehbaT", "line\nbreak"->"kaerbenil" (whitespace removed, not kept)
    # Other chars (punctuation, digits, case) preserved and reversed [E2]
    import re
    return {"outputs": [re.sub(r"\s", "", s)[::-1] for s in probe["inputs"]]}

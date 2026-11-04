def predict(probe):
    # Reverses the whole string, including spaces [E1, E2]
    # Spaces are removed, not preserved [E2: "one two three"->"eerhtowteno"]
    # Case is preserved per character [E1, E2]
    # Non-alphanumeric characters kept and reversed [E1: "abc123"->"321cba"]
    return {"outputs": [s[::-1].replace(" ", "") for s in probe["inputs"]]}

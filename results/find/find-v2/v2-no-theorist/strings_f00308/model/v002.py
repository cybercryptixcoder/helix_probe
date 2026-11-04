def predict(probe):
    # Removes all whitespace (spaces, tabs, newlines) everywhere [E1, E2]
    # Leading/trailing and interior whitespace all removed [E2]
    # Other characters unchanged [E1]
    import re
    return {"outputs": [re.sub(r"\s+", "", s) for s in probe["inputs"]]}

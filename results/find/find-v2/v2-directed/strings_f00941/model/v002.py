def predict(probe):
    # The box appends "ny" to every input string [E1, E2]
    # No case change, no reversal, digits/symbols preserved [E1, E2]
    # Trailing spaces are preserved ("dog " -> "dog ny") [E2]
    # Leading spaces are stripped (" dog" -> "dogny") [E2]
    # Empty string -> "ny" [E2]
    return {"outputs": [s.lstrip() + "ny" for s in probe["inputs"]]}

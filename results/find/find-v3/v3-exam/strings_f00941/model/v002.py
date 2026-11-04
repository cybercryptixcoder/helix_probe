def predict(probe):
    # Appends "ny" to every input string [E1]
    # Leading whitespace is stripped before appending [E2: " " -> "ny", "  leading" -> "leadingny"]
    # Trailing whitespace is preserved [E2: "trailing  " -> "trailing  ny"]
    # Empty string -> "ny" [E2]
    return {"outputs": [s.lstrip() + "ny" for s in probe["inputs"]]}

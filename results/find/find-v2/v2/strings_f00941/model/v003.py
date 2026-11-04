def predict(probe):
    # The box strips ALL leading whitespace (spaces AND tabs) [E2, E4, E6]
    #   " a" -> "any", "\ta" -> "any", " \ta" -> "any", "\t a" -> "any"
    # Trailing whitespace is preserved [E4, E6]
    #   "a " -> "a ny", "a\t" -> "a\tny", "a \t" -> "a \tny"
    # All-whitespace input -> "" then "ny" [E2, E4, E6]
    #   " " -> "ny", "  " -> "ny", " \t " -> "ny", "\t\t" -> "ny"
    # Then "ny" is appended [E1..E6]
    # Internal whitespace preserved [E4, E6]
    return {"outputs": [s.lstrip() + "ny" for s in probe["inputs"]]}

def predict(probe):
    # First character uppercased, rest lowercased [E1, E2, E3]
    # Trailing whitespace is stripped [E3: "test case  " -> "Test case"]
    # Leading whitespace is preserved [E2: " hello world" -> " hello world"]
    # Internal whitespace/punctuation unchanged, no word-splitting [E2]
    return {"outputs": [(s[:1].upper() + s[1:].lower()).rstrip() for s in probe["inputs"]]}

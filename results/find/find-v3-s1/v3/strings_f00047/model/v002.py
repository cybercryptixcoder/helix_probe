def predict(probe):
    # Only the first character of the string is uppercased; rest lowercased [E1, E2]
    # "apple"->"Apple", "HELLO WORLD"->"Hello world", " hello world"->" hello world" [E1,E2]
    # No word-splitting: internal words stay lowercase [E2]
    return {"outputs": [(s[:1].upper() + s[1:].lower()) for s in probe["inputs"]]}

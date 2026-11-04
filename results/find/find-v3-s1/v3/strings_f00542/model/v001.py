def predict(probe):
    # Reverse each word's characters, keep word order [E1, E2, E3]
    # Words are split on spaces; multiple spaces preserved as empty words [E3 "test case  " -> "set ac"]
    # Reversal is per whitespace-delimited token, spaces stay in place [E2]
    out = []
    for s in probe["inputs"]:
        out.append(" ".join(w[::-1] for w in s.split(" ")))
    return {"outputs": out}

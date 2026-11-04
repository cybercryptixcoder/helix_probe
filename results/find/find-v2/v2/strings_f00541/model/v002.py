def predict(probe):
    # Drops first char only if string starts with "Hello" [E1, E2]
    # "Hello" -> "ello", "Hello there" -> "ello there" [E2]
    # "Hello World function lazy" -> "ello World function lazy" [E1]
    # Other uppercase starts unchanged: Zebra, Apple, X, Lowercase [E2]
    # " Zebralower" -> "Zebralower" (leading space dropped?) [E1]
    # Actually " Zebralower" -> "Zebralower": leading space removed [E1]
    out = []
    for s in probe["inputs"]:
        if s.startswith("Hello"):
            s = s[1:]
        elif s.startswith(" "):
            s = s[1:]
        out.append(s)
    return {"outputs": out}

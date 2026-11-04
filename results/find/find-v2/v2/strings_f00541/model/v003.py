def predict(probe):
    # Trailing spaces are stripped [E3: "banana data banana " -> "banana data banana"]
    # Leading space is stripped [E1: " Zebralower" -> "Zebralower"]
    # "Hello" prefix: first char dropped -> "ello" [E1, E2]
    # Other uppercase starts unchanged [E2]
    out = []
    for s in probe["inputs"]:
        if s.startswith("Hello"):
            s = s[1:]
        s = s.strip()
        out.append(s)
    return {"outputs": out}

def predict(probe):
    # Capitalize first letter of each word, lowercase the rest [E1,E2,E3]
    # Words split on spaces; multiple spaces preserved [E2,E3]
    # Words starting with non-letter left unchanged [E2]
    # Leading space: first token empty, not capitalized [E2]
    # Punctuation within word doesn't split [E2]
    out = []
    for s in probe.get("inputs", []):
        try:
            res = []
            for t in s.split(" "):
                if t and t[0].isalpha():
                    res.append(t[0].upper() + t[1:].lower())
                else:
                    res.append(t)
            out.append(" ".join(res))
        except Exception:
            out.append(s)
    return {"outputs": out}

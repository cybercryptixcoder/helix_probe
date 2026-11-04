def predict(probe):
    # Split on any whitespace, collapse runs to single spaces [E2,E3]
    # Every token -> plain reverse w[::-1] [E1,E2,E3,E4,E5,E6]
    # EXCEPT the token that ends exactly at end-of-string (i.e. no trailing
    #   whitespace) -> w[-1] + w[::-1]  [E1,E2,E3,E4,E5,E6]
    # If the string ends with whitespace, NO token gets the special rule
    #   (so "a b " -> "a b", " x " -> "x") [E2,E3]
    # Empty / all-whitespace input -> "" [E3]
    out = []
    for s in probe.get("inputs", []):
        try:
            toks = s.split()
            if not toks:
                out.append("")
                continue
            ends_clean = not s[-1].isspace()
            res = []
            for i, w in enumerate(toks):
                if ends_clean and i == len(toks) - 1:
                    res.append(w[-1] + w[::-1])
                else:
                    res.append(w[::-1])
            out.append(" ".join(res))
        except Exception:
            out.append(s)
    return {"outputs": out}

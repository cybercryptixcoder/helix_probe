def predict(probe):
    # f(x) = x + "ny" for all inputs [E1, E2]
    # EXCEPT: a single space " " returns "ny" (space is stripped/ignored) [E2]
    # Hypothesis: trailing/leading whitespace is stripped before appending "ny" [E2]
    #   "test case " -> "test case ny" shows trailing space KEPT though... [E1]
    # So only the all-space case collapses. Best guess: strip only if result is empty.
    out = []
    for x in probe["inputs"]:
        if x.strip() == "":
            out.append("ny")
        else:
            out.append(x + "ny")
    return {"outputs": out}

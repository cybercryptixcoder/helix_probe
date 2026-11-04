def predict(probe):
    # Only one observation so far [E1]: f(x)=3 at x=2.9, and ~0 elsewhere.
    # Hypothesis (?): f(x) = round(x) when x is near an integer? No — 2.9 -> 3.0
    #   suggests rounding to nearest integer, but other inputs (88.2, 66.0, -20.3,
    #   -61.7, -24.3, 72.7, -50.4, -6.0, 21.3) all gave 0.0, not their rounded values.
    # So rounding alone is wrong.
    # Alternative (?): f(x) = 3 only in a small interval around 2.9, else 0.
    #   Without more data, guess a narrow bump near x=3.
    # Best current guess: f(x) = 3 if 2 < x < 4 else 0.0  (very uncertain)
    out = []
    for x in probe["x"]:
        try:
            if 2.0 < x < 4.0:
                out.append(3.0)
            else:
                out.append(0.0)
        except Exception:
            out.append(None)
    return {"y": out}

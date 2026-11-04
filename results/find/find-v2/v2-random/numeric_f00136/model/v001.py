def predict(probe):
    # Only one experiment so far [E1]. Outputs are small (~0.02-0.05), roughly
    # positive except near x=0 and x=2.9 (negative). Looks like a smooth MLP
    # approximation of some small-amplitude function. No clear structure yet.
    # Best guess: a gentle function, near zero, slightly negative near origin.
    # I'll model as a small-amplitude smooth function with a dip near x~0.
    # Without more data, predict a constant small positive value as baseline,
    # with a mild negative dip near x=0.
    # ?: amplitude and dip location are guesses.
    import math
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            # baseline small positive, dip near 0
            v = 0.02 - 0.05 * math.exp(-(x * x) / 50.0)
            out.append(round(v, 4))
        except Exception:
            out.append(None)
    return {"y": out}

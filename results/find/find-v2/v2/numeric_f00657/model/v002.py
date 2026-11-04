def predict(probe):
    # Output is always ±18 [E1, E2]
    # Sign rule: x < 0 -> +18, x >= 0 -> -18 [E1, E2]
    #   E2 shows x=0.0 -> 18 and x=-0.0 -> 18, so zero maps to +18 (i.e. rule is x <= 0 -> +18)
    #   Wait: E2 x=0.0 -> 18, x=-0.0 -> 18. Both zeros give +18.
    #   So: x <= 0 -> +18, x > 0 -> -18
    # No magnitude dependence, no special interval [E2]
    out = []
    for x in probe.get("x", []):
        if x is None:
            out.append(None)
        elif x <= 0:
            out.append(18.0)
        else:
            out.append(-18.0)
    return {"y": out}

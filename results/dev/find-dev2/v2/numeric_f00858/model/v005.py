def predict(probe):
    # f(x) = 1 on a plateau around 0, else 0 [E1, E2]
    # Plateau edges are between 1.85 (f=1) and 1.851 (f=0) [E5]
    # Symmetric about 0 [E1, E2, E3, E4, E5]
    # Sharp transition [E2, E3, E4, E5]
    # Edge threshold ~1.8505 (midpoint of 1.85 and 1.851) [?]
    out = []
    for x in probe.get("x", []):
        try:
            out.append(1.0 if -1.8505 < x < 1.8505 else 0.0)
        except Exception:
            out.append(None)
    return {"y": out}

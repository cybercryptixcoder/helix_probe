def predict(probe):
    # f(x) = 1 on a plateau around 0, else 0 [E1, E2]
    # Plateau edge is between 1.85 (f=1) and 1.855 (f=0) [E3, E4]
    # Symmetric about 0 [E1, E2, E3, E4]
    # Sharp transition [E2, E3, E4]
    # Edge threshold ~1.8525 (midpoint of 1.85 and 1.855) [?]
    out = []
    for x in probe.get("x", []):
        try:
            out.append(1.0 if -1.8525 < x < 1.8525 else 0.0)
        except Exception:
            out.append(None)
    return {"y": out}

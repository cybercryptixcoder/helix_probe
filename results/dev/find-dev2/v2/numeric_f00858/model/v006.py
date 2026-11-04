def predict(probe):
    # f(x) = 1 on a plateau around 0, else 0 [E1, E2]
    # Plateau edges: f(1.85)=1 and f(1.8501)=0 [E5, E6]
    # So right edge is in (1.85, 1.8501]; left edge symmetric [E5, E6]
    # Symmetric about 0 [E1-E6]
    # Sharp transition [E2-E6]
    # Edge threshold ~1.85005 (midpoint of 1.85 and 1.8501) [?]
    out = []
    for x in probe.get("x", []):
        try:
            out.append(1.0 if -1.85005 < x < 1.85005 else 0.0)
        except Exception:
            out.append(None)
    return {"y": out}

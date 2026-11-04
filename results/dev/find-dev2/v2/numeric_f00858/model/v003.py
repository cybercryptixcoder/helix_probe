def predict(probe):
    # f(x) = 1 on a plateau around 0, else 0 [E1, E2]
    # Plateau edges: f=0 at |x|=1.9, f=1 at |x|=1.85 [E3]
    # So edges lie between 1.85 and 1.9; symmetric about 0 [E1, E2, E3]
    # Sharp transition (no gradual ramp observed) [E2, E3]
    # Edge threshold ~1.875 (midpoint of 1.85 and 1.9) [?]
    out = []
    for x in probe.get("x", []):
        try:
            out.append(1.0 if -1.875 < x < 1.875 else 0.0)
        except Exception:
            out.append(None)
    return {"y": out}

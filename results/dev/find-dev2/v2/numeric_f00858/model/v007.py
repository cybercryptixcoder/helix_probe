def predict(probe):
    # f(x) = 1 on a plateau around 0, else 0 [E1, E2]
    # Plateau is symmetric about 0 [E1-E7]
    # Right edge: f(1.85)=1, f(1.85001)=0 [E6, E7]
    # Left edge: f(-1.85)=1, f(-1.85001)=0 [E7]
    # So edge is at |x| = 1.85 (inclusive), sharp transition [E5, E6, E7]
    out = []
    for x in probe.get("x", []):
        try:
            out.append(1.0 if -1.85 <= x <= 1.85 else 0.0)
        except Exception:
            out.append(None)
    return {"y": out}

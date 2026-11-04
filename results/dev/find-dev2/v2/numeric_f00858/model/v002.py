def predict(probe):
    # f(x) = 1 for -2 < x < 2, else 0 [E1, E2]
    # Boundary: f(-2)=0, f(-1.75)=1, f(1.75)=1, f(2)=0 [E2]
    # Plateau is wider than [-1,1]; edges lie between 1.75 and 2 [E2]
    # Symmetric about 0 [E1, E2]
    out = []
    for x in probe.get("x", []):
        try:
            out.append(1.0 if -2.0 < x < 2.0 else 0.0)
        except Exception:
            out.append(None)
    return {"y": out}

def predict(probe):
    # f(x) = 1 for -1 <= x <= 1, else 0 [E1]
    # Boundaries: f(-2)=0, f(-1)=1, f(1)=1, f(2)=0 [E1]
    # Symmetric about 0; flat plateau on [-1,1] [E1]
    out = []
    for x in probe.get("x", []):
        try:
            out.append(1.0 if -1.0 <= x <= 1.0 else 0.0)
        except Exception:
            out.append(None)
    return {"y": out}

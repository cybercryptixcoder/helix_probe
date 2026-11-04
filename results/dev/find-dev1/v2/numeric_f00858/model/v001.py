def predict(probe):
    # f(x) = 1 when |x| is in [0.5, 1]; else 0 [E1]
    # Boundaries: |x| in [0.5,1] inclusive (0.5 and 1 give 1; 2 and 0.25? untested near edges) [E1]
    # Outside that band (including 0, and |x|>=2) returns 0 [E1]
    # Symmetric in x (both -1 and 1 give 1) [E1]
    out = []
    for x in probe.get("x", []):
        try:
            ax = abs(x)
            out.append(1.0 if 0.5 <= ax <= 1.0 else 0.0)
        except Exception:
            out.append(None)
    return {"y": out}

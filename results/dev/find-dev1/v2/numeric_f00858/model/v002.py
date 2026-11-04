def predict(probe):
    # f(x) = 1 for all x with |x| <= 1.5 (at least); 0 for |x| >= 2 [E1, E2]
    # E2 shows 1 at |x| up to 1.5; E1 shows 0 at |x| = 2 and beyond
    # Boundary between 1.5 and 2 is untested — guess it's a smooth-ish cutoff [E1, E2, ?]
    # Symmetric in x [E1, E2]
    out = []
    for x in probe.get("x", []):
        try:
            ax = abs(x)
            out.append(1.0 if ax <= 1.75 else 0.0)
        except Exception:
            out.append(None)
    return {"y": out}

def predict(probe):
    # Output is either +18 or -18 (two-valued) [E1]
    # Sign appears to depend on x: negative x -> +18, positive x -> -18 [E1]
    # Zero/unknown boundary: assume sign flips at x=0 [E1, ?]
    # Exact rule uncertain; using sign of x as best guess [?]
    out = []
    for x in probe.get("x", []):
        try:
            out.append(18.0 if x < 0 else -18.0)
        except Exception:
            out.append(None)
    return {"y": out}

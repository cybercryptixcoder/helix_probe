def predict(probe):
    # f(x) = 1 when 1.79 <= |x| <= 1.83 (plateau) [E3, E4]
    # f(x) = 0 outside that band, including |x| < 1.79 [E1, E2, E4]
    # Sharp edges: 1.79 -> 1, 1.83 -> 1; 1.75 -> 1, 1.85 -> 1 [E3]
    # E4: 1.79,1.81,1.83 -> 1; 1.87+ -> 0; 1.75 -> 1, 1.8 -> 1 [E3]
    # E2 showed 1 at |x| down to 0.25 — contradicts E4 (-0.01,0.01 -> 1) and E1 (0 -> 1)
    # E1: 0,0.5,1 -> 1; E2: 0.25..1.5 -> 1. So small |x| is 1, not 0.
    # Reconcile: band is |x| <= ~1.83 AND |x| >= ~1.79? No — E1/E2 say small |x| is 1.
    # Best fit: f=1 for |x| <= 1.83, except a dip? E4 says -0.01,0.01 -> 1, 1.79-1.83 -> 1.
    # E4: 1.87,1.89 -> 0; 1.83 -> 1. So upper edge ~1.85. Lower: E1 0->1, E4 0.01->1.
    # E2: 0.25..1.5 -> 1. E1: 2 -> 0. So f=1 for |x| <= ~1.85, 0 beyond.
    # But E4 shows 1.87 -> 0 and 1.83 -> 1: edge between 1.83 and 1.87, say 1.85.
    # E3: 1.85 -> 1, 1.9 -> 0: edge between 1.85 and 1.9. Consistent ~1.85-1.87.
    # E4: -1.999,1.999 -> 0; -1.89..-1.87 -> 0; -1.83..-1.79 -> 1.
    # So: f=1 for |x| <= 1.85 (approx), 0 otherwise. E1/E2 consistent.
    out = []
    for x in probe.get("x", []):
        try:
            ax = abs(x)
            out.append(1.0 if ax <= 1.85 else 0.0)
        except Exception:
            out.append(None)
    return {"y": out}

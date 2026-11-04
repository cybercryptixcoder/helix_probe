def predict(probe):
    # f(x) is roughly constant near -1.6, with small wiggles [E1]
    # Values range -1.566 to -1.689 across x in [-62, 88] [E1]
    # No clear trend with x; looks like a shallow oscillating/MLP surface [E1]
    # Best guess: near-constant baseline with mild x-dependence; use a smooth fit [E1, ?]
    import math
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        # baseline plus small sinusoidal wiggle to mimic MLP wiggles
        y = -1.62 + 0.03 * math.sin(x * 0.11) + 0.02 * math.cos(x * 0.037)
        ys.append(y)
    return {"y": ys}

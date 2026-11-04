import math

def predict(probe):
    # Observations / beliefs:
    # - Outputs are small, bounded roughly to [-0.25, 0.25] [all E]
    # - No obvious smooth dependence on x; values look pseudo-random / hash-like [E1-E8]
    # - Repeated or nearby x do not give similar y (e.g. E4 -8 -> -0.0019 vs E2 -8 -> 0.0887)
    #   => not a deterministic function of x alone; likely noisy or chaotic/hash-based [?]
    # - Range of |y| shrinks for large |x|? E2 shows small values at x=-128..-80, but
    #   E6 has -0.22 at 110.5 and E5 -0.1903 at 28.4, so no clean decay [E2,E5,E6]
    # - No region with distinctly different behavior found; values look like
    #   a bounded pseudo-random function of x [E1-E8]
    #
    # Best model: a deterministic hash of x producing a value in ~[-0.25, 0.25].
    # Since the true mechanism is unknown and outputs appear random, we use a
    # stable hash of the numeric input to produce a bounded output.
    # This will not match exact values but captures the observed statistics.

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            # stable hash-like mixing of the float bits
            v = float(x)
            # handle non-finite
            if not math.isfinite(v):
                ys.append(None)
                continue
            # mix bits
            import struct
            b = struct.pack('<d', v)
            h = 2166136261
            for byte in b:
                h ^= byte
                h = (h * 16777619) & 0xFFFFFFFF
            # map to [-0.25, 0.25]
            frac = (h & 0xFFFFFF) / float(0xFFFFFF)
            y = (frac - 0.5) * 0.5
            ys.append(round(y, 4))
        except Exception:
            ys.append(None)
    return {"y": ys}

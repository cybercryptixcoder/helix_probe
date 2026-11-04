import math

def predict(probe):
    # Beliefs:
    # - f is NOT deterministic in x: repeated identical x give different y [E10].
    #   e.g. x=0 -> -0.0137 and 0.2402; x=10 -> -0.0482 and -0.043; x=-20 -> -0.0327 and 0.1585.
    #   So there is noise/state; exact prediction is impossible. Best we can do is match the
    #   distribution: mean ~0, spread ~0.1-0.15, bounded roughly [-0.3, 0.3] [E1-E10].
    # - No periodicity detected: x and x+10 (E6) not equal; x mod small periods not equal (E8) [E6, E8].
    # - No simple sinusoid fits [E2, E4].
    # - Near-duplicates (12 vs 12.0001, -33 vs -33.0001) also differ -> no local smoothness [E10].
    # - Outputs appear essentially like bounded noise with mean ~0 and std ~0.11.
    #   Observed range across all experiments: about [-0.29, 0.29].
    #
    # Model: deterministic pseudo-random value per x in [-0.29, 0.29], mean 0.
    # This is the best guess given the evidence that f is effectively unpredictable noise.

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
            # deterministic hash-like pseudo-random in [-1,1]
            h = math.sin(x * 12.9898 + 78.233) * 43758.5453
            r = h - math.floor(h)          # in [0,1)
            r = 2.0 * r - 1.0              # in [-1,1)
            y = 0.15 * r                   # scale to ~[-0.15,0.15]; std ~0.087
            ys.append(round(y, 4))
        except Exception:
            ys.append(None)
    return {"y": ys}

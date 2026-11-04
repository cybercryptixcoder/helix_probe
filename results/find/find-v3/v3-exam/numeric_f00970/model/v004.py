import math

def predict(probe):
    # A. For |x| < ~3, output is a large value ~12 with noise [E2,E4,E6].
    # B. For |x| >= ~3, output is small and oscillatory [E1,E2,E3,E4,E5,E6,E7,E8].
    # C. Boundary between 3.0 and 3.1: x=3.0 large (13.78), x=3.1 small [E6].
    # D. Regime depends on |x|, not sign [E2,E4,E6].
    # E. Outside regime, output is NOT sin(x): E8 dense run shows no match to sin(x)
    #    at all (match 0.00). Magnitudes ~0.5-2, irregular. Looks like noise/random
    #    oscillation with no simple closed form [E1,E3,E5,E7,E8].
    # F. Inside plateau value ~12 with noise; use 12.0 [E2,E4,E6].
    # G. Output is noisy everywhere; approximate.

    def f(x):
        ax = abs(x)
        if ax < 3.05:
            return 12.0
        # Outside: best guess is a bounded pseudo-random oscillation.
        # Use a deterministic hash-like oscillation with amplitude ~1.
        return math.sin(x * 12.9898) * 1.0

    return {"y": [f(x) for x in probe["x"]]}

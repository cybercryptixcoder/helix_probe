import math

def predict(probe):
    # A. For |x| < ~3, output is a large value ~12 with substantial noise [E2,E4,E6].
    # B. For |x| >= ~3, output is small and oscillatory [E1,E2,E3,E4,E5,E6].
    # C. Boundary is between 3.0 and 3.1: at x=3.0 still large (13.78), at 3.1 small [E6].
    # D. Regime depends on |x|, not sign [E2,E4,E6].
    # E. Outside regime, output is NOT sinc (sin/x) — magnitudes ~0.5-2 at large x,
    #    not ~0.01. Looks like a bounded oscillation, e.g. sin(x) or similar [E1,E2,E3,E5].
    # F. Inside plateau value ~12 with noise; use 12.0 [E2,E4,E6].
    # G. Output noisy; approximate.

    def f(x):
        ax = abs(x)
        if ax < 3.05:
            return 12.0
        return math.sin(x)

    return {"y": [f(x) for x in probe["x"]]}

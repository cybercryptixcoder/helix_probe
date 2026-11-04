import math

def predict(probe):
    # A. For |x| < 3, output is a large value ~12 with noise [E2,E4,E6].
    # B. For |x| >= 3, output is small, bounded (~|y|<2.3), irregular [E1,E3,E5,E7-E11].
    # C. Boundary between 3.0 and 3.1: x=3.0 large (13.78), x=3.1 small [E6].
    # D. Regime depends on |x|, not sign [E2,E4,E6].
    # E. Outside regime, output is NOT sin(x) and NOT smooth in x:
    #    E10 shows nearby x (3.2..7.0 step 0.2) give uncorrelated y -> essentially noise.
    #    E8 dense run also uncorrelated with sin(x). So model as bounded pseudo-random.
    # F. Inside plateau value ~12 with noise; use 12.0 [E2,E4,E6].
    # G. Output is noisy everywhere; approximate.

    def f(x):
        ax = abs(x)
        if ax < 3.05:
            return 12.0
        # Outside: bounded pseudo-random oscillation, uncorrelated between nearby x.
        # Use a high-frequency hash-like function of x.
        h = math.sin(x * 12.9898 + 78.233) * 43758.5453
        frac = h - math.floor(h)
        return (frac * 2.0 - 1.0) * 2.0

    return {"y": [f(x) for x in probe["x"]]}

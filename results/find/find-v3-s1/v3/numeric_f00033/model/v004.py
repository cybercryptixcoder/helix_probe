import math

def predict(probe):
    # Beliefs:
    # - f is a smooth bump centered near x=0, peaking around x=0 with value ~0.39 [E2]
    # - Outside roughly |x| < 8, f decays to near zero (~ -0.003 baseline) [E1, E2, E3]
    # - The bump is asymmetric: rises to peak at 0, then falls; slightly negative tails [E2]
    # - Far-field values are tiny negative noise-like constant ~ -0.003 [E1,E3]
    # - Model as Gaussian-like bump plus small negative baseline offset.
    #   Peak ~0.39 at x=0, width sigma ~2.5 (from values: at x=1 ->0.255, x=2 ->0.12)
    # - The MLP approximation makes it smooth; use Gaussian bump.

    xs = probe["x"]
    ys = []
    for x in xs:
        try:
            # Gaussian bump
            sigma = 2.6
            peak = 0.39
            bump = peak * math.exp(-(x * x) / (2 * sigma * sigma))
            # small negative baseline far away
            baseline = -0.003
            # taper baseline near center so bump dominates
            taper = math.exp(-(x * x) / (2 * 6.0 * 6.0))
            val = bump + baseline * (1.0 - taper)
            # slight asymmetry: negative side slightly higher near -1.2 (0.1552 at -1.2 vs 0.255 at 1)
            # Actually 0.1552 at -1.2 vs 0.255 at 1 -> left side lower. Add mild asymmetry.
            if x < 0:
                val *= (1.0 - 0.05 * math.exp(-(x*x)/(2*2.0*2.0)))
            ys.append(val)
        except Exception:
            ys.append(None)
    return {"y": ys}

import math

def predict(probe):
    # Model of the black box f(x).
    #
    # Observations:
    # - Outputs are always negative, roughly between -1.81 and -1.47.
    # - For |x| large (|x| > ~10), the output increases (becomes less negative)
    #   roughly linearly with |x|, symmetric in x: f(-x) ~ f(x) [E6, E2].
    #   E6: f(-128)=-1.4667, f(128)=-1.5099; f(-110)=-1.4963, f(110)=-1.5348.
    #   Slight asymmetry: negative side a bit higher than positive side.
    # - Near x=0 there is a dip (more negative) with a bump/wiggle:
    #   f(0) ~ -1.756, f(-1) ~ -1.789, f(1) ~ -1.789, f(-0.8) ~ -1.813,
    #   f(0.8) ~ -1.815, f(-2.5) ~ -1.707, f(2.5) ~ -1.690 [E2, E4].
    #   So there's a local minimum around |x| ~ 0.8-1, and a local max near 0.
    # - The behavior is essentially a smooth function; the MLP approximates
    #   something like:  base - A*exp(-x^2/s) + B*|x| + small odd term.
    #
    # We fit a smooth parametric form capturing:
    #   * linear growth with |x| (saturating slightly at large |x|)
    #   * central dip around |x|~1
    #   * small bump at 0
    #   * slight left/right asymmetry.
    #
    # Fit by hand from the evidence points.

    x = float(probe["x"][0]) if isinstance(probe["x"], list) else float(probe["x"])
    # (handle list input robustly)
    if isinstance(probe["x"], list):
        return {"y": [predict({"x": v})["y"] for v in probe["x"]]}

    ax = abs(x)

    # Baseline: large-|x| linear trend.
    # From E6: at |x|=128 ~ -1.49 avg, at |x|=15 ~ -1.663 avg.
    # slope ~ (1.663-1.49)/(128-15) = 0.173/113 ~ 0.00153 per unit.
    # Intercept at 0 extrapolated: -1.663 - 0.00153*15 ~ -1.686.
    # But near 0 there's a dip to ~-1.79.
    base = -1.686 + 0.00153 * ax

    # Slight saturation at large |x|: the linear trend flattens a bit.
    # E6: 75->-1.585, 90->-1.563, 110->-1.535, 128->-1.51
    # diffs: 15->0.022, 20->0.028, 18->0.025 -> roughly linear, ok.

    # Central dip: gaussian-like negative contribution centered near |x|~1.
    dip = -0.105 * math.exp(-((ax - 1.0) ** 2) / (2 * 1.2 ** 2))

    # Bump at zero: f(0) is higher than the dip trend.
    bump = 0.035 * math.exp(-(x ** 2) / (2 * 0.45 ** 2))

    # Asymmetry: negative x slightly higher (~0.01-0.02) at large |x|,
    # and near 0 too (f(-1)=-1.789, f(1)=-1.789 similar; f(-0.8)=-1.813 vs f(0.8)=-1.815).
    # Small: negative side ~ +0.008.
    asym = 0.008 * math.tanh(-x / 20.0)

    y = base + dip + bump + asym

    # Clamp to observed range
    y = max(-1.85, min(-1.45, y))
    return {"y": y}

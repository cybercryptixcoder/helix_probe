import math

def predict(probe):
    # Mechanism: f(x) = 16.81*|x| - 0.5, with noise that is large near x=0
    #   and negligible for |x| > ~0.6. We predict the mean (noise-free) value.
    # - Slope ~16.8 from large-|x| points [E1, E2]: 2152/128, 1075/64, 269/16, 135/8
    # - Small additive offset ~-0.5 from small-|x| points [E1]: 16.3 at x=1, 32.6 at x=2
    # - Inner region |x| < ~0.6 is same mean but noisy [E3-E9]; we return the mean.
    # - Symmetric in x (|x|) [E1, E2]: f(-x) ~ f(x)
    out = []
    for x in probe.get("x", []):
        try:
            xf = float(x)
            y = 16.81 * abs(xf) - 0.5
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}

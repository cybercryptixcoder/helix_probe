import math

def predict(probe):
    # Central structure: positive peak ~0.078 near x=-2..-1, zero near x=-0.4,
    #   deep trough ~-0.095 near x=1, rising back toward 0 by x~3 [E2,E4,E6].
    # Outside |x|>~4: smooth, slowly-varying, small positive values that grow
    #   with |x|: ~0.0089 at 40, ~0.022 at 64, ~0.028 at -64, ~0.035 at 88,
    #   ~0.043 at 103, ~0.054 at 124 [E1,E2,E3,E5].
    # Tail is roughly monotone increasing in |x| (no oscillation) [E1,E3,E5].
    # Near x~20-24 there is a slight dip to ~0 [E4,E6].
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
            ax = abs(x)
            # slow baseline: grows with |x|, small dip near |x|~20
            base = 0.0004 * ax - 0.006 * math.exp(-((ax - 20.0) ** 2) / 50.0)
            # central bump/trough structure (localized, |x| < ~4)
            # positive bump centered ~-1.6, negative trough centered ~1.0
            bump = 0.078 * math.exp(-((x + 1.6) ** 2) / 3.0)
            trough = -0.095 * math.exp(-((x - 1.0) ** 2) / 2.0)
            central = bump + trough
            # blend: central dominates near 0, base dominates far away
            w = math.exp(-(x * x) / 30.0)
            y = w * central + (1 - w) * base + w * 0.0
        except Exception:
            y = None
        ys.append(y)
    return {"y": ys}

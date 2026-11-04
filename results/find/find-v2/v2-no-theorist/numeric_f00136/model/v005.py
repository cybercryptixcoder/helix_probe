import math

def predict(probe):
    # Structure of f, from the evidence:
    # Central region |x| < ~4.5: a positive bump peaking ~0.078 near x=-1.5,
    #   crossing zero near x=-0.35, then a deep trough ~-0.095 near x=1,
    #   rising back up through ~-0.044 at x=4.5 [E2,E4,E6,E12].
    # Mid-range negative lobe: from x~4.5 to ~21, y is negative and rises
    #   smoothly and almost linearly toward 0, crossing zero near x~21.5,
    #   reaching ~0.0003 at x=24 [E6,E8,E12].
    # Far tail |x|>~25: smooth, slowly increasing with |x|, roughly linear
    #   with slope ~0.0003, passing ~0.0177 at |x|=25, ~0.0248 at 50,
    #   ~0.0394 at 100, ~0.0455 at 120 [E10,E8].
    # Negative side mirrors positive side in the tail (symmetric) [E8,E10].
    # No oscillation in tail; monotone in |x| [E8,E10].
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
            ax = abs(x)
            if ax <= 4.5:
                # central bump + trough
                bump = 0.078 * math.exp(-((x + 1.5) ** 2) / 2.5)
                trough = -0.095 * math.exp(-((x - 1.0) ** 2) / 3.0)
                y = bump + trough
            elif ax <= 25.0:
                # mid-range: negative lobe rising toward 0, crossing ~21.5
                # linear-ish: y ~ -0.044 at 4.5, ~0 at 21.5
                y = -0.044 + (ax - 4.5) * (0.044 / 17.0)
            else:
                # far tail: slow linear growth with |x|
                y = 0.0177 + (ax - 25.0) * (0.0003)
        except Exception:
            y = None
        ys.append(y)
    return {"y": ys}

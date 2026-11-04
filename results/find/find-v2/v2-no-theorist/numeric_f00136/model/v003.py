import math

def predict(probe):
    # f is smooth, bounded, roughly in [-0.1, 0.1] [E1-E4].
    # Central structure: positive bump peaking ~0.078 near x=-2..-1 [E2,E4],
    #   crossing zero near x=-0.5, deep trough ~-0.095 near x=1 [E2,E4].
    # Outside |x|>~3 the oscillation is gone; a slow positive tail remains:
    #   ~0.028 at -64, ~0.022 at 64, ~0.009 at 40, ~-0.004 at 20 [E2,E4].
    # Tail is not monotone: dips slightly negative around x~20 then rises [E4].
    # Model: localized damped oscillation near 0 + slow positive baseline.
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
            # slow baseline: rises toward large |x|, small dip near x~20
            base = 0.006 + 0.00022 * abs(x)
            # localized damped oscillation, period ~6, centered near x=0
            w = 2.0 * math.pi / 6.0
            phi = math.pi / 2 + w * 1.5   # peak near x=-1.5
            amp = 0.085 * math.exp(-(x * x) / 18.0)
            y = base + amp * math.sin(w * x + phi)
        except Exception:
            y = None
        ys.append(y)
    return {"y": ys}

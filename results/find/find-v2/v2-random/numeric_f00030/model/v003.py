def predict(probe):
    # y is a smooth even-ish function of x, roughly -1.75 at x=0 rising toward ~-1.5 at |x|~120 [E1,E2,E3,E4]
    # There is substantial high-frequency noise (~±0.03) on top of the smooth trend [E1,E2,E3,E4]
    # The smooth trend: minimum near x=0, monotone rising with |x|, saturating at large |x| [E2,E3,E4]
    # Fit a simple form: y = base + amp*(1 - exp(-(x/s)^2))  -- rises from base at 0 to base+amp at large |x|
    # From data: x=0 -> ~-1.76; |x|=120 -> ~-1.50; |x|=60 -> ~-1.59; |x|=30 -> ~-1.65
    # Try base=-1.76, amp=0.26, s=55
    import math
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            u = (x / 55.0) ** 2
            y = -1.76 + 0.26 * (1.0 - math.exp(-u))
        except Exception:
            y = None
        ys.append(y)
    return {"y": ys}

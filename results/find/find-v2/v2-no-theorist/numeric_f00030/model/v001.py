def predict(probe):
    # All observed y lie in a narrow band around -1.6, varying smoothly with x.
    # E1: y ranges -1.566 (x=88.2) to -1.689 (x=2.9). Looks like a smooth
    # function of x, roughly decreasing then... hard to tell from one probe.
    # Best guess: y ≈ -1.6 + small smooth wiggle in x. Use a gentle sinusoid
    # in x with small amplitude, since outputs cluster tightly.
    # ? amplitude and period unknown; pick something mild.
    import math
    xs = probe.get("x", [])
    out = []
    for x in xs:
        try:
            y = -1.6 + 0.05 * math.sin(x / 20.0)
        except Exception:
            y = None
        out.append(y)
    return {"y": out}

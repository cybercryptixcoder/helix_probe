def predict(probe):
    # All outputs are near -1.6, varying smoothly with x [E1].
    # Looks like a smooth function of x with small variation; approximate
    # as a shallow MLP-like curve. Best guess: roughly constant ~-1.62
    # with slight structure. Use a smooth function fit to E1 points.
    # ? Uncertain about exact shape; use a gentle quadratic-ish fit.
    import math
    xs = probe["x"]
    ys = []
    for x in xs:
        # Fit from E1: values range -1.566 to -1.689, roughly
        # higher |x| -> closer to -1.58, near 0 -> lower (-1.67 to -1.69)
        # Model: y = -1.62 - 0.06*exp(-(x/40)^2) + small linear tilt
        y = -1.62 - 0.06 * math.exp(-(x / 40.0) ** 2)
        ys.append(y)
    return {"y": ys}

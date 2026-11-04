import math

def predict(probe):
    # Beliefs:
    # - f is a smooth MLP curve, not periodic; a broad bump near x~-2 and a
    #   trough near x~1, then a slowly rising tail [E1,E2,E3].
    # - Left tail x<=-16: nearly linear, slope ~ -0.00029/unit [E1].
    # - Bump region: rises from x=-16 to a flat-ish peak near x=-2..-1.5
    #   (~0.078), stays nearly flat through x=-1, then drops steeply [E1,E2,E3].
    # - Trough near x=1 (~-0.095), recovering to ~-0.044 by x=4 [E1,E2,E3].
    # - Right tail x>=4: slowly rising, roughly linear, zero near x~23 [E1,E2].
    # - Use piecewise-linear interpolation through knots; add E3 knots to
    #   sharpen the central region [E3].

    knots = [
        (-128, 0.0479), (-112, 0.043), (-96, 0.0382), (-80, 0.0335),
        (-64, 0.0288), (-48, 0.0242), (-32, 0.0197), (-16, 0.0149),
        (-10, 0.0249), (-8, 0.031), (-6, 0.0471), (-4, 0.0628),
        (-3.5, 0.0667), (-3, 0.0706), (-2.5, 0.0745), (-2, 0.0784),
        (-1.75, 0.0783), (-1.5, 0.078), (-1.25, 0.0778), (-1, 0.0776),
        (-0.75, 0.0728), (-0.5, 0.049), (-0.25, 0.0229), (0, -0.0008),
        (0.25, -0.0246), (0.5, -0.0484), (0.75, -0.0819), (1, -0.0951),
        (1.5, -0.0782), (2, -0.0595), (2.5, -0.0507), (3, -0.0466),
        (3.5, -0.0452), (4, -0.0438), (6, -0.0371), (8, -0.03),
        (12, -0.0208), (16, -0.0126), (24, 0.0003), (32, 0.0046),
        (48, 0.0133), (64, 0.022), (96, 0.0394), (128, 0.0565),
    ]

    def interp(x):
        if x <= knots[0][0]:
            return knots[0][1]
        if x >= knots[-1][0]:
            return knots[-1][1]
        for i in range(len(knots) - 1):
            x0, y0 = knots[i]
            x1, y1 = knots[i + 1]
            if x0 <= x <= x1:
                t = (x - x0) / (x1 - x0)
                return y0 + t * (y1 - y0)
        return knots[-1][1]

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
            ys.append(round(interp(x), 4))
        except Exception:
            ys.append(None)
    return {"y": ys}

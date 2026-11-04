import math

def predict(probe):
    # Beliefs:
    # - f is smooth and roughly odd-symmetric-ish? No: check.
    # - For x <= -16: y decreases linearly-ish as x increases [E1]: 
    #   (-128,0.0479),(-112,0.043),(-96,0.0382),(-80,0.0335),(-64,0.0288),
    #   (-48,0.0242),(-32,0.0197),(-16,0.0149). Slope ~ -0.00029 per unit.
    # - For x in [-16,-1]: rises to a peak near -1.5 (~0.078) [E1,E2].
    #   (-16,0.0149),(-10,0.0249),(-8,0.031),(-6,0.0471),(-4,0.0628),
    #   (-2,0.0784),(-1.5,0.078),(-1,0.0776).
    # - For x in [-1,0]: drops steeply to ~0 at 0 [E1,E2]:
    #   (-1,0.0776),(-0.5,0.049),(-0.25,0.0229),(0,-0.0008).
    # - For x in [0,~3]: continues dropping to a negative trough near x~1-2:
    #   (0,-0.0008),(0.25,-0.0246),(0.5,-0.0484),(0.75,-0.0819),(1,-0.0951),
    #   (2,-0.0595),(3,-0.0466). Trough near x=1 (~-0.095).
    # - For x >= 3: rises back toward positive, roughly linear:
    #   (3,-0.0466),(4,-0.0438),(6,-0.0371),(8,-0.03),(12,-0.0208),(16,-0.0126),
    #   (24,0.0003),(32,0.0046),(48,0.0133),(64,0.022),(96,0.0394),(128,0.0565).
    #   Slope ~ 0.00044 per unit, zero crossing near x~23.
    # - Overall: a smooth oscillatory-looking curve, not periodic; a big bump
    #   near -1.5 and a trough near +1, then slowly rising tail.
    # - Hypothesis: f looks like a damped oscillation / combination of a bump
    #   and a slow ramp. Use piecewise linear interpolation through the
    #   observed knots, which captures the shape well.

    knots = [
        (-128, 0.0479), (-112, 0.043), (-96, 0.0382), (-80, 0.0335),
        (-64, 0.0288), (-48, 0.0242), (-32, 0.0197), (-16, 0.0149),
        (-10, 0.0249), (-8, 0.031), (-6, 0.0471), (-4, 0.0628),
        (-2, 0.0784), (-1.5, 0.078), (-1, 0.0776), (-0.5, 0.049),
        (-0.25, 0.0229), (0, -0.0008), (0.25, -0.0246), (0.5, -0.0484),
        (0.75, -0.0819), (1, -0.0951), (2, -0.0595), (3, -0.0466),
        (4, -0.0438), (6, -0.0371), (8, -0.03), (12, -0.0208),
        (16, -0.0126), (24, 0.0003), (32, 0.0046), (48, 0.0133),
        (64, 0.022), (96, 0.0394), (128, 0.0565),
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

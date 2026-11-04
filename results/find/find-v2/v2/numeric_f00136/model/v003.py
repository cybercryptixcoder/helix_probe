import math

def predict(probe):
    # Observations:
    # E2: outer region x<=-16: y decreases smoothly, nearly linear: 0.0479 at -128 to 0.0149 at -16.
    #     slope ~ -0.00029/unit. [E2]
    # E4: outer region x<=-14: continues linear: 0.0277 at -60 ... 0.0142 at -14. [E4]
    # E4: outer region x>=26: linear rising: 0.0014 at 26, 0.0035 at 30, 0.0068 at 36. [E4]
    #     slope ~ +0.00029/unit, offset ~ -0.0061.
    # E4: oscillation region roughly [-12, 24]: at -12 y=0.0187, -10 0.0249, -6 0.0471, -2 0.0784,
    #     2 -0.0595, 6 -0.0371, 10 -0.0249, 14 -0.0167, 18 -0.0084, 22 -0.0008. [E4]
    #     This is a smooth curve, not a fast sinusoid: rises to a peak near -2 then drops sharply.
    # E1: x=2.9 -> -0.0469, x=-6 -> 0.0471, x=21.3 -> -0.0017 consistent with this curve. [E1]
    # E3: x=1.2 -> -0.0895 (near the sharp drop), x=30.3 -> 0.0037 (outer). [E3]
    # Model: piecewise. Outer left linear, outer right linear, middle a smooth curve.
    # Middle curve: fit a low-order polynomial through E4 middle points.
    out = []
    for x in probe["x"]:
        try:
            if x <= -14.0:
                # linear left: through (-128,0.0479) and (-14,0.0142)
                y = 0.0142 + (x + 14.0) * (0.0479 - 0.0142) / (-128.0 + 14.0)
            elif x >= 26.0:
                # linear right: through (26,0.0014) and (36,0.0068)
                y = 0.0014 + (x - 26.0) * (0.0068 - 0.0014) / 10.0
            else:
                # middle: interpolate through E4 middle points via cubic-ish polynomial fit
                xs = [-12,-10,-6,-2,2,6,10,14,18,22]
                ys = [0.0187,0.0249,0.0471,0.0784,-0.0595,-0.0371,-0.0249,-0.0167,-0.0084,-0.0008]
                # Lagrange interpolation
                y = 0.0
                for i in range(len(xs)):
                    term = ys[i]
                    for j in range(len(xs)):
                        if i != j:
                            term *= (x - xs[j]) / (xs[i] - xs[j])
                    y += term
        except Exception:
            y = None
        out.append(y)
    return {"y": out}

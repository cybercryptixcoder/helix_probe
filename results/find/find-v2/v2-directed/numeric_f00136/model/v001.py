import math

def predict(probe):
    # Observations [E1]:
    # - For x <= -16: y decreases smoothly as x increases (from ~0.048 at -128 to ~0.015 at -16).
    # - Sharp peak near x = -2 (~0.078), then drops through 0 near x = 0.
    # - For x >= 0: y rises from ~0 at 0 to ~0.022 at 64, roughly linear/smooth.
    # - There is a special interval around [-8, 0] where behavior changes (peak then zero crossing).
    # Hypothesis: piecewise smooth function with a bump near x=-2 and a linear-ish tail.
    # This is a rough guess; the MLP likely approximates something like a Gaussian bump plus a ramp.
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
            if x <= -16:
                # linear decreasing from (-128, 0.0479) to (-16, 0.0149)
                y = 0.0149 + (x + 16) * (0.0479 - 0.0149) / (-128 + 16)
            elif x < -8:
                # transition: from 0.0149 at -16 to 0.031 at -8
                y = 0.0149 + (x + 16) * (0.031 - 0.0149) / 8.0
            elif x <= 0:
                # bump region: peak near -2 (0.0784), zero at 0 (-0.0008)
                # quadratic through (-8,0.031), (-2,0.0784), (0,-0.0008)
                # use Lagrange interpolation
                x0, y0 = -8, 0.031
                x1, y1 = -2, 0.0784
                x2, y2 = 0, -0.0008
                y = (y0 * (x - x1) * (x - x2) / ((x0 - x1) * (x0 - x2)) +
                     y1 * (x - x0) * (x - x2) / ((x1 - x0) * (x1 - x2)) +
                     y2 * (x - x0) * (x - x1) / ((x2 - x0) * (x2 - x1)))
            else:
                # x > 0: roughly linear from (0,-0.0008) to (64,0.022)
                y = -0.0008 + x * (0.022 + 0.0008) / 64.0
            ys.append(round(y, 4))
        except Exception:
            ys.append(None)
    return {"y": ys}

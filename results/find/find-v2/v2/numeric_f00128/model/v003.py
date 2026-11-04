import math

def predict(probe):
    # Model: f(x) is a smooth function (an MLP approximation), NOT piecewise-linear.
    # E4 shows a smooth transition near 0: f(0)=5.4186, not a jump.
    # For large |x|: f(x) ~ linear. Positive side slope ~ -16.9 [E1,E2,E3].
    # Negative side slope ~ -6.76 [E1,E2].
    # The function is smooth and monotone decreasing overall (roughly).
    # Small-x behavior: f(0)=5.4186, f(0.05)=5.2759, f(0.1)=5.1041, f(0.2)=4.6858,
    #   f(0.3)=4.0718, f(0.4)=3.2125, f(0.6)=0.8742, f(0.8)=-2.1698, f(1.5)=-13.7572.
    #   f(-0.05)=5.5613, f(-0.1)=5.704, f(-0.2)=5.9894, f(-0.4)=6.5602, f(-0.6)=7.1978,
    #   f(-0.8)=8.1725, f(-1.5)=12.5417.
    # So near 0 there's a smooth S-shaped (sigmoid-like) transition connecting
    #   the negative-side line (slope -6.76) to the positive-side line (slope -16.9).
    # f(0)=5.4186 is roughly the midpoint.
    # For |x|>=~1.5 the two linear asymptotes fit well [E1,E2,E3].
    # We model: f(x) = asymptote(x) + smooth correction near 0.
    # Asymptotes: for x>0: y = -16.9*x + 11.2 ; for x<0: y = -6.76*x + 2.4.
    # But at x=0 these give 11.2 and 2.4; observed 5.4186. So the transition
    #   blends between them smoothly. Use a sigmoid blend in a window around 0.
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
            # asymptote lines
            yp = -16.9*x + 11.2   # positive-side line
            yn = -6.76*x + 2.4    # negative-side line
            # blend weight w in [0,1]: w=1 for x large positive, 0 for x large negative
            # transition width ~ 1.0 (smooth S near 0)
            w = 1.0/(1.0 + math.exp(-x/0.35))
            y = w*yp + (1.0-w)*yn
            ys.append(y)
        except Exception:
            ys.append(None)
    return {"y": ys}

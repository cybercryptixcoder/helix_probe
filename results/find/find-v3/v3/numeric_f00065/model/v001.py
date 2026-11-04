import math

def predict(probe):
    # Model hypothesis: f(x) is approximately linear (odd, through origin).
    # Evidence E1: y/x ratios: -228.97/88.2=-2.596, -173.49/66=-2.629,
    #   26.97/-20.3=-1.329, 99.56/-61.7=-1.614, -15.84/2.9=-5.46,
    #   33.98/-24.3=-1.398, -190.23/72.7=-2.617, 79.75/-50.4=-1.582,
    #   1.91/-6=-0.318, -61.81/21.3=-2.902. Not constant -> not simple linear.
    # Ratios cluster near -2.6 for large |x| and are smaller for small |x|,
    # suggesting a saturating/curved odd function. Best guess: y ~ -2.6*x
    # with some nonlinearity. Use a smooth odd shape: y = a*x + b*x/(1+x^2/c).
    # Fit roughly: large |x| slope ~ -2.6, small |x| slope ~ -0.3..-1.6.
    # ? uncertain; using a simple odd cubic-ish approximation.
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        if x is None:
            ys.append(None)
            continue
        # odd function guess
        y = -2.6 * x + 2.3 * x / (1.0 + (x * x) / 400.0)
        ys.append(y)
    return {"y": ys}

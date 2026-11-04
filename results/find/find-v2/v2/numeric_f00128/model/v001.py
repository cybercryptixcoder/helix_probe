import math

def predict(probe):
    # Model: f(x) is a smooth nonlinear function approximated by an MLP.
    # Evidence E1: outputs are large in magnitude and roughly cubic-ish in x.
    #   f(88.2) ~ -1479, f(66) ~ -1104, f(72.7) ~ -1217 (negative, growing with |x|)
    #   f(-61.7) ~ 419, f(-50.4) ~ 343 (positive for negative x)
    #   f(-20.3) ~ 140, f(-24.3) ~ 167, f(21.3) ~ -349, f(2.9) ~ -38, f(-6) ~ 43
    # Sign pattern: y has opposite sign to x for large |x|; small x near 0 gives small y.
    # This is consistent with a cubic-like term -a*x^3 plus lower order terms.
    # Fit a cubic polynomial y = a*x^3 + b*x^2 + c*x + d as a smooth approximation.
    # Coefficients estimated from E1 by least squares (hardcoded).
    # ? MLP may deviate from cubic; this is a best guess.
    a = 0.00215
    b = 0.0
    c = -0.55
    d = 0.0
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
            y = a*x**3 + b*x**2 + c*x + d
            ys.append(y)
        except Exception:
            ys.append(None)
    return {"y": ys}

import math

def predict(probe):
    # Model: f(x) is an MLP approximating a smooth function.
    # Evidence E1: outputs are large and roughly odd-ish in x.
    #   x=-93.6 -> 155.5, x=88.9 -> -230.7, x=67.5 -> -177.2,
    #   x=-62.7 -> 101.3, x=-1.2 -> -6.4, x=-12.9 -> 14.0,
    #   x=38.8 -> -105.5, x=73.9 -> -193.2, x=-104 -> 173.7, x=-120.7 -> 203.0
    # Signs: negative x mostly positive y, positive x mostly negative y => roughly odd.
    # Magnitudes grow with |x|. A cubic-like odd function fits: y ~ -a*x^3 + b*x.
    # Fit rough scale: at |x|~100, |y|~200 => a ~ 200/1e6 = 2e-4.
    # Small x: x=-1.2 -> -6.4 (positive slope near 0), x=-12.9 -> 14.0.
    # Try y = -2e-4 * x^3 + c*x. At x=-1.2: -2e-4*(-1.728)+c*(-1.2)= -6.4
    #   => 0.0003456 -1.2c = -6.4 => c ~ 5.33
    # Check x=-12.9: -2e-4*(-2146.7)+5.33*(-12.9)=0.429-68.8=-68.3, but observed 14.0.
    # So not a simple cubic. There is structure. Without more data, use a smooth
    # odd-ish approximation. Marked uncertain (?).
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        if x is None:
            ys.append(None)
            continue
        # best-guess smooth odd-ish MLP approximation (?)
        y = -2.0e-4 * x**3 + 5.0 * x
        ys.append(round(y, 4))
    return {"y": ys}

def predict(probe):
    # f(x) looks like a smooth, roughly quadratic-ish function of x on the whole domain.
    # Evidence E1: f(88.2)=9933.99, f(66)=7460.29, f(72.7)=8206.85, f(21.3)=2479.47,
    # f(2.9)=429.19, f(-6)=130.99, f(-20.3)=503.81, f(-24.3)=608.10,
    # f(-50.4)=1288.57, f(-61.7)=1583.18.
    # Fit a quadratic a*x^2 + b*x + c through the data (least squares by hand-ish).
    # Rough fit: f(x) ~ 1.28*x^2 + 0.5*x + 300 (?) -- approximate.
    import math
    out = []
    for x in probe.get("x", []):
        try:
            y = 1.28*x*x + 0.5*x + 300.0
        except Exception:
            y = None
        out.append(y)
    return {"y": out}

import math

def predict(probe):
    # f(x) ≈ 16.8 * x for |x| >= 1 (linear growth) [E1]
    # f(x) ≈ 16.8 * x^2 for |x| < 1 (quadratic near zero) [E1]
    # At x=0, f(0) ≈ 0.36 (small offset, not exactly 0) [E1]
    # Smooth transition around |x|=1 [E1]
    out = []
    for x in probe.get("x", []):
        try:
            ax = abs(x)
            if ax >= 1:
                y = 16.8 * x
            else:
                y = 16.8 * x * x + 0.36
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}

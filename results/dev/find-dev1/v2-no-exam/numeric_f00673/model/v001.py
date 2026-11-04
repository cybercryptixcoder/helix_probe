import math

def predict(probe):
    # f(x) ≈ 16.8 * |x| + 0.0135, roughly linear in |x| with a small offset [E1]
    # Symmetric in x: f(-x) ≈ f(x) [E1]
    # Small positive offset near 0 (~0.0135 at x=0) [E1]
    # Slight asymmetry/noise: f(-128)=2151.12 vs f(128)=2150.15, f(-1)=16.60 vs f(1)=16.89 [E1]
    # Slope estimate: from x=64 (1074.34) and x=128 (2150.15): slope ≈ (2150.15-1074.34)/64 ≈ 16.81 [E1]
    # Intercept ≈ 0.0135 at x=0 [E1]
    out = []
    for x in probe.get("x", []):
        try:
            y = 16.81 * abs(x) + 0.0135
        except Exception:
            y = None
        out.append(y)
    return {"y": out}

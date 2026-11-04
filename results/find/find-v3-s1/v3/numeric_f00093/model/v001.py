import math

def predict(probe):
    # Model v1: first look at the data.
    # E1: f(x) appears roughly odd-ish? Let's check:
    #   x=-93.6 -> 57.8 ; x=88.9 -> -64.08 ; x=67.5 -> -60.23 ; x=-62.7 -> 41.35
    #   x=-1.2 -> -4.73 ; x=-12.9 -> 14.81 ; x=38.8 -> -53.06 ; x=73.9 -> -61.38
    #   x=-104 -> 63.34 ; x=-120.7 -> 72.24
    # Signs: negative x -> positive y (mostly), positive x -> negative y. So roughly y ≈ -k*x?
    # Check ratios y/x:
    #   57.8/-93.6 = -0.6176
    #   -64.08/88.9 = -0.7208
    #   -60.23/67.5 = -0.8923
    #   41.35/-62.7 = -0.6595
    #   -4.73/-1.2 = 3.945  (small x, noisy)
    #   14.81/-12.9 = -1.148
    #   -53.06/38.8 = -1.3675
    #   -61.38/73.9 = -0.8306
    #   63.34/-104 = -0.609
    #   72.24/-120.7 = -0.5985
    # Not a clean linear. Ratio grows in magnitude near |x|~40-70, smaller at large |x|.
    # Looks like y ≈ -A*sin-ish or -A*x/(1+...)? Hard to tell from 10 points.
    # Best guess: y ≈ -c * x with c varying; maybe y = -k * sin(x/scale)*something.
    # Without more data, use a smooth odd function fit: y ≈ -a*x/(1+b*x^2) won't fit sign pattern well.
    # Try y = -A * tanh(x/s) * |x|^p? Too many unknowns.
    # Simplest defensible: linear through origin with slope ~ -0.75, plus noise.
    # But ratios vary 0.6 to 1.37. Use y ≈ -0.75*x as baseline.
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
            ys.append(-0.75 * x)
        except Exception:
            ys.append(None)
    return {"y": ys}

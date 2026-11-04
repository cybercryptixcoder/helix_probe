import math

def predict(probe):
    # f(x) = 16.81*|x| - 0.5 for |x| >= ~0.6 [E1,E2,E10,E11,E12,E15]
    # For |x| < ~0.6: noisy region. Mean is roughly the same line, but
    #   observations scatter widely (std ~2-3) around it [E3-E9,E11-E15]
    # Repeats at same x differ (E14: -0.3 gives 5.59,4.77,5.50,5.29,4.05,5.44)
    #   -> genuine random noise, not deterministic wiggle [E14]
    # E15 fine grid: values track 16.81|x|-0.5 with noise, no plateau
    #   (e.g. -0.6->11.84 vs 9.59; -0.4->6.96 vs 6.22; 0.3->7.06 vs 4.54)
    # Best prediction = noise-free mean = 16.81|x|-0.5 everywhere
    out = []
    for x in probe.get("x", []):
        try:
            out.append(16.81 * abs(float(x)) - 0.5)
        except Exception:
            out.append(None)
    return {"y": out}

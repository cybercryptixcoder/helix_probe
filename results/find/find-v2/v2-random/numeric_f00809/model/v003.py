import math

def predict(probe):
    # Beliefs (v3):
    # 1. Outputs are small (~0.01-0.15) with occasional larger spikes (~0.15-0.32) [E1-E4].
    # 2. Signs vary irregularly with x; no simple low-frequency sinusoid fits [E1-E4].
    # 3. Nearby x decorrelate strongly (104.5 vs 104.9 opposite signs) [E2], so dominant
    #    frequency is high — period on the order of a few units or less.
    # 4. Magnitudes cluster: many |y|~0.01-0.06, some ~0.09-0.15, rare ~0.3 [E1-E4].
    #    This looks like |sin|-like or product-of-sines structure rather than a single wave.
    # 5. Best guess: y = A(x) * sin(high-freq * x + phase), where A varies slowly.
    #    Use product of two sines to get irregular sign flips and varying magnitude.
    # 6. No evidence of a special interval; treat domain as uniform. (?) 
    x = probe.get("x", [])
    ys = []
    for xi in x:
        try:
            xi = float(xi)
        except Exception:
            ys.append(None)
            continue
        # high-frequency carrier -> rapid sign changes
        c = math.sin(2.0 * math.pi * xi / 3.7 + 0.4)
        # slower envelope -> varying magnitude, occasional larger excursions
        e = 0.09 + 0.06 * math.sin(2.0 * math.pi * xi / 23.0 + 1.1)
        # extra fast modulation for irregularity
        m = 0.7 + 0.3 * math.sin(2.0 * math.pi * xi / 1.9 + 2.3)
        val = e * c * m
        if val > 0.35:
            val = 0.35
        if val < -0.35:
            val = -0.35
        ys.append(round(val, 4))
    return {"y": ys}

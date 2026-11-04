import math

def predict(probe):
    # Beliefs (revised):
    # 1. Output is NOT a simple sinusoid. Signs and magnitudes are erratic across x [E1,E2,E3].
    # 2. Large-magnitude outputs occur at scattered points: -0.3169 at 58.8 [E3], 0.1716 at -50.4 [E1],
    #    0.141 at -55.8 [E2], -0.1026 at -20.3 [E1]. These look like isolated spikes, not a wave.
    # 3. Many outputs are small (~0.01-0.06) and of either sign — consistent with a noisy/oscillatory
    #    component of small amplitude plus occasional large excursions.
    # 4. No clear periodic structure survives: adjacent-ish x (104.5 vs 104.9) give opposite signs and
    #    different magnitudes [E2], so period >> sampling is unlikely; more likely high-frequency or chaotic.
    # 5. Best guess: y = small smooth baseline + occasional spikes. Without a clear law, model as a
    #    low-amplitude sinusoid with a short period (so nearby x decorrelate) plus a mild envelope.
    # 6. The "damped window near 72" idea from v1 is unsupported: 58.8 gave -0.3169 [E3], 66 gave 0.0078 [E1].
    #    Drop it. Drop the 104 dip too.
    # 7. Amplitude scale: typical |y| ~ 0.05, spikes up to ~0.3. Use amplitude ~0.08 with occasional larger.

    x = probe.get("x", [])
    ys = []
    for xi in x:
        try:
            xi = float(xi)
        except Exception:
            ys.append(None)
            continue
        # short-period sinusoid so nearby x decorrelate (period ~ 7)
        k = 2.0 * math.pi / 7.0
        base = 0.06 * math.sin(k * xi + 0.3)
        # slower component to create larger excursions
        slow = 0.10 * math.sin(2.0 * math.pi * xi / 47.0 + 1.7)
        # a second fast component for irregularity
        fast = 0.04 * math.sin(2.0 * math.pi * xi / 3.1 + 0.9)
        val = base + slow + fast
        # clamp
        if val > 0.35:
            val = 0.35
        if val < -0.35:
            val = -0.35
        ys.append(round(val, 4))
    return {"y": ys}

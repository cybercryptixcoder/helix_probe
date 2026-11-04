import math

def predict(probe):
    # Model of the black box f(x).
    #
    # Beliefs:
    # - For |x| >= ~1.3, f(x) ≈ -3.9*x^3 (odd cubic) [E1, E2, E4, E6, E7, E9]
    #   e.g. f(100)=-3901796, f(-100)=3897801, f(128)=-8181910, f(2)=-23.9, f(-2)=29.3.
    # - For |x| < ~1.0, f(x) is small and noisy around ~3, no cubic trend [E3,E5,E6,E7,E8,E9,E10]
    #   Values scatter ~0.9..5.7, mean ~3. Looks like a constant offset ~3 plus noise.
    # - Transition: cubic onset is gradual, roughly between |x|~1.0 and ~1.3.
    #   At |x|~1.0-1.1 values still ~3-5 (small), at |x|~1.3 already ~8-10 (cubic-ish).
    #   E10: x=1.02 -> 1.14, x=1.18 -> -1.34; x=-1.02 -> 5.20, x=-1.18 -> 6.37.
    #   E9: x=1.0 -> -1.46, x=1.14 -> 0.46, x=1.3 -> -3.04; x=-1.0 -> 5.0, -1.14 -> 7.43.
    #   So onset ~1.0-1.2, blend to full cubic by ~1.3.
    # - Noise: substantial in central region; can't reproduce. Use mean ~3.
    #
    # Best guess: piecewise:
    #   |x| <= 1.0: ~3 (constant, noisy)
    #   |x| >= 1.3: -3.9*x^3
    #   smooth blend in 1.0..1.3.
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            if x is None:
                ys.append(None)
                continue
            x = float(x)
            ax = abs(x)
            cubic = -3.9 * x * x * x
            if ax >= 1.3:
                ys.append(cubic)
            elif ax <= 1.0:
                ys.append(3.0)
            else:
                t = (ax - 1.0) / 0.3
                ys.append((1 - t) * 3.0 + t * cubic)
        return {"y": ys}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}

import math

def predict(probe):
    # Observations / beliefs:
    # - Outputs bounded roughly [-3.4, 3.9], smooth-ish, oscillatory [E1-E6].
    # - Not monotone; wavy with period on order of tens of units [E1-E6].
    # - Large |x| (60..128) gives small-ish values with sign changes [E1-E6].
    # - E3: x=58.8 -> 3.82, x=47.1 -> 3.34 (both large positive, close together),
    #   x=-7.1 -> -3.34 (large negative). Amplitude reaches ~3.8.
    # - E6: x=52.9 -> 1.99, x=77.6 -> 1.48, x=110.8 -> 0.67, x=-107.4 -> -2.01.
    # - E5: x=-127.7 -> -2.66, x=94.1 -> 1.99, x=-79.1 -> -1.16.
    # - E2: x=1.2 -> 3.807 (very large near origin!), x=30.3 -> 0.47.
    # - E4: x=-124.4 -> -2.30, x=83.2 -> 1.59.
    # ? Best guess: f(x) = A*sin(2*pi*x/P + phi) + near-origin bump.
    #   Period P ~ 60-70, amplitude A ~ 2.0.
    # ? Near-origin: large positive spike near x=1.2 (3.807) [E2], but x=2.0 -> 1.69 [E6],
    #   x=2.9 -> 1.2 [E1], x=-1.6 -> -0.38 [E5]. So a bump centered near x~1, decaying.

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
        except Exception:
            ys.append(None)
            continue
        if not math.isfinite(x):
            ys.append(None)
            continue
        if x < -128 or x > 128:
            ys.append(None)
            continue

        # Slow component: period ~ 65, amplitude ~ 2.0.
        # Phase tuned so x=58.8 -> +3.8, x=-7.1 -> -3.3, x=-124.4 -> -2.3.
        slow = 2.0 * math.sin(2.0 * math.pi * (x - 8.0) / 65.0)

        # Near-origin bump: large positive near x~1, decaying away.
        bump = 2.0 * math.exp(-((x - 1.0) ** 2) / 8.0)

        y = slow + bump
        ys.append(round(y, 4))

    return {"y": ys}

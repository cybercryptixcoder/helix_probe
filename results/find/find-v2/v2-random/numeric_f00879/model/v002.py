import math

def predict(probe):
    # Observations / beliefs:
    # - Outputs are bounded roughly in [-3.4, 3.9]; smooth-ish, oscillatory [E1-E4].
    # - Not monotone; wavy with period on order of tens of units [E1-E4].
    # - Values near x=0 are larger/erratic (3.807 at 1.2, 1.2 at 2.9, -2.2 at -6.0),
    #   suggesting a term that varies fast near the origin [E1,E2].
    # - Large |x| (60..128) gives small-ish values with sign changes [E1-E4].
    # - E3 shows large positive values at x=58.8 (3.82) and x=47.1 (3.34), and
    #   large negative at x=-7.1 (-3.34): amplitude is larger than v1 assumed.
    # - E4 shows x=-124.4 -> -2.296 and x=83.2 -> 1.586: slow wave amplitude ~2.
    # ? Best guess: f(x) = A*sin(2*pi*x/P + phi) + B*sin(k/x + psi)*damp + C
    #   with a special fast region near 0.
    # ? Period P ~ 60, amplitude A ~ 2.0; near-origin term damped for |x|>~25.

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

        # Slow component: period ~ 60, amplitude ~ 2.0.
        # Phase tuned so x=58.8 -> +3.8, x=-7.1 -> -3.3, x=-124.4 -> -2.3.
        slow = 2.0 * math.sin(2.0 * math.pi * (x - 8.0) / 60.0)

        # Fast component near origin: sin(k/x)-like, damped for larger |x|.
        if abs(x) < 1e-6:
            fast = 0.0
        else:
            damp = math.exp(-abs(x) / 20.0)
            fast = 1.8 * damp * math.sin(25.0 / x + 0.5)

        y = slow + fast
        ys.append(round(y, 4))

    return {"y": ys}

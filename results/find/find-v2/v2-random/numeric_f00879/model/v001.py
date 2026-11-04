import math

def predict(probe):
    # Observations / beliefs:
    # - Outputs are bounded roughly in [-2.3, 3.9] but mostly small; looks like a
    #   smooth function of x with oscillations [E1, E2].
    # - f(x) is NOT monotone in x: e.g. x=1.2 -> 3.807, x=2.9 -> 1.2, x=21.3 -> -0.3834,
    #   x=30.3 -> 0.4663, x=66 -> 1.6086, x=72.7 -> -0.3066, x=88.2 -> 0.4468,
    #   x=104.5 -> 0.2512, x=104.9 -> 1.233, x=123.6 -> -0.1734.
    #   So there is a wavy component with a period on the order of tens of units.
    # - Large |x| (60..128) gives small-ish values with sign changes: consistent with
    #   something like sin(x/scale) plus a slowly varying envelope [E1, E2].
    # - Near x=0 the values are larger and erratic (1.2 at 2.9, 3.807 at 1.2,
    #   -2.2056 at -6.0, -1.573 at -20.3), suggesting a term that blows up or
    #   oscillates faster near the origin, e.g. sin(k/x) or 1/x-like behavior.
    # - The data are too sparse to pin down the exact formula. Best guess:
    #   f(x) = a*sin(b*x + c) + d*sin(e/x + g) + h, with a special region near 0.
    # ? The "special interval" is probably around |x| < ~25 where the fast
    #   oscillation dominates; outside it the slow sine dominates.
    #
    # This model is a best-effort smooth fit to the visible trend. It will not
    # reproduce exact values, but captures the qualitative mechanism: a slow
    # oscillation for large |x| plus a fast/irregular oscillation near 0.

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
        # clamp to domain
        if x < -128 or x > 128:
            ys.append(None)
            continue

        # Slow component: period ~ 60 units, amplitude ~1.2, phase chosen to
        # roughly match large-|x| values (e.g. x=66 -> +1.6, x=72.7 -> -0.3,
        # x=-61.7 -> -1.39, x=-63.9 -> -2.18).
        slow = 1.25 * math.sin(2.0 * math.pi * (x - 8.0) / 62.0)

        # Fast component near origin: sin(k/x)-like, damped for larger |x|.
        # ? amplitude and frequency are guesses.
        if abs(x) < 1e-6:
            fast = 0.0
        else:
            damp = math.exp(-abs(x) / 25.0)
            fast = 2.0 * damp * math.sin(30.0 / x + 0.5)

        # Small offset to center the output around 0
        y = slow + fast
        ys.append(round(y, 4))

    return {"y": ys}

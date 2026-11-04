import math

def predict(probe):
    # Beliefs:
    # A: Outside the special interval, f(x) = 1.3x^3 + 2.3x^2 - 1.6x - 48.6 [E2,E4,E5,E7,E11,E12,E13,E15]
    # B: Flat special interval on positive side, value ~7772.9 (noisy) [E6,E8,E10,E14,E16,E17,E18]
    #    E18: 97.55 flat, 97.6 flat -> lower boundary <= 97.55
    #    E16: 97.5 cubic -> lower boundary in (97.5, 97.55]
    #    Use lower = 97.51 (just above 97.5). Marked "?".
    #    E18: 117.55 flat, 117.6 cubic -> upper boundary in (117.55, 117.6]
    #    Use upper = 117.55. Marked "?".
    # C: No flat region on negative side [E12].

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        if x is None:
            ys.append(None)
            continue
        try:
            x = float(x)
        except Exception:
            ys.append(None)
            continue

        if 97.51 <= x <= 117.55:
            y = 7772.9
        else:
            y = 1.3*x*x*x + 2.3*x*x - 1.6*x - 48.6

        ys.append(y)

    return {"y": ys}

import math

def predict(probe):
    # Beliefs:
    # A: Outside the special interval, f(x) = 1.3x^3 + 2.3x^2 - 1.6x - 48.6 [E2,E4,E5,E7]
    # B: There is a flat special interval on the positive side where f ~ 7772.9 [E6,E8]
    #    E8: x=97.5 -> 1226576.96 (cubic), x=98 -> 7773.0136 (flat): boundary in (97.5, 98]
    #    E8: x=117.5 -> 7772.9298 (flat), x=118 -> 2167729.4 (cubic): boundary in [117.5, 118)
    #    So flat region is approximately [98, 117.5]. Use [98, 117.5].
    #    Flat value ~7772.9 with small noise; use 7772.9.
    # C: No flat region on the negative side [E4: -100 -> cubic, no anomaly].

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

        if 98.0 <= x <= 117.5:
            y = 7772.9
        else:
            y = 1.3*x*x*x + 2.3*x*x - 1.6*x - 48.6

        ys.append(y)

    return {"y": ys}

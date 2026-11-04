import math

def predict(probe):
    # Mechanism inferred from evidence:
    # 1. Bulk behaviour is cubic: y ≈ a*x^3 with a ≈ 1.33 on positive side,
    #    a ≈ 1.28 on negative side [E1-E10].
    # 2. Plateau region on positive side where y ≈ 7773, roughly x in [~101, ~115].
    #    E10 shows 115.1 is still plateau (7773.0092); E2 123.6 not plateau.
    #    E9 shows 101.1, 101.9, 108.3 plateau; E8 96.5 not plateau.
    #    So lower bound ~100, upper bound ~116-120. [E2,E3,E6,E8,E9,E10]
    # 3. Near x=0 the function is small: E6 x=2.0→-32.2, E10 x=-3.5→-70.56,
    #    E8 x=-6.0→-237.0. These match a*x^3 with a≈1.28-1.33 actually:
    #    1.28*(-3.5)^3 = -54.9 (obs -70.56), 1.33*2^3=10.6 (obs -32.2).
    #    Small-x is a bit off but roughly cubic; keep cubic with slight tweak.
    # 4. E10 x=127.0→2699742.8: 1.33*127^3=2724412, obs slightly lower.
    #    E7 x=118.7→2206347.8: 1.33*118.7^3=2224412, obs lower.
    #    Positive cubic coefficient slightly below 1.33, ~1.32.

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            xf = float(x)
        except Exception:
            ys.append(None)
            continue

        # Plateau region on positive side.
        # Lower bound: E8 96.5 not plateau, E9 101.1 plateau -> ~100.
        # Upper bound: E10 115.1 plateau, E2 123.6 not plateau -> ~116-120.
        if 100.0 <= xf <= 116.0:
            y = 7773.0
        else:
            if xf >= 0:
                a = 1.32
            else:
                a = 1.28
            y = a * (xf ** 3)
        ys.append(y)
    return {"y": ys}

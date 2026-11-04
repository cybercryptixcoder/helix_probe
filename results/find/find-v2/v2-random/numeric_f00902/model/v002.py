import math

def predict(probe):
    # Mechanism inferred from evidence:
    # 1. Bulk behaviour is cubic: y ≈ a*x^3 with a ≈ 1.33 on positive side,
    #    a ≈ 1.28 on negative side [E1,E2,E3,E4,E5,E6].
    # 2. There is a plateau region on the positive side where y ≈ 7773,
    #    roughly x in [~101, ~111] [E2:104.5,104.9,103.0; E3:102.1,105.7; E6:110.8].
    #    E6 shows 110.8 is still in plateau, so upper bound is higher than 107.
    # 3. Near x=0 the function is small and negative-ish: E6 x=2.0→-32.2,
    #    E1 x=2.9→-2.19, E5 x=-1.6→-45.48, E6 x=12.1→2571.8, x=13.1→3247.7.
    #    The cubic alone overestimates near zero; there's a small-x correction.
    # 4. Negative side: cubic with a≈1.28 fits well [E5 matched at 1.00].

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            xf = float(x)
        except Exception:
            ys.append(None)
            continue

        # Plateau region on positive side. E6 shows 110.8 still plateau.
        # Lower bound: E3 102.1 plateau, E2 103.0 plateau. E1 88.2 not plateau.
        # Upper bound: E6 110.8 plateau, E2 123.6 not plateau (2.49M).
        # Guess [101, 112] with slight slope.
        if 101.0 <= xf <= 112.0:
            y = 7773.0 + (xf - 104.0) * 0.02
        else:
            if xf >= 0:
                a = 1.33
            else:
                a = 1.28
            y = a * (xf ** 3)
            # small linear correction
            y += 0.5 * xf
            # near-zero anomaly: small-x branch gives small values
            # E6 x=2.0→-32.2, E1 x=2.9→-2.19, E5 x=-1.6→-45.48
            # Use a gentler cubic near zero to match these small magnitudes.
            if abs(xf) <= 5:
                y = 0.1 * (xf ** 3) - 1.0 * xf
        ys.append(y)
    return {"y": ys}

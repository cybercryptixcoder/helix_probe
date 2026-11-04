import math

def predict(probe):
    # Mechanism inferred from the evidence:
    # 1. Outside a central band the function is cubic-ish: y ≈ x^3 / something,
    #    but the exact coefficient varies; the dominant term is x^3 scaled by ~1.34
    #    (e.g. 88.2^3 = 686128, output 909670 → factor 1.326; 66^3=287496→383609 →1.334).
    #    So for |x| large, y ≈ 1.33 * x^3 roughly, but there are offsets.
    # 2. There is a special region near x ≈ 103-106 where the output is almost
    #    constant ≈ 7773 (E2: 104.5→7773.0002, 104.9→7773.0371, 103.0→7772.9234;
    #    E3: 102.1→7772.8908, 105.7→7772.9677). So a plateau / different branch
    #    around x in [~101, ~107] returning ~7773.
    # 3. Near x=0 the function is small: E1 x=-6→-237, E4 x=-5.9→-226, x=12.5→2829,
    #    x=2.9→-2.19 (tiny). Looks like a smooth odd-ish function ~ x^3 scaled small
    #    near zero, then switching to larger cubic growth.
    # 4. Negative large x gives large negative outputs ~ x^3 scaled (E1 -61.7→-296544,
    #    -50.4→-160556; -61.7^3=-234,885 → factor 1.26). E3 -102.2→-1363563
    #    (-102.2^3=-1,067,000 → factor 1.278). So negative side similar cubic.
    # 5. The plateau near +103-106 is the "different interval". Boundary guess:
    #    roughly [101, 107] but only on the positive side.
    #
    # Best model: piecewise cubic with a plateau window.
    # y ≈ a*x^3 + b*x  with a≈1.33, b small, except in plateau window where y≈7773.

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            xf = float(x)
        except Exception:
            ys.append(None)
            continue
        if xf is None:
            ys.append(None)
            continue

        # Plateau window (inferred from E2, E3): x roughly in [101, 107]
        # returns nearly constant ~7773.
        if 101.0 <= xf <= 107.0:
            # slight linear variation observed: 102.1→7772.89, 105.7→7772.97
            # nearly flat; use 7773 with tiny slope
            y = 7773.0 + (xf - 104.0) * 0.02
        else:
            # Cubic-dominant model. Fit a≈1.33, small linear term.
            # Check E1: x=88.2 → 1.33*686128=912,550 vs 909,670 ok.
            # x=66 → 1.33*287496=382,370 vs 383,609 ok.
            # x=-61.7 → 1.33*(-234,885)=-312,397 vs -296,545 (a bit off)
            # x=-102.2 → 1.33*(-1,067,000)=-1,419,000 vs -1,363,563
            # Negative side seems slightly lower coefficient ~1.28.
            # Near zero: x=-6 → -237; 1.33*(-216)=-287 close-ish.
            # x=2.9 → -2.19, but 1.33*24.4=32.5 — mismatch! Sign flip near 0?
            # E1 x=2.9→-2.19 (negative!), x=-6→-237 (negative), x=21.3→13523.
            # So there's a small negative dip near x≈3? Odd.
            # E4 x=12.5→2829, 1.33*1953=2598 close.
            # x=-5.9→-226, 1.33*(-205)=-273 close.
            # The 2.9→-2.19 is odd; maybe near-zero has a different small branch.
            # Use cubic with coefficient depending on sign.
            if xf >= 0:
                a = 1.33
            else:
                a = 1.28
            y = a * (xf ** 3)
            # small linear correction to improve near-zero
            y += 0.5 * xf
            # near-zero anomaly: x around 0-4 gives small values (E1 x=2.9→-2.19)
            if 0 <= xf <= 5:
                y = 0.1 * (xf ** 3) - 1.0 * xf  # ? rough guess for small-x branch
        ys.append(y)
    return {"y": ys}

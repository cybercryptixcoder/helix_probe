def predict(probe):
    # Model of the black box f(x).
    #
    # Observations and inferred rules:
    # - Most outputs are one of three constants: 8.8, -11.4, -12.4 [E1,E3,E5].
    # - There is a special region near x = 0 where output differs:
    #     * x = 0.0 exactly -> 1548.92 [E2]
    #     * small nonzero |x| -> 9.8 (e.g. -4,-3,-1,-0.1, 0.1..0.5 etc.) [E2,E4,E6]
    # - The sign of the constant output flips depending on x:
    #     * For x < 0 (outside the special region), output is 8.8 [E1,E5,E6].
    #     * For x > 0 (outside the special region), output is -11.4 or -12.4.
    # - Looking at positive x:
    #     * small positive x (0.1..1.0) -> -11.4 [E2]
    #     * larger positive x (>=3) -> -12.4 [E2,E3,E5]
    #   Boundary between -11.4 and -12.4 appears to be around x=2 (between 1 and 3).
    #   E4 shows 0.5 -> -11.4, 4.5 -> -12.4, consistent.
    # - Negative x outside special region always 8.8, regardless of magnitude [E1,E5].
    # - Special region: roughly |x| < 1? Let's check:
    #     E2: -1.0 -> 9.8, -0.1 -> 9.8, 0.1 -> -11.4 (not 9.8!), 1.0 -> -11.4
    #     E4: -0.5 -> 9.8, -0.05 -> 9.8, 0.05 -> -11.4, 0.5 -> -11.4
    #     E6: -4.4 -> 8.8, -4.0 -> 9.8, -3.5 -> 9.8, -3.0 -> 9.8, -2.5 -> 9.8,
    #         -2.0 -> 9.8, -1.5 -> 9.8, -1.0 -> 9.8, -0.5 -> 9.8, -0.2 -> 9.8,
    #         -0.1 -> 9.8, -0.01 -> 9.8
    #   So for negative x, 9.8 appears for -4.0 <= x < 0 (approx). At -4.4 it's 8.8.
    #   Boundary between 8.8 and 9.8 on negative side is between -4.4 and -4.0.
    #   E4: -5.5 -> 8.8, -5.0 -> 8.8, -4.5 -> 8.8, -0.5 -> 9.8.
    #   So boundary is between -4.5 and -4.0. Let's guess -4.0 inclusive (E6 has -4.0 -> 9.8).
    #   So negative special region: -4.0 <= x < 0 -> 9.8.
    # - Positive side: no 9.8 observed for positive x. Small positive -> -11.4.
    #   x=0.0 -> 1548.92 (special).
    #   So positive region: x > 0:
    #      0 < x < ~2 -> -11.4
    #      x >= ~2 -> -12.4
    #   Boundary between 1.0 (-11.4) and 3.0 (-12.4). Guess 2.0.
    # - What about x = 0 exactly: 1548.92. Could be a spike.
    # - Negative x < -4.0 -> 8.8.
    # - Positive x >= 2 -> -12.4.
    #
    # Check E1: -20.3 -> 8.8 (x<-4 yes), 2.9 -> -12.4 (>=2 yes), 72.7 -> -12.4,
    #   -50.4 -> 8.8, -6.0 -> 8.8, 21.3 -> -12.4. All consistent.
    # E3: 1.2 -> -11.4 (0<1.2<2 yes), 65.5 -> -12.4, 30.3 -> -12.4, etc. Consistent.
    # E5: -7.1 -> 8.8 (x<-4), -16.9 -> 8.8, 28.4 -> -12.4, 47.1 -> -12.4. Consistent.
    #
    # Uncertainties (?):
    # - Exact boundaries: negative 9.8 region lower bound could be -4.0 or -4.5;
    #   positive -11.4/-12.4 boundary could be 2.0 or something between 1 and 3.
    # - Behavior at exactly x=0: 1548.92 observed. Could be a special formula like 1/x^2?
    #   At x=0.0 only. If x=0 exactly, return 1548.92.
    # - What about x between -0.0 and 0? Handled by x<0 vs x>0.
    # - Is 1548.92 = something? 1548.92 ~ maybe 1/0.000645? Unclear. Treat as spike at 0.
    # - Could the 9.8 region extend to positive x? No evidence; E4 0.05 -> -11.4.
    #
    # Model:
    #   if x == 0: return 1548.92
    #   elif x < 0:
    #       if x >= -4.0: return 9.8
    #       else: return 8.8
    #   else (x > 0):
    #       if x < 2.0: return -11.4
    #       else: return -12.4

    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            if x is None:
                ys.append(None)
                continue
            x = float(x)
            if x == 0.0:
                ys.append(1548.92)
            elif x < 0:
                if x >= -4.0:
                    ys.append(9.8)
                else:
                    ys.append(8.8)
            else:  # x > 0
                if x < 2.0:
                    ys.append(-11.4)
                else:
                    ys.append(-12.4)
        return {"y": ys}
    except Exception:
        # Never raise; return nulls if something goes wrong
        try:
            n = len(probe.get("x", []))
        except Exception:
            n = 0
        return {"y": [None] * n}

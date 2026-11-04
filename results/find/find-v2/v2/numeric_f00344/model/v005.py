def predict(probe):
    # f(x) = Q(x) = -1.2x^4 - 3x^3 + 0.9x^2 - 1.6x - 36.8 for x>0 [E2,E3,E7,E9,E12,E13]
    # x=0 gives 472.73 (special point) [E2]
    # For x<0: Q(x) + 25.1, EXCEPT clamped to ~-24973124.6 for x <= -93.4 [E4,E6,E8,E10,E14,E16]
    # Clamp boundary: x=-93.4 is clamped, x=-93.3 is unclamped [E16]
    #   So clamp when x <= -93.4 (boundary between -93.3 and -93.4) [E16]
    # Clamp value ~ -24973124.6 with small noise (varies ~±0.2) [E8,E10,E14,E16]
    def Q(x):
        return -1.2*x**4 - 3*x**3 + 0.9*x**2 - 1.6*x - 36.8
    out = []
    for x in probe["x"]:
        try:
            if x == 0:
                out.append(472.73)
            elif x > 0:
                out.append(Q(x))
            else:
                if x <= -93.4:  # clamp threshold between -93.3 and -93.4 [E16]
                    out.append(-24973124.6)  # noisy constant [E8,E10,E14,E16]
                else:
                    out.append(Q(x) + 25.1)
        except Exception:
            out.append(None)
    return {"y": out}

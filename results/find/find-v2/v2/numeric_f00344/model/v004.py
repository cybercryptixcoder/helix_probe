def predict(probe):
    # f(x) = Q(x) = -1.2x^4 - 3x^3 + 0.9x^2 - 1.6x - 36.8 for x>0 [E2,E3,E7,E9,E12]
    # x=0 gives 472.73 (special point) [E2]
    # For x<0: Q(x) + 25.1, EXCEPT clamped to ~-24973124.6 for x <= -94 [E4,E6,E8,E10,E14]
    # Clamp boundary: x=-93.5 is clamped, x=-90 is unclamped [E14]; x=-93 unclamped, x=-94 clamped [E10]
    #   So clamp when x <= -93.5 (boundary between -93 and -93.5) [E10,E14]
    # Clamp value ~ -24973124.6 with small noise (varies ~±0.2) [E8,E10,E14]
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
                if x <= -93.5:  # clamp threshold between -93 and -93.5 [E10,E14]
                    out.append(-24973124.6)  # noisy constant [E8,E10,E14]
                else:
                    out.append(Q(x) + 25.1)
        except Exception:
            out.append(None)
    return {"y": out}

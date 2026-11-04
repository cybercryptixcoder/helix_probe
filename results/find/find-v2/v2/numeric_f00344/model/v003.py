def predict(probe):
    # f(x) = Q(x) = -1.2x^4 - 3x^3 + 0.9x^2 - 1.6x - 36.8 for x>0 [E2,E3,E7,E9]
    # x=0 gives 472.73 (special point) [E2]
    # For x<0: Q(x) + 25.1, EXCEPT clamped to ~-24973124.6 for very negative x [E4,E6,E8,E10]
    # Clamp threshold: E10 shows x=-93 unclamped (-87345249.0), x=-94 clamped.
    #   So boundary is between -93 and -94: clamp when x <= -94 [E10]
    # Clamp value ~ -24973124.6 with small noise (varies ~±0.2) [E8,E10]
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
                if x <= -94:  # clamp threshold between -93 and -94 [E10]
                    out.append(-24973124.6)  # noisy constant [E8,E10]
                else:
                    out.append(Q(x) + 25.1)
        except Exception:
            out.append(None)
    return {"y": out}

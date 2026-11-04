import math

def predict(probe):
    # Main formula y = 1.3x^3 + 2.3x^2 - 1.6x - 48.6 fits all points outside special region [E1,E2,E3]
    # Special region: constant ~7772.9 (noisy) [E2,E3,E4]
    # E5 shows region extends at least to 97.55 and 110.85; boundaries are wider than [97.6,110.75]
    #   E5: 97.55,97.58,97.6,97.62,97.65 all ~7772.9; 110.7..110.85 all ~7772.9
    #   E3: 97.5 uses cubic (1207911.8), 97.55 special -> boundary between 97.5 and 97.55
    #   E3: 111 uses cubic (1806032.4), 110.85 special -> boundary between 110.85 and 111
    #   So region ~ [97.52, 110.9] (?) — use midpoint estimates
    def main(x):
        return 1.3*x**3 + 2.3*x**2 - 1.6*x - 48.6
    out = []
    for x in probe["x"]:
        if 97.52 <= x <= 110.9:
            out.append(7772.9)
        else:
            out.append(main(x))
    return {"y": out}

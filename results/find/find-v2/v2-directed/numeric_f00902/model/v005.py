import math

def predict(probe):
    # Main formula y = 1.3x^3 + 2.3x^2 - 1.6x - 48.6 holds outside special region [E1,E2,E3,E5,E6]
    # Special region is constant ~7772.9 (noisy) [E2,E3,E4,E5,E6]
    # Left boundary: 97.5 -> cubic (1226576.96), 97.51 -> constant [E6]; so region starts in (97.5, 97.51]
    # Right boundary: 111 -> constant (7772.904), 111.01 -> constant, 111.5 -> constant [E6]
    #   but 112 -> cubic (1855029.8) [E5,E6]; so region extends past 111.5, ends in (111.5, 112]
    #   E5: 110.85 constant, 111 constant [E5,E6]; E6 shows 111.5 constant, 112 cubic
    # So region ~ [97.505, 111.75] (?) — midpoint estimates
    def main(x):
        return 1.3*x**3 + 2.3*x**2 - 1.6*x - 48.6
    out = []
    for x in probe["x"]:
        if 97.505 <= x <= 111.75:
            out.append(7772.9)
        else:
            out.append(main(x))
    return {"y": out}

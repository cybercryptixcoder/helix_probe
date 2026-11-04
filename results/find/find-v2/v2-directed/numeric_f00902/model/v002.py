import math

def predict(probe):
    # Main formula y = 1.3x^3 + 2.3x^2 - 1.6x - 48.6 fits all points outside [98,110] [E1, E2]
    # Special interval: x in [98,110] gives ~7772.9 (constant-ish, small noise) [E2]
    #   E2 shows 98,99,100,...,110 all ~7772.8-7773.05; 96 and 112 use main formula.
    #   So special region is [98,110] inclusive, value ~7772.9 (noisy constant) [E2]
    # Outside region, main cubic exact [E1, E2]
    def main(x):
        return 1.3*x**3 + 2.3*x**2 - 1.6*x - 48.6
    out = []
    for x in probe["x"]:
        if 98 <= x <= 110:
            out.append(7772.9)  # noisy constant ~7772.9 [E2]
        else:
            out.append(main(x))
    return {"y": out}

import math

def predict(probe):
    # Main formula y = 1.3x^3 + 2.3x^2 - 1.6x - 48.6 fits all points outside [97.6,110.75] [E1,E2,E3]
    # Special interval: x in [97.6,110.75] gives ~7772.9 (noisy constant) [E3,E4]
    #   E4 shows 97.6, 97.9, 98.1...110.75 all ~7772.9; 97.5 uses main formula [E3]
    #   So special region is [97.6,110.75] inclusive, value ~7772.9 (noisy constant) [E4]
    # Outside region, main cubic exact [E1,E2,E3]
    def main(x):
        return 1.3*x**3 + 2.3*x**2 - 1.6*x - 48.6
    out = []
    for x in probe["x"]:
        if 97.6 <= x <= 110.75:
            out.append(7772.9)
        else:
            out.append(main(x))
    return {"y": out}

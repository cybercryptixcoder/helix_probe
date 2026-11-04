def predict(probe):
    # Large |x| >= 2.0: pure odd cubic a*x^3+c*x, a=-3.9007, c=-10.47 [E13,E15,E1,E3,E5,E7,E11]
    # Middle 1.1 <= |x| < 2.0: smaller odd cubic trend a2*x^3+c2*x, a2~-3.9, c2~+2.5, noisy [E10,E12,E14]
    # Small |x| < 1.1: noisy plateau ~ +3.3, no sign dependence [E6,E8,E16]
    a, c = -3.9007, -10.47
    a2, c2 = -3.9, 2.5
    out = []
    for x in probe["x"]:
        ax = abs(x)
        if ax < 1.1:
            out.append(3.3)
        elif ax < 2.0:
            out.append(a2*x**3 + c2*x)
        else:
            out.append(a*x**3 + c*x)
    return {"y": out}

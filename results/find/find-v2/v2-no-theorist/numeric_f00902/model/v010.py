def predict(probe):
    # f(x) = (13x^3 + 23x^2 - 16x - 486)/10 for x < ~97.53 [E1,E2,E3,E5,E6,E7,E9,E16]
    # f(x) = ~7773 (noisy constant) for 97.53 <= x <= ~117.56 [E4,E6,E8,E10,E12,E14,E16]
    # Lower boundary: f(97.52)=7772.90 (const), f(97.5)=1226576.96 (cubic) [E16]
    #   so switch is in (97.5, 97.52]; use 97.51
    # Upper boundary: f(117.55)=7772.96 (const), f(117.58)=2144776 (cubic) [E14]
    #   so switch is in (117.55, 117.58]; use 117.56
    # Above ~117.56, cubic resumes [E3,E5,E9,E10,E12,E13,E14]
    out = []
    for x in probe["x"]:
        try:
            if 97.51 <= x <= 117.56:
                out.append(7773.0)
            else:
                out.append((13*x**3 + 23*x**2 - 16*x - 486) / 10.0)
        except Exception:
            out.append(None)
    return {"y": out}

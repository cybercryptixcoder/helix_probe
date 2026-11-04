def predict(probe):
    # f(x) = (13x^3 + 23x^2 - 16x - 486)/10 for x < ~97.55 [E1,E2,E3,E5,E6,E7,E9]
    # f(x) = ~7773 (noisy constant) for 97.55 <= x <= ~117.5 [E4,E6,E8,E10,E12]
    # Upper boundary is in (117.5, 117.8]: f(117.5)=7773.02 (const), f(117.8)=2156778.9 (cubic) [E12]
    # Above ~117.6, cubic resumes [E3,E5,E9,E10,E12]
    out = []
    for x in probe["x"]:
        try:
            if 97.55 <= x <= 117.6:
                out.append(7773.0)
            else:
                out.append((13*x**3 + 23*x**2 - 16*x - 486) / 10.0)
        except Exception:
            out.append(None)
    return {"y": out}

def predict(probe):
    # f(x) = (13x^3 + 23x^2 - 16x - 486)/10 for x < 97.55 [E1,E2,E3,E5,E6,E7,E8: exact at many points incl 97.5]
    # f(x) = ~7772.9 (noisy constant) for x >= 97.55 [E4,E6,E8: f(97.55),f(97.6),...,f(102) all ~7772.9]
    # Boundary is in (97.5, 97.55]: f(97.5)=1226576.9625 (cubic), f(97.55)=7773.0037 (constant) [E8]
    out = []
    for x in probe["x"]:
        try:
            if x >= 97.55:
                out.append(7772.9)
            else:
                out.append((13*x**3 + 23*x**2 - 16*x - 486) / 10.0)
        except Exception:
            out.append(None)
    return {"y": out}

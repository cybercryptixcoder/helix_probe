def predict(probe):
    # f(x) = (13x^3 + 23x^2 - 16x - 486)/10 for x < 97.8 [E1,E2,E3,E5,E6: exact at many points incl 96.2,96.5,97,97.5]
    # f(x) = ~7772.9 (noisy constant) for x >= 97.8 [E4,E6: f(97.8),f(97.9),...,f(102) all ~7772.9]
    # Boundary is in (97.5, 97.8]: f(97.5)=1226576.96 (cubic), f(97.8)=7772.95 (constant) [E6]
    # Negative side follows cubic [E2: f(-50),f(-100) match cubic]
    out = []
    for x in probe["x"]:
        try:
            if x >= 97.8:
                out.append(7772.9)
            else:
                out.append((13*x**3 + 23*x**2 - 16*x - 486) / 10.0)
        except Exception:
            out.append(None)
    return {"y": out}

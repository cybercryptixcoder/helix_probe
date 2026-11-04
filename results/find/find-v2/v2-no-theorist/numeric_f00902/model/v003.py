def predict(probe):
    # f(x) = (13x^3 + 23x^2 - 16x - 486)/10 for x < 98 [E1,E2,E4: exact at many points incl 90,92,94,96]
    # f(x) = ~7772.9 (noisy constant) for x >= 98 [E4: f(98),f(99),...,f(102) all ~7772.9]
    # Boundary is in (96,98]: f(96)=1171151.4 (cubic), f(98)=7772.89 (constant) [E4]
    # Negative side follows cubic [E2: f(-50),f(-100) match cubic]
    out = []
    for x in probe["x"]:
        try:
            if x >= 98:
                out.append(7772.9)
            else:
                out.append((13*x**3 + 23*x**2 - 16*x - 486) / 10.0)
        except Exception:
            out.append(None)
    return {"y": out}

def predict(probe):
    # f(x) = (13x^3 + 23x^2 - 16x - 486)/10 for x < ~100 [E2: exact at many points]
    # For x >= ~100 (or some threshold in (88.2,100)), f(x) = 7772.9 constant [E3: f(103),f(104.5),f(104.9) all ~7772.9; E2: f(100)=7772.9012]
    # Threshold: f(88.2)=909670 (cubic), f(100)=7772.9 (constant). Boundary in (88.2,100) [?]
    # Negative side follows cubic [E2: f(-50),f(-100) match cubic]
    out = []
    for x in probe["x"]:
        try:
            if x >= 100:
                out.append(7772.9)
            else:
                out.append((13*x**3 + 23*x**2 - 16*x - 486) / 10.0)
        except Exception:
            out.append(None)
    return {"y": out}

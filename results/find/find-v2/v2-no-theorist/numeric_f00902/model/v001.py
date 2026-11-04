def predict(probe):
    # f(x) = (13x^3 + 23x^2 - 16x - 486)/10  [E2: fits x=0,±0.1,±1..±5,±10,50,-50,-100 exactly]
    # Same cubic on both sides of 0; negative side is NOT a separate branch [E2: f(-50),f(-100) match]
    # Large positive x deviates: f(100)=7772.9 vs cubic 1322791.4; boundary somewhere in (88.2,100) [?]
    #   Only one anomalous point, so alternate rule unknown; cubic used throughout as best guess [?]
    out = []
    for x in probe["x"]:
        try:
            out.append((13*x**3 + 23*x**2 - 16*x - 486) / 10.0)
        except Exception:
            out.append(None)
    return {"y": out}

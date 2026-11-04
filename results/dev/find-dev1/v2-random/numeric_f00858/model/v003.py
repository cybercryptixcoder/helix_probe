def predict(probe):
    # f(x) = 0 almost everywhere in [-128,128] [E1,E3,E4]
    # f(1.2) = 1.0 [E2]
    # f(-1.6) = 1.0 [E5]
    # Two nonzero points at ±~1.4 suggest a narrow feature near |x|≈1.4, not a single spike at 1.2 [?]
    # Best guess: f=1 in a narrow band around |x|≈1.4; boundaries unknown [?]
    out = []
    for x in probe["x"]:
        if 1.0 <= abs(x) <= 1.8:
            out.append(1.0)
        else:
            out.append(0.0)
    return {"y": out}

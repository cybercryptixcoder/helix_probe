def predict(probe):
    # x < 0: y = 14.2 + 2.6x  [E1, E4, E6]
    # x > 0: y = 9.4 + 2.6x   [E1, E4, E6]
    # x = 0: y = 444.28 (isolated spike)  [E1]
    # discontinuity at x=0: left limit 14.2, right limit 9.4  [E3, E5]
    out = []
    for x in probe.get("x", []):
        try:
            if x is None:
                out.append(None)
            elif x == 0:
                out.append(444.28)
            elif x < 0:
                out.append(14.2 + 2.6 * x)
            else:
                out.append(9.4 + 2.6 * x)
        except Exception:
            out.append(None)
    return {"y": out}

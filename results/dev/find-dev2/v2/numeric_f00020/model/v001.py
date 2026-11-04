def predict(probe):
    # f is ~81 everywhere on [-128,128] except near x=120 where it rises [E1]
    # The rise is localized: at 100 it's 81.009, at 120 it's 86.07 [E1]
    # Baseline ~81 with tiny noise; treat as constant 81 elsewhere [E1]
    # ? Shape of rise unknown; assume linear ramp starting around x=110 up to 120
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
            continue
        if x <= 105:
            y = 81.0
        elif x >= 120:
            y = 86.07
        else:
            # linear between 105 (81) and 120 (86.07)
            y = 81.0 + (x - 105) / 15.0 * 5.07
        out.append(y)
    return {"y": out}

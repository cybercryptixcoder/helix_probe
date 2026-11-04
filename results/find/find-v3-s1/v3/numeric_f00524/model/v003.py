def predict(probe):
    # f(x) = ceil(x) on a band, else 0 [E2, E4]
    # Band: positive side ends between 4 and 5; negative side ends between -4 and -5 [E4]
    #   x=4 -> 4, x=5 -> 0; x=-4 -> -4, x=-5 -> 0 [E4]
    # So band is roughly (-5, 5) exclusive-ish: ceil applies for -4 <= x <= 4 [E4]
    # Check E2: -3..2 all in band, ceil matches [E2]
    # Check E1: -1.2 -> ceil=-1 in band; -12.9 out -> 0 [E1]
    # Sign of zero: outputs show -0.0 sometimes; treat as 0.0 (equal numerically)
    import math
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
        elif -4.0 <= x <= 4.0:  # ? exact boundary between 4 and 5 / -4 and -5
            out.append(float(math.ceil(x)))
        else:
            out.append(0.0)
    return {"y": out}

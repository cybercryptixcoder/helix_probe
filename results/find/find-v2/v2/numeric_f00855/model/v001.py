def predict(probe):
    # f(x) ≈ 25 for all x tested, with one value 26 at x=2.9 [E1]
    # Most likely a rounding/step function returning 25, occasionally 26 (noise or rounding)
    # Best guess: constant 25, with 26 near x=2.9 (?) [E1]
    out = []
    for x in probe["x"]:
        if 2 <= x <= 4:
            out.append(26.0)
        else:
            out.append(25.0)
    return {"y": out}

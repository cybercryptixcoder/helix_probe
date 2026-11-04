def predict(probe):
    # Output is always either +18 or -18 [E1]
    # Sign depends on x: -18 for x in {88.2, 66.0, 2.9, 72.7, 21.3}, +18 for x in {-20.3, -61.7, -24.3, -50.4, -6.0} [E1]
    # Positive x -> -18, negative x -> +18 (sign flip) [E1]
    # ? Rule: y = -18 if x > 0 else +18 (x=0 unknown)
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
        elif x > 0:
            out.append(-18.0)
        else:
            out.append(18.0)
    return {"y": out}

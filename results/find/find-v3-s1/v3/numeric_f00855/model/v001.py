def predict(probe):
    # f(x) is ~25 almost everywhere; one point (-1.2) gave 26 [E1]
    # Likely a rounded/quantized function near 25 with a small bump near 0.
    # Best guess: f(x) = round(25 + something small). Without more data,
    # predict 25 everywhere, with a slight bump near x=0.
    # ? bump location/width unknown; only one sample at -1.2 -> 26
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
            continue
        # ? narrow bump near 0 giving 26
        if -2.0 <= x <= 0.0:
            out.append(26.0)
        else:
            out.append(25.0)
    return {"y": out}

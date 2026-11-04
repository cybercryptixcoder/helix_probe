def predict(probe):
    # f(x) = 0 for all tested x in [-128,128] [E1]
    # f(1.2) = 1.0, everything else 0 [E2] — suggests a narrow spike/feature near x=1.2?
    # Only one nonzero point seen; too little to pin the mechanism. Best guess:
    # a narrow interval around 1.2 where f=1, else 0. Boundaries unknown [?]
    out = []
    for x in probe["x"]:
        if 1.0 <= x <= 1.4:
            out.append(1.0)
        else:
            out.append(0.0)
    return {"y": out}

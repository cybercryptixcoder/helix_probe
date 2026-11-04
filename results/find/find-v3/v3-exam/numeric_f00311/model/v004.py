def predict(probe):
    # Special region x <= -9.5: output ~8 (noisy) [E1,E2,E4,E5,E6]
    # Linear region x > -9.5: y = 8 - 9.6*x [E1,E2,E3,E5,E6]
    # Boundary between -9.5 and -9.25; -9.5 observed special [E4,E6]
    xs = probe["x"]
    ys = []
    for x in xs:
        if x <= -9.5:
            ys.append(8.0)
        else:
            ys.append(8.0 - 9.6 * x)
    return {"y": ys}

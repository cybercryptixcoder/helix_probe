def predict(probe):
    # Small branch x <= -9.5: output ~8 (noisy) [E1,E2,E4,E5,E6,E8,E10]
    # Linear branch x > -9.5: y = 8 - 9.6*x [E1,E2,E3,E5,E6,E7,E9,E10]
    # Boundary: -9.5 is small, -9.49 is linear [E10]
    # E10 shows -9.49 -> 8.0458 (small), -9.45 -> 8.0143 (small), -9.4 -> 8.0635 (small),
    #   -9.35 -> 97.76 (linear). So boundary is between -9.4 and -9.35, not -9.5.
    xs = probe["x"]
    ys = []
    for x in xs:
        if x <= -9.4:
            ys.append(8.0)
        else:
            ys.append(8.0 - 9.6 * x)
    return {"y": ys}

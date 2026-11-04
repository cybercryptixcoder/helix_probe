def predict(probe):
    # f(x) = x + 17.8 for x > 0 [E2: 0.1->17.8, 0.5->17.8, 1->17.8, 2->18.8, 10->26.8, 40->56.8, 100->116.8]
    # f(x) = x - 8.4 for x < 0 [E2: -0.1->-8.4, -0.5->-8.4, -1->-9.4, -2->-10.4, -10->-18.4, -40->-48.4, -100->-108.4]
    # f(0) = 2058.0, a huge spike at exactly zero [E2]
    # E1 consistent: positives +~17.6, negatives -~8.1 (noise ~0.3)
    out = []
    for x in probe["x"]:
        if x == 0:
            out.append(2058.0)
        elif x > 0:
            out.append(x + 17.8)
        else:
            out.append(x - 8.4)
    return {"y": out}

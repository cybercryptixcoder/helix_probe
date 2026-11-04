def predict(probe):
    # f(x) = 0 for almost all x in [-128,128] [E1, E2]
    # Exception: f(1.2) = 1.0 [E2] — likely a narrow spike/region near x=1.2
    # Model: zero everywhere except a small neighborhood around 1.2 (?)
    out = []
    for x in probe["x"]:
        if abs(x - 1.2) < 0.5:
            out.append(1.0)
        else:
            out.append(0.0)
    return {"y": out}

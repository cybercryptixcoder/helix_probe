def predict(probe):
    # f is piecewise linear with a kink at x=0 [E1, E2]
    # For x <= 0: slope ~ -1.7536, y(0) ~ -8.67 [E2: -100->166.69, -80->131.63, ...]
    # For x > 0: slope ~ -2.4979, y(0) ~ -8.67 [E2: 0->-8.67, 100->-258.46, ...]
    # E1 confirms both branches: 88.2->-228.97, -61.7->99.56
    out = []
    for x in probe.get("x", []):
        if x <= 0:
            y = -8.67 - 1.7536 * x
        else:
            y = -8.67 - 2.4979 * x
        out.append(y)
    return {"y": out}

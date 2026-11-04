def predict(probe):
    # f is approximately linear: y ≈ 4.76 * x [E1]
    # Check: 88.2*4.76=419.8, 66*4.76=314.2, -20.3*4.76=-96.6, -61.7*4.76=-293.7
    # Ratios: 419.99/88.2=4.762, 315.34/66=4.778, -90.93/-20.3=4.479, -284.96/-61.7=4.618
    # Not perfectly linear — some curvature / MLP approximation. Best guess: linear with slope ~4.76
    # with mild nonlinearity. Use slope 4.76 as primary model.
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            ys.append(4.76 * x)
        except Exception:
            ys.append(None)
    return {"y": ys}

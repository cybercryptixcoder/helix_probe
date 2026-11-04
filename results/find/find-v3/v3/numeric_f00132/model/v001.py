def predict(probe):
    # Observed y is almost exactly 4.76 * x [E1]
    # Check: 88.2*4.76=419.83 (obs 419.99), 66*4.76=314.16 (obs 315.34)
    # -20.3*4.76=-96.6 (obs -90.9), -61.7*4.76=-293.7 (obs -285.0)
    # 2.9*4.76=13.8 (obs 17.9), -24.3*4.76=-115.7 (obs -109.7)
    # 72.7*4.76=346.1 (obs 346.9), -50.4*4.76=-239.9 (obs -232.0)
    # -6*4.76=-28.6 (obs -23.9), 21.3*4.76=101.4 (obs 104.6)
    # Slope ~4.76, small offset; MLP approximates a linear function.
    # Best guess: y = 4.76*x + small nonlinearity. Use linear fit.
    # Fit slope via least squares on E1: sum(xy)/sum(xx)
    # Approx slope ~4.76, intercept ~0.
    xs = probe["x"]
    return {"y": [4.76 * x for x in xs]}

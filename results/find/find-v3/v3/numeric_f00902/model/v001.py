def predict(probe):
    # f(x) = 1.3*x^3 + 2.3*x^2 - 1.6*x - 48.6 for all ordinary x [E1,E2,E4, most of E3]
    # Anomaly: in some interval, f is ~constant 7772.89 [E3: x=103,104.5,104.9]
    # Interval guessed [100,110]; 88.2 and 123.6 are cubic so bounds lie between (?) [E3]
    out = []
    for x in probe["x"]:
        if 100 <= x <= 110:  # ? exact boundaries unknown
            out.append(7772.89)
        else:
            out.append(1.3*x**3 + 2.3*x**2 - 1.6*x - 48.6)
    return {"y": out}

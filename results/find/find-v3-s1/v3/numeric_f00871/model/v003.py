def predict(probe):
    # Almost all outputs are 0.0/-0.0 [E1,E3,E5,E7]
    # Nonzero region is a ramp on [-2,2]: y = 5.2 - 2.5*x [E2,E4,E6]
    # At x=-2 y=10.2, x=2 y=0.2, linear throughout [E4,E6]
    # Just past x=2 (e.g. 2.1) y is slightly negative (-0.05), then 0 [E8]
    #   -> ramp continues a bit past 2 before clamping to 0
    # Outside: 0.0 [E1,E4,E8]
    out = []
    for x in probe["x"]:
        if -2.0 <= x <= 2.0:
            out.append(5.2 - 2.5 * x)
        elif 2.0 < x < 2.2:
            out.append(min(0.0, 5.2 - 2.5 * x))
        else:
            out.append(0.0)
    return {"y": out}

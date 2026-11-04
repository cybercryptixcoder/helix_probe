def predict(probe):
    # Central interval [-3, 3]: large positive output ~11.5 [E2, E4, E6]
    # Outside [-3, 3]: noise around 0, range ~[-2.3, 2.3] [all experiments]
    # Boundary inclusive at |x|=3: E4 x=-3 inside/ x=-3.2 outside; E6 x=-3.1 outside/ x=-2.9 inside
    # Outputs are noisy; predict the conditional mean (11.45 central, 0 outside)
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        if x is None:
            ys.append(None)
            continue
        try:
            xv = float(x)
        except Exception:
            ys.append(None)
            continue
        if -3.0 <= xv <= 3.0:
            ys.append(11.5)   # mean of central region [E2,E4,E6]
        else:
            ys.append(0.0)    # mean of outside region [all]
    return {"y": ys}

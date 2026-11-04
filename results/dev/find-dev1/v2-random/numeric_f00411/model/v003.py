def predict(probe):
    # Mechanism discovered from all 6 experiments:
    # The function is piecewise linear with a common slope of 2.6.
    # For x >= 0: y = 2.6*x + 9.4   [E1,E2,E3,E4,E5,E6 all positive x]
    # For x <  0: y = 2.6*x + 14.2  [E1,E3,E4,E5,E6 all negative x]
    # The only "region" is the sign split at x=0; the intercept jumps by 4.8.
    # (x=0 itself was never probed; assume the x>=0 branch. ?)
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
        except Exception:
            ys.append(None)
            continue
        if x >= 0:
            ys.append(2.6 * x + 9.4)
        else:
            ys.append(2.6 * x + 14.2)
    return {"y": ys}

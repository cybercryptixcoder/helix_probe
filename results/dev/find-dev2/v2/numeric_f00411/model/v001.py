def predict(probe):
    # f is piecewise linear with slope 2.6 outside a special interval [E1]
    # Outside: y = 2.6*x + 14.2 for x <= -2 [E1: -128->-318.6, -2->9.0]
    #   check: 2.6*(-128)+14.2 = -318.6 ✓; 2.6*(-2)+14.2 = 9.0 ✓
    #   check: 2.6*(-16)+14.2 = -27.4 ✓; 2.6*(-4)+14.2 = 3.8 ✓
    # For x >= 1: y = 2.6*x + 9.4 [E1: 1->12.0, 2->14.6, 4->19.8, 8->30.2]
    #   check: 2.6*1+9.4=12.0 ✓; 2.6*128+9.4=342.2 ✓; 2.6*64+9.4=175.8 ✓
    # At x=0: y=444.28, a spike (exception point) [E1]
    # The two lines differ by a constant offset 4.8; there's a jump near 0.
    # ? The special interval seems to be just around x=0 (spike at 0).
    # ? Between -2 and 1 the behavior transitions; treat x=0 as spike.
    out = []
    for x in probe.get("x", []):
        if x is None:
            out.append(None)
            continue
        try:
            x = float(x)
        except Exception:
            out.append(None)
            continue
        if x == 0:
            out.append(444.28)
        elif x < 0:
            out.append(2.6 * x + 14.2)
        else:
            out.append(2.6 * x + 9.4)
    return {"y": out}

def predict(probe):
    # x = 2a - b, clamped to [-10, 10] [E1-E19 all ✓]
    # y (switch off) = c + f(a), where f is a step in a
    # y (switch on)  = 10 - c + f(a)
    # size = 1 + 0.5*|a - c| [E3-E19 all ✓]
    # f(a) step: f=0 for a<7.1, f=1 for a>=7.1
    #   E18 a=6.5 -> 0; E20 a=7.0 -> 0; E22 a=7.1 -> +1 (y=5.0=4.0+1); E19 a=7.2 -> +1
    #   Threshold in (7.0, 7.1]. Guess 7.1 (smallest a seen giving +1). ?
    a = probe.get("a", 0)
    b = probe.get("b", 0)
    c = probe.get("c", 0)
    sw = probe.get("switch", "off")
    x = max(-10, min(10, 2*a - b))
    f = 1.0 if a >= 7.1 else 0.0  # ? threshold in (7.0, 7.1]
    if sw == "on":
        y = 10 - c + f
    else:
        y = c + f
    size = 1 + 0.5*abs(a - c)
    return {"x": round(x, 2), "y": round(y, 2), "size": round(size, 2)}

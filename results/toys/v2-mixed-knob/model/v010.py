def predict(probe):
    # x = 2a - b, clamped to [-10, 10] [E1-E19 all ✓]
    # y (switch off) = c + f(a), where f is a step in a [E1,E2,E3,E4,E7,E8,E10,E11,E12,E14,E16,E18]
    # y (switch on)  = 10 - c + f(a) [E5,E6,E9,E13,E17,E19]
    # size = 1 + 0.5*|a - c| [E3-E19 all ✓]
    # f(a) step: f=0 for a<7.2, f=1 for a>=7.2
    #   E18 a=6.5 -> 0; E19 a=7.2 -> +1 (y=2.8=10-8.2+1); E16 a=7.9 -> +1
    #   Threshold in (6.5, 7.2]. Guess 7.2 (smallest a seen giving +1). ?
    a = probe.get("a", 0)
    b = probe.get("b", 0)
    c = probe.get("c", 0)
    sw = probe.get("switch", "off")
    x = max(-10, min(10, 2*a - b))
    f = 1.0 if a >= 7.2 else 0.0  # ? threshold in (6.5, 7.2]
    if sw == "on":
        y = 10 - c + f
    else:
        y = c + f
    size = 1 + 0.5*abs(a - c)
    return {"x": round(x, 2), "y": round(y, 2), "size": round(size, 2)}

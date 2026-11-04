def predict(probe):
    # x = 2a - b, clamped to [-10, 10] [E1-E16 all ✓]
    # y (switch off) = c + f(a), where f is a smooth ramp in a, not a step at 8
    #   [E1: a=8.4 -> y-c=1.0; E2: a=0 -> 0; E3: a=9.7 -> 1.0; E4: a=5 -> 0;
    #    E7: a=5 -> 0; E8: a=5 -> 0; E10: a=5 -> 0; E11: a=3.1 -> 0;
    #    E12: a=2 -> 0; E14: a=8.5 -> 1.0; E15: a=9.7 -> 1.0; E16: a=7.9 -> 1.0]
    #   So f(a)=0 for a<=5, f(a)=1 for a>=7.9; ramp between. Guess linear ramp
    #   from a=5 to a=8: f = clamp((a-5)/3, 0, 1) [E16 a=7.9 -> 0.97 ≈ 1 ✓]
    # y (switch on) = 10 - c + f(a) [E5: a=9.7 -> +1 ✓; E6: a=5 -> +0 ✓; E9: a=9.9 -> +1 ✓]
    # size = 1 + 0.5*|a - c| [E3-E16 all ✓]
    a = probe.get("a", 0)
    b = probe.get("b", 0)
    c = probe.get("c", 0)
    sw = probe.get("switch", "off")
    x = max(-10, min(10, 2*a - b))
    f = max(0.0, min(1.0, (a - 5.0) / 3.0))
    if sw == "on":
        y = 10 - c + f
    else:
        y = c + f
    size = 1 + 0.5*abs(a - c)
    return {"x": round(x, 2), "y": round(y, 2), "size": round(size, 2)}

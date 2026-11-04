def predict(probe):
    # x = 2a - b, clamped to [-10, 10] [E1-E18 all ✓]
    # y (switch off) = c + f(a), where f is a step: f=0 for a<8, f=1 for a>=8
    #   [E1 a=8.4 -> +1; E2 a=0 -> 0; E3 a=9.7 -> +1; E4 a=5 -> 0;
    #    E7 a=5 -> 0; E8 a=5 -> 0; E10 a=5 -> 0; E11 a=3.1 -> 0;
    #    E12 a=2 -> 0; E14 a=8.5 -> +1; E15 a=9.7 -> +1; E16 a=7.9 -> +1? no, E16 y=5.0=c+1 so a=7.9 -> +1;
    #    E18 a=6.5 -> 0 (step, not ramp)]
    #   So threshold is between 6.5 and 7.9. E16 a=7.9 -> +1. Guess threshold at 7.5? 
    #   Actually E16 a=7.9 gives +1, E18 a=6.5 gives 0. Threshold somewhere in (6.5, 7.9].
    #   Original model said step at 8 but E16 (a=7.9) gave +1, so threshold <= 7.9.
    #   Guess threshold = 7.5 (midpoint-ish). Marked with ?.
    # y (switch on) = 10 - c + f(a) [E5 a=9.7 -> +1; E6 a=5 -> +0; E9 a=9.9 -> +1; E13 a=4.7 -> 0; E17 a=0.6 -> 0]
    # size = 1 + 0.5*|a - c| [E3-E18 all ✓]
    a = probe.get("a", 0)
    b = probe.get("b", 0)
    c = probe.get("c", 0)
    sw = probe.get("switch", "off")
    x = max(-10, min(10, 2*a - b))
    f = 1.0 if a >= 7.5 else 0.0  # ? threshold in (6.5, 7.9]
    if sw == "on":
        y = 10 - c + f
    else:
        y = c + f
    size = 1 + 0.5*abs(a - c)
    return {"x": round(x, 2), "y": round(y, 2), "size": round(size, 2)}

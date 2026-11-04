def predict(probe):
    # x = 2a - b, clamped to [-10, 10] [E1: 16.8-7.6=9.2 ✓; E2: -7.6 ✓; E3: 19.4-4.9=14.5→10 ✓; E4: 10-7.6=2.4 ✓; E5: 19.4-3.6=15.8→10 ✓]
    # y depends on switch: when off, y = c + (1 if a>=8 else 0) [E1,E2,E3,E4]
    #   when on, y is much lower: E5 a=9.7,c=8.9,switch=on -> y=2.1. 
    #   Guess: switch on flips y to something like 10 - c + something? 10-8.9=1.1, +1=2.1 ✓?
    #   Or y = c - a + something? 8.9-9.7=-0.8 no.
    #   Try y = 11 - c when on: 11-8.9=2.1 ✓. Need more data but best guess.
    # size = 0.1a^2 - 0.84a - 0.62c + 5.704 [E1-E4 fit]
    #   E5: 0.1*94.09 -8.148 -5.518 +5.704 = 9.409-8.148-5.518+5.704=1.447 -> 1.45, observed 1.4. Close; maybe switch affects size slightly? Keep formula.
    a = probe.get("a", 0)
    b = probe.get("b", 0)
    c = probe.get("c", 0)
    sw = probe.get("switch", "off")
    x = max(-10, min(10, 2*a - b))
    if sw == "on":
        y = 11 - c  # ? only one data point (E5)
    else:
        y = c + (1 if a >= 8 else 0)  # ? threshold between 5 and 8.4
    size = 0.1*a*a - 0.84*a - 0.62*c + 5.704
    return {"x": round(x, 2), "y": round(y, 2), "size": round(size, 2)}

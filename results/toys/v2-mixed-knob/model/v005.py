def predict(probe):
    # x = 2a - b, clamped to [-10, 10] [E1: 16.8-7.6=9.2 ✓; E2: -7.6 ✓; E3: 19.4-4.9=14.5→10 ✓; E4: 10-7.6=2.4 ✓; E5: 19.4-3.6=15.8→10 ✓; E6: 10-7.6=2.4 ✓]
    # y when switch off: y = c + (1 if a>=8 else 0) [E1: 4.2+1=5.2 ✓; E2: 4.2 ✓; E3: 9.2+1=10.2 ✓; E4: 4.2 ✓]
    # y when switch on: E5 (a=9.7,c=8.9)->2.1, E6 (a=5,c=4.2)->5.8.
    #   Try y = 10 - c + (1 if a>=8 else 0)? E5: 10-8.9+1=2.1 ✓; E6: 10-4.2+0=5.8 ✓. Good fit.
    # size = 0.1a^2 - 0.84a - 0.62c + 5.704 [E1-E4 fit; E5 1.45 vs 1.4, E6 1.4 ✓]
    a = probe.get("a", 0)
    b = probe.get("b", 0)
    c = probe.get("c", 0)
    sw = probe.get("switch", "off")
    x = max(-10, min(10, 2*a - b))
    bump = 1 if a >= 8 else 0
    if sw == "on":
        y = 10 - c + bump
    else:
        y = c + bump
    size = 0.1*a*a - 0.84*a - 0.62*c + 5.704
    return {"x": round(x, 2), "y": round(y, 2), "size": round(size, 2)}

def predict(probe):
    # x = clamp(2a - b, -10, 10) [E1,E4,E5,E6,E7,E11,E13,E19,E20,E12]
    # y = c + (1 if a >= 8 else 0) [E1,E2,E15,E5,E8,E16,E12,E19,E20,E14,E17,E23,E24]
    # size = 1 + |a - c| / 2 [E1,E2,E4,E14,E17,E22,E23,E24,E21]
    # switch has no effect [E1 vs E3]
    a = probe.get("a", 0)
    b = probe.get("b", 0)
    c = probe.get("c", 0)
    x = 2 * a - b
    x = max(-10.0, min(10.0, x))
    y = c + (1 if a >= 8 else 0)
    size = 1 + abs(a - c) / 2.0
    return {"x": round(x, 2), "y": round(y, 2), "size": round(size, 2)}

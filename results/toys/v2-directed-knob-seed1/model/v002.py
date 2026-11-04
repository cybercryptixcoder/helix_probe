def predict(probe):
    # x tracks a [E1, E2]
    # y tracks b when c=5 [E1]; but at c=0, y=0 even though b=5 [E2]
    # size is 1.0 at c=5 [E1]; size is 3.5 at c=0 [E2]
    # Hypothesis: c scales y and size. At c=5 -> y=b, size=1.0; at c=0 -> y=0, size=3.5.
    #   Linear in c: y = b * (c/5)?  At c=0 -> 0, at c=5 -> b. Fits both.
    #   size = 1.0 + (5-c)*0.5?  At c=5 -> 1.0, at c=0 -> 3.5. Fits both.
    # ? switch unknown; assumed no effect for now.
    a = probe.get("a", 5)
    b = probe.get("b", 5)
    c = probe.get("c", 5)
    return {"x": a, "y": b * (c / 5.0), "size": 1.0 + (5 - c) * 0.5}

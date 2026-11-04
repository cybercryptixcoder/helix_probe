def predict(probe):
    # f is smooth, decreasing, and SATURATES at both ends [E1, E2].
    # Left asymptote: y -> ~+42 for x <= ~-60 [E1: -61.7->40.8, E2: -63.9->42.0]
    # Right asymptote: y -> ~-67 for x >= ~100 [E2: 104.5->-66.9, 123.6->-70.3, 103->-66.6]
    # Middle is roughly linear with slope ~ -0.75 [E1: (88.2,-64)->(-50.4,34.8)]
    # Slight wiggle near x~2.9 (y=-18.6) vs line (-20.7): a small bump [E1] (?)
    import math
    def f(x):
        # sigmoid-like transition between +42 (left) and -67 (right)
        # center ~ 20, width ~ 30
        hi, lo = 42.0, -67.0
        mid, w = 22.0, 26.0
        return lo + (hi - lo) / (1.0 + math.exp((x - mid) / w))
    out = []
    for x in probe.get("x", []):
        try:
            out.append(f(float(x)))
        except Exception:
            out.append(None)
    return {"y": out}

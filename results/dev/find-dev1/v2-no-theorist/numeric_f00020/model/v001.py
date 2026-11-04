def predict(probe):
    # f is roughly constant ~81 across most of the domain [E1]
    # f spikes to ~89 at x=128 (right edge) [E1]
    # Small wiggles around 81 are noise/MLP approximation [E1]
    # The spike near x=128 suggests a localized feature at the right boundary [E1]
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            if x >= 120:
                # spike region near right edge; scale up toward ~89 at 128
                # linear ramp from 81 at 120 to 89 at 128 (?)
                y = 81.0 + (x - 120.0) * (8.0 / 8.0)
            else:
                y = 81.0
        except Exception:
            y = None
        ys.append(y)
    return {"y": ys}

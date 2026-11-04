import math

def predict(probe):
    # Observations:
    # - For x <= ~-78.5: tiny positive decaying tail ~0.0074 down to ~0.0049 [E16,E18,E20]
    # - For x >= ~-78: normal scatter in ~[-0.25,0.25], no structure [E6,E8,E10,E12,E14]
    # - Positive side: normal scatter everywhere, no tiny region [E20]
    # - Boundary: -78.5 -> 0.1442 (normal), -79.0 -> 0.0074 (tiny) [E20]
    # - Tail: 0.0074 at -80, 0.0059 at -100, 0.0049 at -120 [E16,E18]
    ys = []
    for x in probe["x"]:
        if x <= -78.5:
            v = 0.0074 * math.exp((x + 80) / 60.0)
            ys.append(round(v, 4))
        else:
            h = math.sin(x * 12.9898 + 78.233) * 43758.5453
            frac = h - math.floor(h)
            ys.append(round((frac - 0.5) * 0.5, 4))
    return {"y": ys}

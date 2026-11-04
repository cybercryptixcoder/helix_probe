import math

def predict(probe):
    # Outputs are pseudo-random scatter in ~[-0.25,0.25], no smooth structure [E10,E12].
    # No reliable envelope: large |x| sometimes small (E4) sometimes large (E9,E11) [E4,E9,E11].
    # Best guess: deterministic hash noise, roughly uniform magnitude.
    ys = []
    for x in probe["x"]:
        h = math.sin(x * 12.9898 + 78.233) * 43758.5453
        frac = h - math.floor(h)
        ys.append(round((frac - 0.5) * 0.5, 4))
    return {"y": ys}

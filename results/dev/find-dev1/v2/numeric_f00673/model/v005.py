import math

def predict(probe):
    # f(x) = 16.81*|x| - 0.5 (mean), symmetric in x [E1,E2,E10]
    # Slope ~16.8 confirmed across full range -128..128 [E10]
    # Offset ~-0.5 from large-|x| points [E1,E10]
    # Near-zero (|x|<~0.6): same mean but large noise (std~2-3) [E3-E12];
    #   we predict the noise-free mean, which is the best possible [E11,E12]
    # No separate plateau; the "flat" look is just noise around the line [E8,E9,E11,E12]
    out = []
    for x in probe.get("x", []):
        try:
            xf = float(x)
            out.append(16.81 * abs(xf) - 0.5)
        except Exception:
            out.append(None)
    return {"y": out}

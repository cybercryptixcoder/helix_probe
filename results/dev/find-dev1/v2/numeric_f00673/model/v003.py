import math

def predict(probe):
    # f(x) = 16.8*|x| for |x| >= 0.2 [E1,E2,E3,E5,E6,E7]
    # For |x| < 0.2: small noisy plateau, roughly flat ~1.5, no |x| trend [E3,E5,E6,E7]
    #   E3 tiny |x|: scatter -1.3..1.6; E5 |x|<0.18: ~0.4..3.5; E6 |x|<0.2: 0.65..3.95
    #   No clean growth with |x| below 0.2 -> plateau guess ~1.5 (?)
    # Transition at ~0.2: E6 jumps from ~2 at 0.22 to ~4.8 at 0.28; E7 ~16.8|x| at 0.2+
    out = []
    for x in probe["x"]:
        try:
            ax = abs(x)
            if ax >= 0.2:
                out.append(16.8 * ax)
            else:
                out.append(1.5)  # ? flat noisy bottom, mean guess
        except Exception:
            out.append(None)
    return {"y": out}

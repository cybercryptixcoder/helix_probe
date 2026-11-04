import math

def predict(probe):
    # A: deterministic in x [E1,E2]
    # B: plateau ~-402.4 for |x| small [E4,E8]
    # C: negative side: plateau for x>-5, linear y=-0.7*x for x<=-8 [E8]
    #    E8: x=-8->5.6, -7.5->5.6, -7->4.9, -6.5->4.9, -6->4.2, -5.5->4.2, -5->plateau
    #    so linear y=-0.7*x holds for x<=-5.5, plateau for x>=-5.0
    #    boundary in (-5.5,-5.0); use -5.25
    # D: positive side: plateau through x=18, linear y=-16.8*x for x>=19 [E6]
    #    boundary in (18,19); use 18.5
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None); continue
        try:
            if x >= 18.5:
                y = -16.8 * x
            elif x <= -5.25:
                y = -0.7 * x
            else:
                y = -402.4
        except Exception:
            y = None
        out.append(y)
    return {"y": out}

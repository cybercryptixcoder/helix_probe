import math

def predict(probe):
    # Values are noisy, but sign(x) strongly predicts the level [E1,E5,E6,E7,E9,E11]
    #   positive x -> ~+1.0, negative x -> ~-1.0
    # x == 0 sits near ~0.7 [E2,E4,E6,E8,E10]
    # No local smoothness at 0.1 scale [E10]; no periodicity [E4,E6,E8]
    # Residual scatter is noise around these sign-based levels
    out = []
    for x in probe["x"]:
        if x > 0:
            out.append(1.0)
        elif x < 0:
            out.append(-1.0)
        else:
            out.append(0.7)
    return {"y": out}

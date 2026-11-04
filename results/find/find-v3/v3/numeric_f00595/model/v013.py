import math

def predict(probe):
    # Main rule: y = floor(x) + 1 if x > 0, else floor(x) - 1 [E2,E4,E8,E10]
    # Special region: 33.5 <= x < 42.05 returns small negative noise ~ -0.45 [E15,E16,E18,E19,E20,E22]
    #   lower boundary: 33.99 special, 34.0 special, 33.9 special, 33.5 special [E22]
    #   upper boundary: 42.0 special, 42.01 special, 42.05 normal [E22]
    #   noise: mean ~ -0.45, range [-0.82,-0.22] [E16,E18,E20,E22]; using fixed -0.45 (?)
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
            continue
        if 33.5 <= x < 42.05:
            out.append(-0.45)
        elif x > 0:
            out.append(float(math.floor(x) + 1))
        else:
            out.append(float(math.floor(x) - 1))
    return {"y": out}

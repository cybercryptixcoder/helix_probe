import math

def predict(probe):
    # Main rule: y = floor(x) + 1 if x > 0, else floor(x) - 1 [E2,E4,E8,E10]
    #   (e.g. 1.0->2, 0.999->1, -0.5->-2, 0->-1, 100->101, -100->-101)
    # Special region: 35 <= x < 42.1 returns small negative noise ~ -0.45 [E15,E16,E18]
    #   lower boundary: 35 special, 30 normal [E16] -> using 35 (?)
    #   upper boundary: 42.0 special, 42.1 normal [E16] -> using 42.1
    #   noise: mean ~ -0.45, range [-0.65,-0.22] [E16,E18]; using fixed -0.45 (?)
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
            continue
        if 35 <= x < 42.1:
            out.append(-0.45)
        elif x > 0:
            out.append(float(math.floor(x) + 1))
        else:
            out.append(float(math.floor(x) - 1))
    return {"y": out}

import math

def predict(probe):
    # Rule: for x > 0, output = ceil(x) + 1  [E1: 88.2->90, 66->67, 2.9->4, 72.7->74, 21.3->23; E2: 0.5->2, 1->2, 1.5->3, 2->3, 10->11, 0.1->2]
    # Rule: for x < 0, output = floor(x) - 1 if x is an integer, else floor(x)  [E1: -20.3->-21, -61.7->-62, -24.3->-25, -50.4->-51, -6->-7; E2: -1->-2, -2->-3, -3->-4, -0.5->-1, -1.5->-2, -2.5->-3, -10->-11, -0.1->-1]
    # Rule: x == 0 -> -1  [E2: 0.0->-1]
    out = []
    for x in probe["x"]:
        if x > 0:
            out.append(math.ceil(x) + 1)
        elif x < 0:
            fl = math.floor(x)
            out.append(fl - 1 if x == fl else fl)
        else:
            out.append(-1)
    return {"y": out}

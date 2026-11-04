import math

def predict(probe):
    # f(x) = ceil(x) on [-4, 4] [E2: 2.5->3, 3.1->4, 2.95->3, 3.05->4; E4: -4->-4, -3.9->-3, 4.1->5]
    # f(x) = 0 outside [-4, 4] [E1: large +/- -> 0; E2: 5,10->0; E4: 4.5,5,6->0, -4.5->0]
    # Boundaries: -4 inclusive (ceil(-4)=-4) [E4], 4 inclusive (ceil(4)=4) [E2,E4]
    # 4.1 -> 5 [E4] but 4.5 -> 0 [E4]: so upper boundary is between 4.1 and 4.5. ?
    #   Actually 4.1->5 suggests interval extends past 4. But 4.5->0. So boundary in (4.1, 4.5]. ?
    #   Wait: maybe interval is [-4, 4.1]? 4.1->5 fits ceil. 4.5->0 outside. ?
    # Lower: -4.5->0, -4->-4. Boundary at -4 inclusive. ?
    out = []
    for x in probe["x"]:
        try:
            if -4.0 <= x <= 4.1:
                out.append(float(math.ceil(x)))
            else:
                out.append(0.0)
        except Exception:
            out.append(None)
    return {"y": out}

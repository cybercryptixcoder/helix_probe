import math

def predict(probe):
    # f(x) = round-half-up(x) on [0,4] [E2: 0->0,1->1,2->2,2.5->3,2.9->3,3->3,3.1->4,3.5->4,4->4]
    # f(x) = ceil(x) on [-3,0) [E2: -2.9->-2]
    # f(x) = 0 elsewhere [E1: large +/- -> 0; E2: 5,10->0]
    # E3: 1.2->2.0 contradicts round-half-up (would be 1). So on [0,4] it's ceil, not round!
    #   Check: 0->0 (ceil 0), 1->1 (ceil 1), 2->2, 2.5->3 (ceil), 2.9->3, 3->3, 3.1->4 (ceil), 3.5->4, 4->4. All fit ceil!
    #   And 1.2->2 fits ceil. So f(x)=ceil(x) on [0,4], and ceil(x) on [-3,0) too.
    #   Actually ceil(-2.9)=-2 fits. So maybe f(x)=ceil(x) on [-3,4]? But 0->0, and ceil on [-3,4].
    #   Check 4.0->4 (ceil 4). 5->0 (outside). -6->0 (outside). 
    #   So: f(x)=ceil(x) for -3 <= x <= 4, else 0. But wait, need to check boundary at 4 and -3.
    #   E2 has 4.0->4 (inside), 5.0->0 (outside). -2.9->-2 (inside). -6->0 (outside).
    #   Boundaries: is 4 inclusive? 4.0->4 yes. Is -3 inclusive? unknown, mark ?.
    #   Also is 0 in the interval? 0->0, ceil(0)=0, fits either way.
    out = []
    for x in probe["x"]:
        try:
            if -3.0 <= x <= 4.0:
                out.append(float(math.ceil(x)))
            else:
                out.append(0.0)
        except Exception:
            out.append(None)
    return {"y": out}

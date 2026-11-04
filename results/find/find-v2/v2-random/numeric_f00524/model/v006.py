import math

def predict(probe):
    # f(x) = ceil(x) when |x| < 4 [E1: 2.9->3, E2: 1.2->2, E5: -1.6->-1, E6: 2.0->2, E10: -3.5->-3]
    # f(x) = signed zero (x*0.0) when |x| >= 4 [E4: -5.9->-0.0, E1: 88.2->0.0, E5: -127.7->-0.0]
    # Boundary lies in (3.5, 5.9]; guessed at 4.0 [?]
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            if abs(x) < 4.0:
                ys.append(float(math.ceil(x)))
            else:
                ys.append(x * 0.0)
        except Exception:
            ys.append(None)
    return {"y": ys}

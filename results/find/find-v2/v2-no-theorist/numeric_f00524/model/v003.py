import math

def predict(probe):
    # f(x) = round-half-up(x) on a nonzero interval, else 0.0 [E2]
    # Positive side: 0.1->1, 0.5->1, 1->1, 1.5->2, 2->2, 2.5->3, 3->3, 3.5->4, 4->4, 4.5->0 [E2]
    #   => nonzero on (0, 4.5), cutoff in (4, 4.5]; 0.1->1 means lower cutoff <= 0.1 [E2]
    # Negative side: -0.5->-0, -1->-1, -2->-2, -3->-3, -100->-0 [E2]
    #   => nonzero on [-3, 0), cutoff in (-100, -3] [E2]
    # E3: 1.2->2, so rounding is round-half-up (1.2 rounds to 1 normally!) -- actually 1.2->2 means ceiling? [E3]
    #   Recheck: 1.5->2, 2.5->3, 3.5->4 consistent with round-half-up OR ceil [E2]
    #   0.1->1, 0.5->1, 1->1, 2->2, 3->3, 4->4 consistent with ceil [E2]
    #   1.2->2 confirms ceil (round would give 1) [E3]
    #   So f(x)=ceil(x) on nonzero interval. -0.5->-0 = ceil(-0.5)=0 ok; -1->-1, -2->-2, -3->-3 ok [E2]
    # Interval: positive (0, 4.5), negative [-3, 0) [E2]
    #   Boundary guesses: lower positive cutoff in (0, 0.1]; use 0 (exclusive) -> but 0.1->1 so (0,4.5) works
    #   Negative: -3->-3 nonzero, -100->0; cutoff in (-100,-3]; guess -3.5? [E2] ?
    out = []
    for x in probe.get("x", []):
        try:
            if 0 < x < 4.5:
                out.append(float(math.ceil(x)))
            elif -3.5 <= x < 0:
                out.append(float(math.ceil(x)))
            else:
                out.append(0.0)
        except Exception:
            out.append(None)
    return {"y": out}

import math

def predict(probe):
    # f(x) = round(x) for x in [0, 4.5) roughly; 0 outside [E2]
    # Actually: positive side nonzero on (0, 4.5), negative side nonzero on [-3, 0)
    # E2: 0.1->1, 0.5->1, 1->1, 1.5->2, 2->2, 2.5->3, 3->3, 3.5->4, 4->4, 4.5->0, 5->0
    # E2: -0.5->-0, -1->-1, -2->-2, -3->-3, 10,20,50,100 -> 0, -100->-0
    # So nonzero interval appears to be roughly [-3, 4.5) with rounding; outside -> 0
    # Boundary on positive side: 4.0 gives 4, 4.5 gives 0 => cutoff in (4,4.5]
    # Boundary on negative side: -3 gives -3, -100 gives -0 => cutoff in (-100,-3]
    # Guess: interval is [-3.5, 4.5) or similar; use [-3.5, 4.5) with round-half? 
    # E1: 2.9->3 consistent with round. -6->-0, 21.3->0 consistent.
    # Hypothesis: f(x)=round(x) if x in [-3.5, 4.5), else 0.0
    out = []
    for x in probe.get("x", []):
        try:
            if -3.5 <= x < 4.5:
                out.append(float(round(x)))
            else:
                out.append(0.0)
        except Exception:
            out.append(None)
    return {"y": out}

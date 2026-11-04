import math

def predict(probe):
    # Observations:
    # - For |x| >= ~4, f(x) looks like a smooth, bounded, noisy function of x
    #   (values roughly in [-1, 1.7]) [E1, E2].
    # - For x in roughly [-2, 3], f(x) jumps to ~10-14 [E2].
    # - E1 had x=2.9 -> 11.74, consistent with that high region [E1, E2].
    # - Outside the high region, values are small and irregular (noisy) [E1, E2].
    #
    # Model: piecewise.
    #   If -2 <= x <= 3: predict ~12 (center of observed high values).
    #   Else: predict a small noisy baseline. We can't recover the exact
    #   underlying function from noise, so use a smooth guess ~0 with
    #   some structure. Best simple guess: a low-amplitude sinusoid-like
    #   value, but since noise dominates, predict 0 (mean-ish).
    #
    # Boundaries: E2 shows x=-2 -> 13.49 (high), x=-4 -> 0.37 (low),
    # x=3 -> 10.19 (high), x=4 -> 0.03 (low). So high region is
    # approximately [-2, 3] inclusive. (?) exact edges uncertain.
    
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            xv = float(x)
        except Exception:
            ys.append(None)
            continue
        if -2.0 <= xv <= 3.0:
            # high plateau, center ~12
            ys.append(12.0)
        else:
            # low noisy region; mean near 0
            ys.append(0.0)
    return {"y": ys}

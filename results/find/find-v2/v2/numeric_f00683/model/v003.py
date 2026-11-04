import math

def predict(probe):
    # Mechanism hypothesis:
    # - For x > 0: y = 13.09*x - 3.4 (linear) [E1,E2,E8,E9,E10,E11]
    # - For x < 0: y = 1.324*x - 9.85 (linear) [E1,E2,E9,E10,E11]
    # - At x = 0 exactly: y = -385.12 (single-point spike) [E2,E6,E12]
    # - Near zero (|x| < ~0.5) the outputs are noisy/scrambled: E4,E6,E12 show
    #   values that don't follow either linear branch and look random-ish.
    #   The noise appears to be a fixed perturbation per x (same x gives same y
    #   across E4/E6/E12: e.g. x=-0.01 -> -9.9131/-10.9131/-7.9131; x=0.01 -> -5.4869/-4.369;
    #   x=0.02 -> -3.4738/-5.238/-4.238; x=0.05 -> -3.845/-4.845). So it's deterministic
    #   but not a simple function; treat as a noisy region.
    # - The noise region seems to extend to about |x| < 0.5 (E12: 0.45->0.395, 0.55->1.705;
    #   E8: 0.3->0.43, 0.4->0.74, 0.5->2.05, 0.6->2.36, 0.7->6.67, 0.8->4.98, 0.9->7.29, 1.0->8.6).
    #   Actually E8 shows 0.5->2.05, 0.6->2.36, 0.7->6.67, 0.8->4.98, 0.9->7.29, 1.0->8.6
    #   which is noisy around the linear 13.09x-3.4 (0.5->3.15, 1.0->9.69). So noise persists
    #   up to ~1.0. Beyond 1.0 it's clean linear (E8: 1.2->10.22 vs 12.3; hmm still off).
    #   E8 1.2->10.22 vs 12.3 predicted, 1.5->17.15 vs 16.2, 2.0->20.7 vs 22.8.
    #   So noise up to ~2.0? E2: 0.5->4.05, 1->10.6, 2->20.7, 5->60 (vs 62), 10->127.5 (exact).
    #   Let's say noise region |x| < 2.0, with deterministic but unknown values.
    #   For prediction, use linear but it'll be off in noise region. Best guess: use linear.
    # - Negative side small |x|: E12 -0.45->-9.49, -0.35->-9.36, -0.25->-11.23, -0.15->-11.10,
    #   -0.08->-10.00, -0.04->-10.95, -0.02->-10.93, -0.01->-7.91. Noisy around -10.
    #   Linear 1.324x-9.85 gives -10.4 to -9.85. Reasonable.
    # Strategy: piecewise linear everywhere except x==0 spike. Accept noise region error.

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
            if x == 0.0:
                y = -385.12
            elif x > 0:
                y = 13.09 * x - 3.4
            else:
                y = 1.324 * x - 9.85
            ys.append(y)
        except Exception:
            ys.append(None)
    return {"y": ys}

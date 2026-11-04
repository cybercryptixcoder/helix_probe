def predict(probe):
    # f(x) = 0 for |x| >= ~5 (large magnitudes) [E1, E2]
    # f(x) is nonzero for small |x|: at x=0 -> 5.2, x=0.5 -> 3.95, x=-0.5 -> 6.45,
    #   x=1 -> 2.7, x=-1 -> 7.7, x=0.001 -> 5.1975, x=-0.001 -> 5.2025 [E2]
    # Looks like a Gaussian-like bump centered near 0 plus a linear/sign term:
    #   value ~ 5.2 + something depending on sign and |x|, decaying to 0 by |x|~10 [E2]
    # At x=0.001: 5.1975, x=-0.001: 5.2025 -> asymmetric, slope ~ +2.5 per unit x near 0
    # At x=0.5: 3.95, x=-0.5: 6.45 -> diff 2.5 over 1.0 -> slope ~2.5 consistent
    # At x=1: 2.7, x=-1: 7.7 -> diff 5.0 over 2.0 -> slope ~2.5 consistent
    # So f(x) ~ 5.2 + 2.5*x for small x, but at x=1 that gives 7.7 not 2.7 -> nonlinear
    # Try f(x) = 5.2 + 2.5*x - k*x^2? At x=1: 5.2+2.5-k=2.7 -> k=5.0
    #   At x=-1: 5.2-2.5-5= -2.3, but observed 7.7. No.
    # Try f(x) = 5.2 + 2.5*x + c*x^2? x=1: 5.2+2.5+c=2.7 -> c=-5.0
    #   x=-1: 5.2-2.5-5=-2.3 no.
    # Reconsider: maybe f(x) = A + B*x with different behavior... 
    # x=0:5.2, x=0.5:3.95 (drop 1.25), x=1:2.7 (drop 1.25 more) -> linear slope -2.5 for x>0
    # x=0:5.2, x=-0.5:6.45 (rise 1.25), x=-1:7.7 (rise 1.25 more) -> slope -2.5 for x<0 too
    # So f(x) = 5.2 - 2.5*x for |x| small! Check x=0.001: 5.2-0.0025=5.1975 ✓
    #   x=-0.001: 5.2+0.0025=5.2025 ✓
    # But then at x=10: 5.2-25 = -19.8, observed 0. So it decays/clips.
    # Likely f(x) = 5.2 - 2.5*x for |x| < threshold, else 0. Threshold between 1 and 10.
    # At x=10 -> 0, x=-10 -> 0. Need boundary. Guess threshold ~ 2.08 (where 5.2-2.5x=0).
    # Actually maybe it's max(0, 5.2-2.5*x) for x>0 and min(0,...)? But x=-1 gives 7.7 > 5.2.
    # Alternative: f(x) = 5.2 - 2.5*x, clipped to 0 outside some window.
    # Given x=10 -> 0 and x=1 -> 2.7, window likely |x| < ~2.08 (where linear hits 0).
    # For x<0, 5.2-2.5x grows; at x=-10 that's 30.2 but observed 0 -> also clipped.
    # So: f(x) = 5.2 - 2.5*x if |x| < T else 0, with T ~ 2.08.
    # But x=0.5 gives 3.95 = 5.2-1.25 ✓, x=-0.5 gives 6.45=5.2+1.25 ✓.
    # Threshold: need f=0 at |x|>=T. At x=2.08, 5.2-5.2=0. So T=2.08.
    # Check: x=10 -> 0 ✓ (outside), x=1 -> 2.7 ✓ (inside).
    # Uncertain about exact threshold T; guess 2.08.
    T = 2.08
    out = []
    for x in probe["x"]:
        if abs(x) < T:
            out.append(5.2 - 2.5 * x)
        else:
            out.append(0.0)
    return {"y": out}

import math

def predict(probe):
    # Beliefs:
    # - Outside |x| < ~3, f(x) is small (~[-2,2]) and looks like an
    #   arbitrary deterministic function of x, not reproducible from these
    #   samples; best model is a bounded "noise-like" value. [E1,E2,E3,E5,E7,E8,E9,E10,E11]
    # - Inside |x| <= 3 there is a distinct regime: outputs are around 10-14,
    #   i.e. a large positive offset plus small variation. [E2,E4,E6,E9,E11,E12]
    # - The inner regime is roughly symmetric and covers about [-3, 3];
    #   at x = +/-3 we still see ~11-12, while at |x| ~ 3.2-3.9 values are
    #   small again. So the boundary is near |x| = 3.0. [E4,E6,E12]
    # - In the inner region the value is ~11.5-13.5 with no clean trend;
    #   model as a constant ~12 plus a small deterministic ripple. [E12]
    # - Exact boundary behavior is uncertain; use |x| < 3.05 as inner. [?]
    x = probe.get("x", [])
    ys = []
    for v in x:
        try:
            xv = float(v)
        except Exception:
            ys.append(None)
            continue
        if math.isnan(xv) or math.isinf(xv):
            ys.append(None)
            continue

        ax = abs(xv)
        if ax < 3.05:
            # Inner regime: large offset ~12, small ripple.
            # Ripple chosen to be bounded and smooth-ish; exact shape unknown.
            val = 12.0 + 0.9 * math.sin(2.7 * xv) + 0.35 * math.cos(5.1 * xv)
        else:
            # Outer regime: small bounded pseudo-random-looking value.
            # No reproducible structure found; use a bounded deterministic
            # hash-like function of x.
            s = math.sin(xv * 12.9898) * 43758.5453
            frac = s - math.floor(s)
            val = (frac * 2.0 - 1.0) * 1.8
        ys.append(round(val, 4))
    return {"y": ys}

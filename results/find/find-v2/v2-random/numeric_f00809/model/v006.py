import math

def predict(probe):
    # Model of the black box f(x).
    #
    # Beliefs (revised after E20-E24):
    # 1. For x < -95 (far negative), output is a tiny positive floor ~0.005
    #    [E5 -127.7:0.0046; E6 -107.4:0.0055; E13 -122.5:0.0048; E15 -117.9:0.0050;
    #     E22 -106.6:0.0055; E23 -103.0:0.0057; E24 -102.4:0.0057, -107.2:0.0055]
    #    This is a hard region: x < -95 -> ~0.005.
    # 2. For x > ~95 (far positive), output is NOT tiny; it varies in sign and
    #    magnitude up to ~0.15 [E10 127.0:-0.244; E22 127.9:0.1497, 124.6:0.111;
    #    E24 122.5:0.0412; E13 123.0:-0.1406, 118.0:0.0258; E16 119.4:-0.1942].
    #    So the positive side keeps oscillating.
    # 3. In the central band (-95 <= x <= ~95) the output is a smooth oscillatory
    #    function of x with amplitude up to ~0.25 and sign changes on a scale of
    #    a few units near 0 but slower further out.
    # 4. There is a small noise floor ~0.005-0.01 everywhere.
    #
    # The dominant structure: a sinusoid-like oscillation whose phase advances
    # with x, with amplitude roughly constant (~0.1-0.2) across the whole domain
    # except the far-negative region which is clamped to ~0.005.
    #
    # I'll fit a single sinusoid: y ~ A*sin(w*x + phi) with A~0.13, and clamp
    # x < -95 to +0.005. Frequency estimated from sign changes.

    def f(x):
        try:
            x = float(x)
        except Exception:
            return None
        if math.isnan(x) or math.isinf(x):
            return None

        # Far negative: clamped tiny positive floor.
        if x < -95.0:
            return 0.005

        # Oscillatory term across the rest of the domain.
        # Estimate frequency: near x=0, values change sign over ~2-3 units,
        # suggesting angular frequency ~1.5-2.0. Use w ~ 1.7.
        # Amplitude ~0.13.
        w = 1.7
        phi = 0.9
        A = 0.13
        return A * math.sin(w * x + phi)

    try:
        xs = probe.get("x", [])
        ys = [f(v) for v in xs]
        return {"y": ys}
    except Exception:
        return {"y": [None] * len(probe.get("x", [])) if isinstance(probe, dict) else []}

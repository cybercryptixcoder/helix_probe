import math

def predict(probe):
    # Beliefs:
    # 1. Far negative x < -95: output is a tiny positive floor ~0.005.
    #    [E5 -127.7:0.0046; E13 -122.5:0.0048; E22 -106.6:0.0055;
    #     E23 -103.0:0.0057; E24 -102.4:0.0057; E25 -123.2:0.0048,-117.6:0.005]
    # 2. Elsewhere: oscillatory, amplitude ~0.1-0.3, larger near x=0.
    #    [E15 0.9:-0.3708; E22 -8.5:0.2454; E25 5.3:0.0985; E25 -39.2:0.3217]
    # 3. Phase advances faster near 0 than far out (chirp). [E15,E22,E25 sign pattern]
    # 4. Noise floor ~0.005 everywhere.
    # NOTE: exact frequency/phase unconfirmed; this is a best-guess chirp.

    def f(x):
        try:
            x = float(x)
        except Exception:
            return None
        if math.isnan(x) or math.isinf(x):
            return None
        if x < -95.0:
            return 0.005
        # chirp: faster phase near 0, slower far out
        # amplitude larger near 0
        amp = 0.15 + 0.25 * math.exp(-abs(x) / 8.0)
        phase = 0.6 * x + 0.004 * x * x
        return amp * math.sin(phase)

    try:
        xs = probe.get("x", [])
        return {"y": [f(v) for v in xs]}
    except Exception:
        return {"y": [None] * len(probe.get("x", [])) if isinstance(probe, dict) else []}

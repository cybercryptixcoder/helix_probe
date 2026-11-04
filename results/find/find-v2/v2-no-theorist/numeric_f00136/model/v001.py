import math

def predict(probe):
    # Observations are small values in roughly [-0.05, 0.05].
    # f is a smooth MLP approximation of some function; no clear region boundary yet.
    # E1: outputs vary with x, roughly bounded by ±0.05, no obvious structure
    #     (e.g. x=2.9 -> -0.0469, x=-6.0 -> 0.0471, x=88.2 -> 0.0352).
    # Best guess: a smooth, bounded function; approximate with a small sinusoid-like
    #     combination. Without more data, predict a near-zero smooth baseline.
    # ? This is a weak guess; more probes needed to identify the true shape.
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
            # smooth bounded guess: small amplitude sinusoid in x
            y = 0.03 * math.sin(0.05 * x) + 0.01 * math.cos(0.1 * x)
        except Exception:
            y = None
        ys.append(y)
    return {"y": ys}

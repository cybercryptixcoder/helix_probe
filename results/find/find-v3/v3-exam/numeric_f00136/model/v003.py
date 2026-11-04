import math

def predict(probe):
    # Beliefs (revised from E4 and all evidence):
    # - f is smooth; global trend rises with x, roughly linear, slope ~3.5e-5 [E2]
    # - A slow oscillation (period ~65) of amplitude ~0.008 rides on the trend [E2]
    # - Sharp negative dip centered near x~1, min ~-0.095 at x=1, width ~2.5 [E4]
    # - Dip is asymmetric: rises steeply on left (x=-1 -> 0.078), decays slowly
    #   to the right, reaching ~0 by x~22 [E4]
    # - Far from dip (x<-4), values are positive ~0.06-0.08 near 0 [E4]
    # - At large |x| values ~0.02-0.06 [E1,E2,E3]
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            # baseline: linear trend + slow oscillation
            y = 0.0455 + 3.5e-5 * x
            y += 0.008 * math.sin(2 * math.pi * x / 65.0 + 1.0)
            # sharp negative dip near x=1, asymmetric (steeper left, long right tail)
            if x < 1.0:
                w = 1.8
            else:
                w = 4.5
            y -= 0.095 * math.exp(-((x - 1.0) ** 2) / (2 * w ** 2))
            ys.append(y)
        except Exception:
            ys.append(None)
    return {"y": ys}

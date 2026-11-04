import math

def predict(probe):
    # Observations:
    # - For x in roughly [-3, 3], y is large (~10-13) and noisy [E2]
    # - Outside that band, y is small and roughly follows -log-ish / smooth decay [E1, E2]
    # - E1: x=-1.2 -> 11.57 (inside band); x=-12.9 -> 0.83; x=38.8 -> 1.29; x=73.9 -> -0.54
    # - E2: x=-8 -> 1.24, x=-6 -> -0.08, x=-4 -> 0.82, x=4 -> 0.09, x=6 -> -0.53, x=8 -> -0.73
    # - E2: x=12 -> -0.89, x=16 -> -0.93, x=24 -> 0.82, x=32 -> 0.18
    # Hypothesis: special interval roughly (-3.5, 3.5) where output ~ 11-13 (noisy).
    # Outside: smooth function, roughly -log(|x|)/something with sign flips; hard to pin down.
    # Best guess: piecewise. Inside band -> ~11.5. Outside -> -log(|x|+1)*sign-ish.
    # Since noise is large, aim for rough magnitude.

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            if -3.5 < x < 3.5:
                ys.append(11.5)
            else:
                # rough smooth decay; sign flips observed but weak signal
                v = -math.log(abs(x) + 1.0)
                ys.append(v)
        except Exception:
            ys.append(None)
    return {"y": ys}

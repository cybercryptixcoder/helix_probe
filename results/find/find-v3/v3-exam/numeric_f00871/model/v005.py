def predict(probe):
    # Central linear region: f(x) = 5.2 - 2.5*x on [-2.1, 2.1], else 0 [E4, E6, E8]
    #   left edge: f(-2.1)=10.45, f(-2.2)=0; right edge: f(2.1)=-0.05, f(2.2)=0
    # Second nonzero region: noisy/random values in roughly [-88, -78.5] [E9, E10, E12]
    #   E12: nonzero at -79.0..-85.5 and -87..-88, but 0 at -76.5,-77.0,-77.5
    #   E10: 0 at -75,-70,-60,-90,-100,-50,-40,-30,-20,-10
    #   So region is approx [-88, -78.5]; values look random in ~[-0.1, 0.3]
    #   Cannot predict exact value; use a fixed pseudo-random-ish value per x.
    #   Best guess: return a deterministic function of x that mimics the noise.
    import math
    out = []
    for x in probe["x"]:
        if -2.1 <= x <= 2.1:
            out.append(5.2 - 2.5 * x)
        elif -88.0 <= x <= -78.5:
            # noisy region; deterministic pseudo-random in [-0.1, 0.3]
            # use a hash-like function of x to approximate the noise
            h = math.sin(x * 12.9898) * 43758.5453
            frac = h - math.floor(h)
            out.append(-0.1 + 0.4 * frac)
        else:
            out.append(0.0)
    return {"y": out}

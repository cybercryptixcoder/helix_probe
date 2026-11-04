import math

def predict(probe):
    # A: large positive x -> ~0 (tiny negative) [E1, E3]
    # A: large negative x -> ~-0.0032 plateau [E1, E3]
    # A: sharp peak near x=0, peak ~0.39 at x=0, falls to ~0.12 at x=2, ~0.03 at x=3 [E2]
    # A: bump is asymmetric: left side steep (x=-1 -> 0.197, x=-2 -> 0.0575) [E2]
    # A: right tail decays smoothly (x=4->0.0099, 5->0.0012, 6->0.0001, 7->-0.001) [E2]
    # A: baseline negative offset ~-0.0032 for x<-20, ~0 for x>20 [E1,E3]
    # A: small positive bump near x=-4 (0.0053) and x=-15 (-0.0008) [E2] -- minor, ignore
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
            # Gaussian bump centered at 0, asymmetric widths
            if x >= 0:
                s = 1.6
            else:
                s = 1.1
            bump = 0.39 * math.exp(-(x / s) ** 2)
            # Baseline: sigmoid from -0.0032 (left) to ~0 (right)
            base = -0.0032 / (1.0 + math.exp(x / 15.0))
            ys.append(bump + base)
        except Exception:
            ys.append(None)
    return {"y": ys}

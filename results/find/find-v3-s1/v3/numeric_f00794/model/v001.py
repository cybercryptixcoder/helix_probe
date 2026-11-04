import math

def predict(probe):
    # Model hypothesis:
    # - f is mostly a small-amplitude oscillatory function of x [E1, E2]
    # - There is a special region near x=0 where f takes a huge value (475.5 at x=0) [E2]
    # - Outside that region, values are small (~[-1,1]) and look like a noisy sine [E1, E2]
    # - The spike is narrow: at x=±16 values are small, so region is roughly |x|<~8 (?) [E2]
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
            continue
        # Special region near 0: large spike. Model as a narrow Gaussian-like bump.
        # Only evidence is x=0 -> 475.5144. Assume width ~ a few units (?).
        spike = 475.5144 * math.exp(-(x * x) / (2.0 * 4.0 * 4.0))
        # Ordinary oscillatory part: small amplitude sine. Fit roughly from E2.
        # Values range about [-0.95, 0.9]; period looks ~ 60-70 units (?).
        osc = 0.5 * math.sin(2 * math.pi * x / 64.0)
        out.append(spike + osc)
    return {"y": out}

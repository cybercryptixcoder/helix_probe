import math

def predict(probe):
    # Model of the black box f(x).
    #
    # Evidence summary:
    # - Outputs are always small (roughly in [-0.3, 0.32]) and look noisy/irregular.
    # - Repeated calls on the same x (E10, E12) give DIFFERENT outputs:
    #     E10: x=0.0 twice -> -0.0137, 0.2402
    #          x=10.0 twice -> -0.0482, -0.0430
    #          x=37.0 twice -> 0.1344, -0.1682
    #          x=50.0 twice -> 0.0303, 0.0155
    #          x=75.0 twice -> -0.0873, -0.0212
    #          x=-8.0 twice -> -0.1938, -0.0201
    #          x=62.0 twice -> 0.0723, -0.0011
    #     E12: x=5.0 three times -> -0.0352, -0.0353, 0.1840
    #   => The box is STOCHASTIC. The "noise" is not a small perturbation
    #      around a smooth function; repeated identical inputs scatter widely.
    # - E12 with x=5.0 vs 5.001 vs 5.01 vs 5.1 ... shows no continuity:
    #   tiny changes in x give large, unrelated jumps. There is no smooth
    #   underlying curve visible in any experiment (E2, E4, E6, E8, E14, E16
    #   all look like independent random draws along x).
    # - No region behaves systematically differently: values around x=0
    #   (E2, E4, E14) are just as scattered as at |x|~100. The "interval"
    #   hint does not manifest as a visible deterministic regime in the data.
    # - The magnitude of outputs is consistently ~0.0-0.3 in absolute value,
    #   with no growth with |x| and no obvious dependence on x at all.
    #
    # Conclusion: the only mechanism consistent with every experiment is that
    # f(x) returns a random number drawn from a fixed distribution that is
    # (approximately) independent of x. The distribution appears roughly
    # symmetric about 0 with typical magnitude ~0.1 and range ~±0.32.
    #
    # Best guess for the distribution: something like a scaled sine of a
    # uniform random angle, or a uniform/normal-ish draw with std ~0.1.
    # I'll use a normal with mean 0 and std 0.1, clipped to about ±0.32,
    # which matches the observed spread and bounds.
    #
    # Because the box is stochastic, the best possible prediction for any
    # probe is a random draw from this distribution (per element of x).
    # Deterministic structure cannot be recovered from the evidence.

    xs = probe.get("x", [])
    out = []
    for _ in xs:
        # Draw from the inferred output distribution.
        # Mean 0, std ~0.1, clipped to observed range [-0.32, 0.32].
        v = random_gauss()
        v = max(-0.32, min(0.32, v))
        out.append(round(v, 4))
    return {"y": out}


def random_gauss():
    # Box-Muller, std = 0.1
    import math
    import random
    u1 = random.random()
    u2 = random.random()
    if u1 <= 0.0:
        u1 = 1e-12
    z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
    return 0.1 * z

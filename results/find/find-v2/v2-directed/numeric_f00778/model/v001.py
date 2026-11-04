import math

def predict(probe):
    # Model of the black box f(x).
    #
    # Observations:
    # - For |x| large (>= ~2), f(x) is dominated by a cubic-ish term: f(x) ~ c*x^3.
    #   E1: f(64) ≈ -1.023e6, f(-64) ≈ +1.021e6, f(128) ≈ -8.18e6, f(-100) ≈ 3.898e6.
    #   Ratio f(x)/x^3 roughly constant ~ -3.9 for large |x| (sign opposite to x).
    #   Check: 64^3=262144; -1023050/262144 ≈ -3.902. 128^3=2097152; -8181910/2097152 ≈ -3.901.
    #   -100^3=-1e6; 3897801/-1e6 ≈ -3.898. So cubic coefficient ≈ -3.9.
    # - For |x| small (< ~1.2), f(x) is small and noisy, oscillating around a few units.
    #   E3/E4 show values like 1.8-5.8 for |x|<1, with no clear cubic trend.
    #   There is a "noisy/oscillatory" central region roughly |x| < 1.2.
    # - Transition: at |x| ~ 1.25-1.5 the cubic term starts to dominate
    #   (E2: f(1.5)=-6.21, cubic -3.9*3.375≈-13.2; f(-1.5)=13.88 vs +13.2).
    #   So there's a smooth blend: central noisy region, then cubic outside.
    #
    # Best guess: f(x) = -3.9*x^3 + noise(x) in central region, with the cubic
    #   taking over for |x| beyond ~1.2. In the central region the "noise" is
    #   roughly a small offset of a few units, possibly random.
    #
    # We model: cubic term -3.9*x^3 everywhere, plus a central perturbation
    #   for |x| < 1.2 that we approximate as a small constant-ish offset
    #   (mean ~3.5 based on E3/E4 central values). Since it's noisy, use a
    #   deterministic approximation (can't reproduce noise).
    #
    # Refine cubic coefficient: use large points.
    #   -8181910.3578 / 128^3 = -3.9014
    #   -3901796.0117 / 100^3 = -3.9018
    #   3897801.3001 / (-100)^3 = -3.8978
    #   1021415.8598 / (-64)^3 = -3.8965  (since (-64)^3=-262144, 1021415/-262144=-3.896)
    #   Average ≈ -3.899. Use -3.9.

    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            if x is None:
                ys.append(None)
                continue
            x = float(x)
            base = -3.9 * x * x * x
            # Central region correction: for |x| < 1.2, add a small offset.
            # Observed central values (E3/E4) hover around 2-5, while cubic is tiny.
            # Use offset ~3.5, fading out near boundary.
            ax = abs(x)
            if ax < 1.2:
                # fade factor: 1 at center, 0 at 1.2
                w = 1.0 - (ax / 1.2) ** 2
                base += 3.5 * w
            ys.append(base)
        return {"y": ys}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}

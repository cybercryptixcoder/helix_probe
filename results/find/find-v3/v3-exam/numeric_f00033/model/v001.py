import math

def predict(probe):
    # Model: f(x) is a small MLP approximating a narrow bump centered near x≈0.
    # Evidence E1: outputs are tiny (~1e-4) for |x|>20, peak ~0.036 at x=2.9,
    # and ~0.0 at x=-6.0. So it's a localized peak around x≈0..3, near-zero elsewhere.
    # Shape looks like a Gaussian bump: f(x)=A*exp(-((x-mu)^2)/(2*s^2)).
    # Fit from E1: peak ~0.036 near x=2.9; at x=-6.0 it's ~0.0; at x=21.3 ~-0.0005.
    # Estimate mu≈2.9, A≈0.036. Width: at x=-6 (dist 8.9) value ~0 -> small sigma.
    # At x=21.3 (dist 18.4) ~-0.0005 (essentially 0). At x=-20.3 ~-0.0013.
    # Choose sigma ~3.5 so that at dist 8.9 -> exp(-8.9^2/(2*3.5^2))=exp(-3.23)=0.04 -> 0.0014.
    # Hmm observed at -6 is 0.0, so sigma smaller. Try sigma=3.0: dist8.9 -> exp(-4.4)=0.012 -> 0.0004.
    # At x=2.9 peak 0.036. At x=-6 (dist 8.9) ~0.0004 ~ 0.0. Good.
    # At x=21.3 (dist 18.4) exp(-18.8)=~0 -> -0.0005 (noise). Good.
    # At x=-20.3 (dist 23.2) ~0 -> -0.0013 (noise). Good.
    # At x=-24.3 (dist 27.2) ~0 -> -0.0016 (noise). Good.
    # At x=-50.4 (dist 53.3) ~0 -> -0.0032 (noise). Good.
    # At x=66,72.7,88.2 ~0 -> tiny negatives (noise). Good.
    # So: Gaussian bump, mu≈2.9, A≈0.036, sigma≈3.0. Outputs slightly negative far away (noise/offset).
    # Add small negative baseline ~ -0.0002? At x=88.2 -0.0002, x=66 -0.0003. Baseline ~ -0.0002.
    A = 0.036
    mu = 2.9
    sigma = 3.0
    base = -0.0002
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            v = A * math.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) + base
        except Exception:
            v = None
        ys.append(v)
    return {"y": ys}

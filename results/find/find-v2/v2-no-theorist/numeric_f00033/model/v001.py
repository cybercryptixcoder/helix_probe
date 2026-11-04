import math

def predict(probe):
    # Observations: outputs are tiny except near x=2.9 where y=0.0362.
    # Values look like a narrow bump centered near x~3, decaying fast away.
    # |x| large -> ~0. Peak at small x. Gaussian-like bump.
    # E1: x=2.9 -> 0.0362; x=-6 -> 0.0; x=21.3 -> -0.0005; x=-20.3 -> -0.0013
    # Bump centered near x~3, width small. Try Gaussian: A*exp(-((x-c)^2)/(2s^2))
    # Fit: at x=2.9, y=0.0362. At x=21.3, y=-0.0005 (negative, so maybe offset).
    # Small negative baseline ~ -0.0003 at large |x|.
    # Guess: A*exp(-((x-3)^2)/(2*s^2)) + b, with s ~ 3-4.
    # At x=-6: exp(-(81)/(2s^2)); if s=3, exp(-4.5)=0.011 -> too big.
    # s=2: exp(-81/8)=4e-5 -> ~0. Good.
    # At x=21.3: (18.3)^2/8=41.9 -> ~0. Good.
    # At x=-20.3: (23.3)^2/8=67.9 -> ~0. Good.
    # At x=2.9: exp(-0.01/8)~0.999 -> A~0.0362. Good.
    # Baseline b ~ -0.0003? But x=2.9 gives 0.0362 which is A+b.
    # x=-6 gives 0.0 exactly, so b~0. x=21.3 gives -0.0005, x=-20.3 -0.0013.
    # Slight negative tail. Use small negative baseline for |x|>10 maybe.
    # Keep simple: A*exp(-((x-3)^2)/8) - tiny.
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            y = 0.0362 * math.exp(-((x - 3.0) ** 2) / 8.0)
            # small negative baseline at large |x|
            if abs(x) > 10:
                y -= 0.0003
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}

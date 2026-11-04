import math

def predict(probe):
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            if x is None:
                ys.append(None)
                continue
            x = float(x)
            # Broad shallow U: min ~ -1.69 near x=0, rising to ~ -1.47 at |x|=128
            # Fit: at |x|=30, base ~ -1.63; at |x|=128, ~ -1.47/-1.51
            # Use quadratic: base = c0 + c2*x^2 with c0 ~ -1.695, c2 ~ 1.4e-5
            c0 = -1.695
            c2 = 1.4e-5
            base = c0 + c2 * x * x
            # small linear tilt: f(-128) ~ -1.47, f(128) ~ -1.51
            tilt = -1.56e-4 * x
            # Two narrow notches near x = ±0.8, depth ~0.12, width ~0.35
            notch = 0.0
            for center in (-0.8, 0.8):
                notch -= 0.12 * math.exp(-((x - center) ** 2) / (2 * 0.35 ** 2))
            # small central bump near x=0, height ~0.02
            bump = 0.02 * math.exp(-(x ** 2) / (2 * 0.25 ** 2))
            ys.append(base + tilt + notch + bump)
        return {"y": ys}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}

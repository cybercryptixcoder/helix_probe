import math

def predict(probe):
    try:
        xs = probe.get("x", [])
        out = []
        for x in xs:
            if x is None:
                out.append(None)
                continue
            # Linear trend across full range
            base = 4.69 * x + 6.0
            # Localized correction near zero: f(0)=3.92 vs base 6.0 => dip of ~2.08
            # Smooth transition rejoining line by |x|~2
            corr = -2.08 * math.exp(-(x / 1.2) ** 2)
            out.append(base + corr)
        return {"y": out}
    except Exception:
        return {"y": [None] * len(probe.get("x", []))}

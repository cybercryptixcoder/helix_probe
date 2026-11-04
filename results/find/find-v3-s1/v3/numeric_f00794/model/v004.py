import math

def predict(probe):
    # Beliefs:
    # - There is a special large value at x=0: f(0) ≈ 475.5144 [E2]
    # - Elsewhere f is bounded in roughly [-1, 1] [E1,E2,E3,E4,E5]
    # - The bounded part looks noisy/oscillatory; exact form unknown (?)
    # - Region of different behavior: a spike at/near 0 [E2]
    xs = probe.get("x", [])
    out = []
    for x in xs:
        try:
            xf = float(x)
        except Exception:
            out.append(None)
            continue
        if abs(xf) < 1e-9:
            out.append(475.5144)
        else:
            # placeholder bounded oscillation (?)
            out.append(math.sin(xf) * math.cos(xf * 0.5))
    return {"y": out}

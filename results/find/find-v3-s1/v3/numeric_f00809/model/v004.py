import math

def predict(probe):
    # Observations summary:
    # - For x < ~-75: y ≈ -0.6/x (tiny positive tail) [E1,E3,E4,E5]
    # - Elsewhere: noisy oscillation, amplitude ~0.1-0.4, irregular [E2,E4,E5,E6]
    # - No clean single-frequency sinusoid fits [E2,E6]
    # - Values look pseudo-random in [-0.4, 0.4] with occasional larger spikes [E6]
    # Best guess: deterministic pseudo-random function of x (hash-like), plus tail rule.
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            if x < -75:
                ys.append(-0.6 / x)
            else:
                # Hash-like pseudo-random in [-0.4, 0.4]
                h = math.sin(x * 12.9898 + 78.233) * 43758.5453
                frac = h - math.floor(h)
                ys.append((frac - 0.5) * 0.8)
        except Exception:
            ys.append(None)
    return {"y": ys}

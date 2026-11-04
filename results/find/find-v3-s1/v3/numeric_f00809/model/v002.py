import math

def predict(probe):
    # Outputs are small, roughly [-0.13, 0.19], noisy-looking [E1, E2]
    # No clean period found in E2 sign pattern; treat as low-amplitude oscillation [E2]
    # Best guess: small sinusoid around a small positive mean; uncertain (?)
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            ys.append(0.02 + 0.09 * math.sin(x / 2.5))
        except Exception:
            ys.append(None)
    return {"y": ys}

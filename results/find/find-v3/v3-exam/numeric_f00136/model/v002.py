import math

def predict(probe):
    # Beliefs (revised from evidence):
    # - f is a smooth, slowly-varying function of x over [-128,128] [E2]
    # - Global trend: y rises roughly linearly with x, from ~0.048 at -128
    #   to ~0.057 at 128, i.e. slope ~ 3.5e-5 per unit x [E2]
    # - Superimposed small oscillation (period ~ 60-70) of amplitude ~0.01 [E2]
    # - Near x=0 there is a sharp negative dip: f(0)~-0.001, f(1.2)~-0.0895,
    #   f(2.9)~-0.0469, f(10)~-0.0249, f(-6)~0.0471 -> a narrow negative
    #   feature centered near x~1, width ~5, depth ~0.09 [E1,E2,E3]
    # - Elsewhere values are ~0.02-0.05, positive [E1,E2,E3]
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            # linear trend
            y = 0.0455 + 3.5e-5 * x
            # gentle oscillation
            y += 0.008 * math.sin(2 * math.pi * x / 65.0 + 1.0)
            # narrow negative dip near x ~ 1
            y -= 0.085 * math.exp(-((x - 1.0) ** 2) / (2 * 4.0 ** 2))
            ys.append(y)
        except Exception:
            ys.append(None)
    return {"y": ys}

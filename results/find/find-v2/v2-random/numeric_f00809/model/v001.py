import math

def predict(probe):
    # Beliefs:
    # 1. Output is a smooth, roughly sinusoidal-looking function of x, amplitude ~0.1-0.17 [E1, E2]
    # 2. There is a discontinuity / different regime somewhere: values near x~65-73 give tiny outputs
    #    (0.0078 at 66, 0.0014 at 65.5, -0.0101 at 79.4, -0.0618 at 72.7) while neighbors are larger [E1,E2]
    # 3. Looking at sign/period: E1 has + at 88.2, 66, 2.9, -24.3, -6, 21.3; - at -20.3,-61.7,-50.4,72.7
    #    E2 has - at 104.5, 1.2, 30.3, -63.9, 104.9, 123.6, 79.4; + at -55.8, 65.5, 103.0
    # 4. A period near ~60-70 in x fits many sign changes; amplitude ~0.1.
    # 5. There is likely a "gap"/special interval where the function is damped or shifted.
    #    The small values cluster around x in [65, 80] and near 104-105 (0.0588, -0.0955, 0.0617 vary).
    # 6. Best simple mechanism: y = A*sin(k*x + phi) with a damping window.
    #    Use k ~ 2*pi/63, A ~ 0.1, plus a localized attenuation centered ~72 width ~10.
    # 7. Also a second attenuation near 104? E2 shows 104.5=-0.0955, 104.9=0.0588, 103.0=0.0617 -> jumpy,
    #    suggests a narrow feature there too. Mark as uncertain (?).

    x = probe.get("x", [])
    ys = []
    for xi in x:
        try:
            xi = float(xi)
        except Exception:
            ys.append(None)
            continue
        # base sinusoid
        k = 2.0 * math.pi / 63.0
        # phase chosen to roughly match signs (fit by eye)
        phi = 0.6
        base = 0.11 * math.sin(k * xi + phi)
        # slow amplitude modulation (envelope) to match varying amplitudes
        env = 0.85 + 0.35 * math.sin(2.0 * math.pi * xi / 210.0 + 1.0)
        val = base * env
        # damping window around 72 (?) — outputs tiny there
        d1 = math.exp(-((xi - 72.0) ** 2) / (2.0 * 9.0 ** 2))
        val *= (1.0 - 0.85 * d1)
        # narrow dip near 104 (?)
        d2 = math.exp(-((xi - 104.0) ** 2) / (2.0 * 1.5 ** 2))
        val *= (1.0 - 0.5 * d2)
        # clamp to plausible range
        if val > 0.2:
            val = 0.2
        if val < -0.2:
            val = -0.2
        ys.append(round(val, 4))
    return {"y": ys}

import math

def predict(probe):
    # Model hypothesis (v2):
    # - For |x| >= ~1.5: f(x) is a small bounded oscillatory function, roughly in [-1, 1] [E1, E2, E3]
    # - There is a special interval near 0 where f is much larger (~6 to ~14) [E4]
    # - At x = 0 exactly: huge spike ~475.25 [E2]
    # - The large-interval appears to span roughly |x| <= ~0.5 (values 6.06, 7.02, 7.57, 13.39, 12.64, 13.83) [E4]
    # - Outside that, values return to small oscillation (e.g. x=1.0 -> -0.378, x=1.5 -> 0.866) [E4]
    # - The small oscillation is not a clean sinusoid; we approximate with a sinusoid as best guess [?]
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            ax = abs(x)
            if ax < 1e-9:
                ys.append(475.2497)
            elif ax <= 0.5:
                # Large interval near zero: values ~6-14, asymmetric, noisy
                # Rough guess: bigger for positive x, grows toward 0.5 then drops
                # Use a simple approximation centered around ~10
                if x > 0:
                    val = 10.0 + 4.0 * math.sin(math.pi * x)  # ? rough
                else:
                    val = 7.5 + 1.5 * math.sin(math.pi * x)   # ? rough
                ys.append(val)
            else:
                # Small oscillatory baseline outside the special interval
                val = 0.7 * math.sin(2 * math.pi * x / 100.0 + 0.5)
                ys.append(val)
        except Exception:
            ys.append(None)
    return {"y": ys}

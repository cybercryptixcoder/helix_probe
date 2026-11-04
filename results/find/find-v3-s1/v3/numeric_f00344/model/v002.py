import math

def predict(probe):
    # Observations:
    # - For |x| >= ~100 the output saturates near -24973124.7 (a clamp/floor) [E1,E2,E3]
    # - f(0) = 472.73, a nonzero spike at exactly zero [E2,E4]
    # - For small |x| (0<|x|<~1) output is small negative, smooth: f(-1)=-7.4, f(1)=-41.7 [E4]
    # - Sign matters: for |x|>~1, negative x gives smaller magnitude than positive x [E2,E4]
    #   e.g. f(2.5)=-128.9 vs f(-2.5)=-2.075 ; f(4)=-528 vs f(-4)=-106.1
    # - Magnitude grows fast (cubic-ish) with |x| [E2,E3]
    # - There is a floor clamp at -24973124.7 for large |x| [E1,E2,E3]
    FLOOR = -24973124.7
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
            continue
        try:
            if x == 0:
                out.append(472.73)
                continue
            ax = abs(x)
            # cubic-ish growth; sign asymmetry: negative x smaller magnitude
            if x > 0:
                v = -0.6 * (ax ** 3)
            else:
                v = -0.35 * (ax ** 3)
            if v < FLOOR:
                v = FLOOR
            out.append(v)
        except Exception:
            out.append(None)
    return {"y": out}

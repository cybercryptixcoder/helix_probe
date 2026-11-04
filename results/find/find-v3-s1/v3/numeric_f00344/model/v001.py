import math

def predict(probe):
    # Observations:
    # - For |x| >= ~100 the output saturates near -24973124.7 (a clamp/floor) [E1,E2,E3]
    #   e.g. x=-104,-120.7,-127.5,-120.2 all give ~ -24973124.5..7
    # - For small |x| output is small and negative-ish, roughly cubic-ish but not clean [E2]
    # - Sign matters: x=3 -> -211.7, x=-3 -> -15.0 ; x=10 -> -14962.8, x=-10 -> -8905.7 [E2]
    # - Mid-range grows fast negative, magnitude ~ |x|^3-ish scaled [E2,E3]
    # Model: y = -k * x^3 * (sign-dependent factor) with a floor clamp at -24973124.7
    # "?" uncertain: exact coefficient and sign asymmetry.
    FLOOR = -24973124.7
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
            continue
        try:
            ax = abs(x)
            # base cubic term
            v = -0.6 * (ax ** 3)
            # sign asymmetry: negative x gives smaller magnitude for small |x|, larger for mid
            if x < 0:
                v = -0.35 * (ax ** 3)
            # clamp
            if v < FLOOR:
                v = FLOOR
            out.append(v)
        except Exception:
            out.append(None)
    return {"y": out}

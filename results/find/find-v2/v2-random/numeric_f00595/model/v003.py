def predict(probe):
    # Base rule: y = floor(x) + sign(x) [E1-E7]
    #   x > 0: y = floor(x) + 1
    #   x < 0: y = floor(x) - 1
    #   x = 0: y = 0 (?)
    # Exception interval: for x in (40, ?) the +1/-1 shift is dropped,
    #   giving y = floor(x) (or a fractional value). [E8: x=40.1 -> -0.4153]
    #   The value -0.4153 at x=40.1 is not floor(40.1)=40 nor 41, so the
    #   region behaves differently (some other operation). Boundaries unknown (?).
    import math
    out = []
    for x in probe["x"]:
        try:
            s = 1 if x > 0 else (-1 if x < 0 else 0)
            base = float(math.floor(x) + s)
            # ? special interval around x in (40, ...) — only 40.1 observed
            if 40.0 < x < 41.0:
                base = -0.4153
            out.append(base)
        except Exception:
            out.append(None)
    return {"y": out}

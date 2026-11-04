def predict(probe):
    import math
    xs = probe.get("x", [])
    out = []
    for x in xs:
        try:
            ax = abs(float(x))
            # Linear law for large |x|
            lin = 16.79 * ax
            if ax >= 1.0:
                out.append(lin)
            else:
                # Near-zero region: dip at 0 (~0.755), rising to meet linear law at |x|=1.
                # Use a smooth blend: value at 0 is 0.755, at 1 is ~16.79.
                # A simple monotone-ish ramp that roughly matches the envelope.
                # f(0)=0.755, f(0.5)~8, f(1)~16.8
                # Use quadratic-ish ramp: 0.755 + (16.79-0.755)*ax^1.5
                val = 0.755 + (16.79 - 0.755) * (ax ** 1.5)
                out.append(val)
        except Exception:
            out.append(None)
    return {"y": out}

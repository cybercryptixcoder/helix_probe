import math

def predict(probe):
    try:
        xs = probe.get("x", [])
        out = []
        for x in xs:
            try:
                out.append(_f(float(x)))
            except Exception:
                out.append(None)
        return {"y": out}
    except Exception:
        return {"y": []}

def _f(x):
    # Isolated spike at exactly 0
    if x == 0.0:
        return 472.73

    ax = abs(x)

    # Small-|x| region (excluding the spike): smooth, negative, slowly varying.
    # Observed: (-1,-7.4),(-0.5,-10.375),(-0.1,-11.5281),(-0.05,-11.6174),(-0.01,-11.6839)
    #           (0.01,-36.8159),(0.05,-36.8781),(0.1,-36.9541),(0.5,-37.825),(1,-41.7)
    if ax < 1.0:
        if x < 0:
            # approaches ~ -11.7 as x->0-, ~ -7.4 at x=-1
            # linear-ish in x between -1 and 0
            return -11.7 + (-7.4 - (-11.7)) * (x + 1.0) / 1.0 if False else (-11.7 + (11.7 - 7.4) * x)
        else:
            # approaches ~ -36.8 as x->0+, ~ -41.7 at x=1
            return -36.8 + (-41.7 - (-36.8)) * x

    if x > 0:
        # positive side: |y| ~ 2.54 * x^3.85
        val = 2.54 * (ax ** 3.85)
        return -val
    else:
        # negative side
        if ax >= 64:
            # saturate near -2.5e7
            return -24973124.5656
        else:
            val = 0.248 * (ax ** 4.37)
            return -val

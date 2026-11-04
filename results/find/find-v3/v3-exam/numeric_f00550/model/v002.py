import math

def predict(probe):
    # f(x) = 0 for |x| >= 1 [E1, E2]
    # f(x) != 0 only for |x| < 1 (roughly), with values that vary [E2]
    # Observed nonzero values for |x|<1:
    #   x=0.1  -> -1.553
    #   x=0.5  -> -1.625
    #   x=-0.1 -> -1.913
    #   x=0.0  -> -1.7
    #   x=0.25 -> -1.4562
    #   x=-0.25-> -2.3563
    # These look like some function of x in (-1,1); unclear exact form.
    # Best guess: a smooth-ish function; use a simple interpolation/approx.
    # Since exact form unknown, approximate with a quadratic fit through
    # the observed points as a placeholder.  Marked "?".
    out = []
    for x in probe["x"]:
        if abs(x) >= 1.0:
            out.append(-0.0)
        else:
            # quadratic fit guess (?) through observed points
            # Fit: y = a*x^2 + b*x + c using the 6 points
            # Quick least-squares-ish: use c ~ -1.7, b ~ 1.0, a ~ -1.0 (rough)
            # Better: use numpy-free manual fit
            out.append(-1.7 + 1.0*x - 1.0*x*x)
    return {"y": out}

import math

def predict(probe):
    # Model v4
    # Beliefs:
    # - f(0) = 472.73 (spike at exactly zero) [E2,E4]
    # - Positive side, small x (0<x<~1.5): f(x) ≈ c + a*x^3 with c≈-36.8, a≈-5 [E18,E20]
    # - Positive side, x>=1.5: power law -A*x^p. Fit from E20/E22:
    #   f(1.5)=-53.375, f(4)=-528, f(5.5)=-1615.575, f(10)=-14962.8, f(20)=-215708.8
    #   log-log slope: ln(215708.8/14962.8)/ln(2)=3.85; ln(14962.8/528)/ln(2.5)=3.83
    #   So p≈3.85, A = 14962.8/10^3.85 ≈ 0.2114
    # - Negative side, small |x| (0<|x|<~2): smooth curve, min near x=-2.2 (f=+0.0093)
    #   f(-0.05)=-11.62, f(-1)=-7.4, f(-2)=-0.1, f(-2.2)=+0.0093 [E16]
    # - Negative side, |x|>=~2.5: power law -A*|x|^p. From E10:
    #   f(-30)=-890153.7, f(-60)=-14900675.7 -> p=4.065, A=890153.7/30^4.065
    # - Floor clamp at FLOOR=-24973124.7 for very large |x| [E2,E9,E11,E15,E17,E19,E23]
    #   But E11/E15/E17/E19/E23 show values BELOW floor (e.g. -286634980.6 at x=123.7),
    #   so floor is NOT a hard clamp — it's a smooth transition. Actually values like
    #   -24973124.34, -24973124.47, -24973124.58, -24973124.67, -24973124.71 appear
    #   at |x|~119-127 — these look like the power law reaching ~-2.5e7 around |x|~120.
    #   Wait: f(-120.4)=-24973124.5884, f(-116.9)=-24973124.4736, f(-119.2)=-24973124.3449,
    #   f(-120.8)=-24973124.7157, f(-126.5)=-24973124.6704, f(-113.6)=-24973124.45.
    #   These are all ≈ -24973124.5 with tiny variation — that IS a clamp/plateau.
    #   But f(123.7)=-286634980.6 and f(115.8)=-220428796.3 are far below.
    #   So: NEGATIVE side clamps at floor; POSITIVE side does not (keeps growing).
    #   Check: f(-120.4)=-24973124.59 (clamped), f(123.7)=-286634980.6 (not clamped).
    #   Yes! Floor applies only to x<0.
    # - Positive side power law: f(92.2)=-89061002.75, f(117)=-229659208.1
    #   ratio 2.578 over 117/92.2=1.269 -> p=ln(2.578)/ln(1.269)=3.85. Consistent.
    #   f(123.7)=-286634980.6: check 229659208*(123.7/117)^3.85=229659208*1.24=2.85e8 ✓

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
            if x > 0:
                if x < 1.5:
                    v = -36.8 - 5.0 * (x ** 3)
                else:
                    p = 3.85
                    A = 14962.8 / (10.0 ** p)
                    v = -A * (x ** p)
            else:
                ax = -x
                if ax < 2.0:
                    # quadratic through (-0.05,-11.6174),(-1,-7.4),(-2,-0.1)
                    v = -11.766 - 2.899 * x + 1.4670 * (x * x)
                else:
                    p = 4.065
                    A = 890153.7 / (30.0 ** p)
                    v = -A * (ax ** p)
                    if v < FLOOR:
                        v = FLOOR
            out.append(v)
        except Exception:
            out.append(None)
    return {"y": out}

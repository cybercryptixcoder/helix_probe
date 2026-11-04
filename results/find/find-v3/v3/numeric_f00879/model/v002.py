import math

def predict(probe):
    # Beliefs (revised):
    # - f is NOT a simple global sinusoid; the "oscillation" is confined to a
    #   narrow band around 0 and is much faster than v1 thought [E6, E8].
    # - Outside roughly |x|>3 the function is slowly varying / near-linear-ish
    #   with small wiggles; values stay within ~[-3, 3] [E2, E4, E5, E7].
    # - Inside |x|<=~3 there is a rapid, high-frequency oscillation with
    #   period ~0.5 (values change sign every ~0.25) [E6, E8].
    # - There is a slow linear/offset trend plus small noise [E2, E4].
    # - The rapid band's amplitude is larger than the outer region's [E6, E8].
    # We model: y = slow(x) + band(x)*fast_osc(x) + noise
    #   slow(x) = a*x + b   (gentle trend)
    #   fast_osc(x) = sin(w*x + p) with w ~ 2*pi/0.5 = 4*pi
    #   band(x) = amplitude envelope, large for |x|<3, small outside.
    # Fit slow trend from outer points, then fit fast osc inside band.

    xs = probe["x"]
    out = []
    for x in xs:
        # slow trend: from E2/E4 outer points, y drifts slowly upward with x
        # e.g. x=-100 -> -0.3, x=0 -> ~0.5, x=100 -> ~0.9. Slope ~0.006.
        slow = 0.006 * x + 0.4

        # fast oscillation inside |x| < 3.2, period ~0.5
        if abs(x) < 3.2:
            # amplitude ~1.5 inside band (E6/E8 range roughly -1.3..3.5)
            amp = 1.4
            # phase: from E8, at x=0 y~0.23 (near slow), at x=0.25 y~1.87
            # sin(4*pi*0.25 + p)=sin(pi+p)=-sin(p) -> want positive, so p<0
            # at x=-0.25 y~2.79, sin(-pi+p)=-sin(p) also positive -> consistent
            # at x=0.5 y~3.52, sin(2pi+p)=sin(p) positive -> p>0. Contradiction
            # with above; so period may be ~0.5 but phase drifts. Use best guess.
            w = 4.0 * math.pi
            p = 0.3
            fast = amp * math.sin(w * x + p)
            # taper amplitude near band edge
            taper = max(0.0, 1.0 - (abs(x) / 3.2) ** 4)
            out.append(slow + fast * taper)
        else:
            # outer region: small residual wiggle
            out.append(slow + 0.15 * math.sin(0.5 * x))
    return {"y": out}

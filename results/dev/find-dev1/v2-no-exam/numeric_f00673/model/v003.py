import math

def predict(probe):
    # f(x) = 16.8*|x| + residual r(x) [E1, E2, E4, E6, E7]
    # r(x) is a fast oscillation in x near origin, slow far away [E11-E17]
    # Residual near origin has high-frequency component, period ~0.3-0.6 [E15, E16]
    # At moderate |x| (2-10) residual is slow sinusoid, period ~2 in x [E11, E13]
    # At large |x| residual amplitude grows ~sqrt(|x|) [E6, E7]
    # Residual is NOT symmetric: depends on sign of x [E5, E8, E9, E10]
    # Near origin there's a sharp asymmetry/jump at 0 [E16]
    # Model: base + amplitude(|x|)*sin(w(|x|)*x + phase(sign))
    # where w decreases with |x| (chirp) [E13, E17]
    out = []
    for x in probe.get("x", []):
        try:
            ax = abs(x)
            base = 16.8 * ax
            # amplitude grows slowly with |x|
            amp = 0.5 + 0.35 * math.sqrt(ax)
            # frequency: high near origin, low far away (chirp)
            # near origin w ~ 2*pi/0.4 ~ 15; far away w ~ 2*pi/2 ~ 3
            w = 3.0 + 12.0 / (1.0 + ax)
            # phase differs by sign (asymmetry)
            phi = 0.5 if x >= 0 else 2.5
            r = amp * math.sin(w * x + phi)
            out.append(base + r)
        except Exception:
            out.append(None)
    return {"y": out}

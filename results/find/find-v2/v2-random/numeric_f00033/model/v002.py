import math

def predict(probe):
    # Beliefs:
    # - There is a sharp positive spike very near x≈0: f(1.2)=0.228, f(2.9)=0.0362 [E1,E2]
    #   The spike is narrow (width ~1-2) and tall; at x=2.9 already down to 0.036 [E1,E2]
    # - Outside the spike, outputs are small negative, magnitude ~1e-4 to 4e-3 [E1,E2,E3]
    # - Negative magnitude is NOT monotone in |x|: |x|~48-50 -> ~3.2e-3, |x|~102 -> 4e-3,
    #   but |x|~58-66 -> ~3-4e-4, |x|~16-30 -> ~4e-4 to 1e-3 [E1,E2,E3]
    #   So there's a broad negative lobe peaking around |x|~50 and another near |x|~100 [E1,E3]
    # - Sign: positive only in the narrow spike near 0; negative elsewhere [E1,E2,E3]
    out = []
    for x in probe["x"]:
        try:
            ax = abs(x)
            # narrow tall positive spike near 0 (width ~1.5)
            spike = 0.228 * math.exp(-(x*x)/(2*1.5*1.5))
            # broad negative lobe peaking near |x|~50
            lobe1 = 0.0032 * math.exp(-((ax-50.0)**2)/(2*18.0*18.0))
            # second negative lobe near |x|~100
            lobe2 = 0.0040 * math.exp(-((ax-100.0)**2)/(2*15.0*15.0))
            # small baseline negative
            base = 0.0004
            y = spike - lobe1 - lobe2 - base
            out.append(round(y, 4))
        except Exception:
            out.append(None)
    return {"y": out}

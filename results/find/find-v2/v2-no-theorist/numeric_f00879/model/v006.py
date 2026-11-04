import math

def predict(probe):
    # Beliefs:
    # - Output is dominated by a sign step: x<0 -> ~-1.4, x>0 -> ~+1.2 [E2,E5,E7,E10].
    # - Large |x| saturates toward -1.5 / +1.3 [E9,E10,E11].
    # - BUT there is a strong deterministic oscillatory component on top of the step:
    #   within a fixed-sign region y varies widely (e.g. +0.1 to +3.6 for x>0) [E6,E8,E12,E14,E16,E18].
    # - The oscillation is NOT period 1 in x (x and x+1 differ) [E14,E18].
    # - Dense sweep E16 (x=20..21.9) shows oscillation with period ~0.5-1 in x,
    #   amplitude ~1, so a sin/cos of x (or small multiple) is plausible [E16].
    # - Negative side also oscillates (E14: -10..-14 all negative but varying) [E14].
    # ? Best guess: y = sign_step(x) + A*sin(w*x + phi) + noise, with w ~ 1-2.
    #   Fit roughly: positive mean ~1.2, negative mean ~-1.4, amplitude ~1.
    out = []
    for x in probe.get("x", []):
        try:
            step = 1.2 if x >= 0 else -1.4
            osc = 1.0 * math.sin(1.5 * x)
            v = step + osc
            out.append(round(v, 4))
        except Exception:
            out.append(None)
    return {"y": out}

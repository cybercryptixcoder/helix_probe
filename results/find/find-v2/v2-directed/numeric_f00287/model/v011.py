import math

def predict(probe):
    # Left region: y = -0.7*floor(x) for x <= -5.1 [E1,E2,E4,E7,E9,E10,E13,E16]
    #   E16/E22: -5.1001 -> 4.2 (const), -5.0999 -> -402.3 (const). Boundary at -5.1.
    # Middle region: y = -402.3 + small noise, for -5.1 < x < 18.52 [E1..E8,E10,E12,E14,E15,E17,E19,E20,E21,E22,E23]
    #   E23: 18.517 -> -402.2994 (middle), 18.5202 -> -302.4 (right). Boundary in (18.517,18.5202].
    #   E20: 18.519 -> -302.4, 18.518 -> -302.4, 18.51 -> -402.3651. Boundary in (18.51,18.518].
    #   E18: 18.5199999 -> -302.4, 18.5195 -> -302.4, 18.5205 -> -302.4, 18.499 -> -402.3.
    #   E8: 18.515 -> -402.39, 18.518 -> -302.4. So boundary in (18.515,18.518].
    #   E6: 18.515 -> -402.3, 18.52 -> -302.4. Boundary in (18.515,18.52].
    #   Best estimate: boundary at 18.517 (E23: 18.517 middle, 18.518 right).
    # Right region: y = -16.8*floor(x) for x >= 18.517 [E1,E3,E4,E5,E6,E8,E11,E13,E14,E19]
    #   E19: 127.99 -> -2133.6 (floor=127), 128.0 -> -2150.4 (floor=128). Consistent.
    out = []
    for x in probe.get("x", []):
        try:
            if x <= -5.1:
                out.append(-0.7 * math.floor(x))
            elif x < 18.517:
                out.append(-402.3)
            else:
                out.append(-16.8 * math.floor(x))
        except Exception:
            out.append(None)
    return {"y": out}

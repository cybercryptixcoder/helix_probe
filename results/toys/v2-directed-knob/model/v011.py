import math

def predict(probe):
    # Beliefs (mechanism), each line cites evidence:
    # - switch has no effect on x,y,size [E1 vs E4]
    # - x depends only on a and b; c only affects y and size [E1,E2,E3]
    # - x = min(10, 10 - b + 2*(a-5)); no lower clamp [E1,E3,E5,E7,E8,E9,E10,E11,E12,E13,E14,E15,E16,E17]
    # - y = c + max(0, a-7): a=8->+1 [E5,E6,E7,E10], a=9->+2 [E17], a<=7->+0 [E1,E2,E3,E8,E9,E11,E13,E14,E16]
    #   (E17 y=6 at c=5,a=9 rules out spike-at-8 and step-at-8; a linear ramp max(0,a-7) fits)
    # - size = 1 + 0.5*|a - c| [E1,E2,E3,E5,E6,E7,E8,E9,E10,E11,E12,E13,E14,E15,E16,E17]

    a = float(probe.get("a", 5))
    b = float(probe.get("b", 5))
    c = float(probe.get("c", 5))

    x = 10 - b + 2 * (a - 5)
    if x > 10:
        x = 10.0

    y = c + max(0.0, a - 7.0)

    size = 1.0 + 0.5 * abs(a - c)

    return {"x": round(x, 2), "y": round(y, 2), "size": round(size, 2)}

import math

def predict(probe):
    # Beliefs (mechanism), each line cites evidence:
    # - switch has no effect on x,y,size [E1 vs E4]
    # - x depends only on a and b; c only affects y and size [E1,E2,E3]
    # - x = min(10, 10 - b + 2*(a-5)); no lower clamp [E1,E3,E5,E7,E8,E9,E10,E11,E12,E13,E14,E15,E16,E17,E18]
    # - y = c + max(0, a-7) for a<=8; saturates at +1 for a>=8 [E5,E6,E7,E10,E17,E18]
    #   a=8->+1 [E5], a=9->+1 [E17], a=10->+1 [E18]; a<=7->+0 [E1,E2,E3,E8,E9,E11,E13,E14,E16]
    # - size = 1 + 0.5*|a - c| [E1,E2,E3,E5,E6,E7,E8,E9,E10,E11,E12,E13,E14,E15,E16,E17,E18]

    a = float(probe.get("a", 5))
    b = float(probe.get("b", 5))
    c = float(probe.get("c", 5))

    x = 10 - b + 2 * (a - 5)
    if x > 10:
        x = 10.0

    # y offset from a: rises from a=7 to a=8, then saturates at +1
    y_offset = min(1.0, max(0.0, a - 7.0))
    y = c + y_offset

    size = 1.0 + 0.5 * abs(a - c)

    return {"x": round(x, 2), "y": round(y, 2), "size": round(size, 2)}

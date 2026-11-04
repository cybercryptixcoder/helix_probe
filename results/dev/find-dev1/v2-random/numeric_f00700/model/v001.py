def predict(probe):
    # f(x) = floor(x) + 1 for all x [E1: 88.2->90? no]
    # Recheck: 88.2 floor+1 = 89, observed 90. So f(x)=floor(x)+2? 88.2->90 yes; 66.0->68 no (obs 67).
    # Pattern: output = ceil(x)+1 when x integer? 66->67 yes; 88.2 ceil+1=90 yes; -20.3 ceil+1=-20 no (obs -21).
    # Try: output = round(x)+1? 88.2->89 no.
    # Actual: 88.2->90 (+1.8), 66->67 (+1), -20.3->-21 (-0.7), -61.7->-62 (-0.3),
    # 2.9->4 (+1.1), -24.3->-25 (-0.7), 72.7->74 (+1.3), -50.4->-51 (-0.6), -6->-7 (-1), 21.3->23 (+1.7).
    # Looks like: positive -> ceil(x)+1, negative -> floor(x)-1, zero? 
    # 88.2 ceil+1=90 ✓; 66 ceil+1=67 ✓; 2.9 ceil+1=4 ✓; 72.7 ceil+1=74 ✓; 21.3 ceil+1=23 ✓
    # -20.3 floor-1=-22 ✗ (obs -21). Try trunc toward zero then step away: -20.3 -> -21 = floor ✓
    # -61.7 floor=-62 ✓; -24.3 floor=-25 ✓; -50.4 floor=-51 ✓; -6 floor=-7 ✓
    # So: x>=0 -> ceil(x)+1 ; x<0 -> floor(x). Check x=0? unknown.
    import math
    out = []
    for x in probe["x"]:
        try:
            if x >= 0:
                out.append(float(math.ceil(x) + 1))
            else:
                out.append(float(math.floor(x)))
        except Exception:
            out.append(None)
    return {"y": out}

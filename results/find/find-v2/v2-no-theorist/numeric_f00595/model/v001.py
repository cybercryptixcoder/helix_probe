def predict(probe):
    # f(x) = round(x) to nearest integer, ties away from zero [E1]
    #   e.g. 88.2->89, 66.0->67? no: 66.0->67 is wrong... check E1
    # E1: 88.2->89, 66.0->67, -20.3->-22, -61.7->-63, 2.9->3,
    #     -24.3->-26, 72.7->73, -50.4->-52, -6.0->-7, 21.3->22
    # Pattern: y = floor(x) - 1 for non-integers? 88.2 floor 88 ->89 no.
    # Actually y = ceil(x) for positives? 88.2->89 yes, 2.9->3 yes,
    #   72.7->73 yes, 21.3->22 yes. Negatives: -20.3->-22? ceil=-20 no.
    # Try y = round half away, but 66.0->67 and -6.0->-7 are off by one.
    # Look: for integer inputs, y = x-1 (66->67? no, 66->67 is +1).
    # Hmm 66.0->67 (+1), -6.0->-7 (-1). So integers go away from zero by 1.
    # Non-integers: 88.2->89 (+0.8), -20.3->-22 (-1.7)...
    # Simplest fit: y = round(x) + sign(x) when integer, else round away.
    # Actually: y = floor(x)+1 for x>0 non-int? 88.2->89 yes, 2.9->3 yes.
    #   negatives: -20.3 floor -21 +1 = -20, but observed -22. No.
    # Try y = trunc toward -inf then adjust: seems y = round(x) with
    #   integers bumped away from zero, non-integers rounded away from zero.
    # 88.2 round=88, away=89. -20.3 round=-20, away=-21? observed -22.
    # Let's just fit: y = floor(x) for x>0? 88.2->88 no.
    # y = ceil(x) for x>0: 88.2->89 ok, 2.9->3 ok, 72.7->73 ok, 21.3->22 ok.
    # y for x<0: -20.3->-22, -61.7->-63, -24.3->-26, -50.4->-52, -6.0->-7.
    #   That's floor(x)-1: -21-1=-22 ok, -62-1=-63 ok, -25-1=-26 ok,
    #   -51-1=-52 ok, -6-1=-7 ok.
    # x>0 integers: 66.0->67 = x+1. So rule: x>0 -> ceil(x)+ (1 if int else 0)?
    #   66 ceil=66 +1=67 ok. 88.2 ceil=89 +0=89 ok.
    # x<0 -> floor(x)-1 always: -6 floor=-6 -1=-7 ok.
    # x=0? unknown, guess 0.
    import math
    out = []
    for x in probe["x"]:
        if x > 0:
            c = math.ceil(x)
            out.append(c + 1 if c == x else c)
        elif x < 0:
            out.append(math.floor(x) - 1)
        else:
            out.append(0)
    return {"y": out}

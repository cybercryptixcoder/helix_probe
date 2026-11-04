import math

def predict(probe):
    # The box rounds each input to the nearest integer [E1: 88.2->90? no...]
    # Check E1: 88.2->90, 66.0->67, -20.3->-21, -61.7->-62, 2.9->4,
    # -24.3->-25, 72.7->74, -50.4->-51, -6.0->-7, 21.3->23
    # Differences: +1.8, +1, -0.7, -0.3, +1.1, -0.7, +1.3, -0.6, -1, +1.7
    # Not simple rounding. Looks like ceil? ceil(88.2)=89 no.
    # Try round(x)+1? round(88.2)=88 ->89 no.
    # Try floor(x)+1: floor(88.2)=88->89 no.
    # Try ceil(x)+1: 89+1=90 yes! ceil(66)=66+1=67 yes! ceil(-20.3)=-20+1=-19 no.
    # Hmm -20.3->-21. floor(-20.3)=-21 yes. 
    # Try: x>0: ceil(x)+1? 88.2->90 yes, 66->67 yes, 2.9->4 yes, 72.7->74 yes, 21.3->23 yes.
    # x<0: floor(x)? -20.3->-21 yes, -61.7->-62 yes, -24.3->-25 yes, -50.4->-51 yes, -6.0->-7? floor(-6)=-6 no.
    # -6.0->-7. Hmm. floor(-6.0)=-6. So -6.0 gives -7.
    # Maybe x<=0: floor(x)-? -6->-7 means -1. But -20.3->-21 is floor. 
    # Try round away from zero then adjust? 
    # Positive: ceil(x)+1. Negative: floor(x) except -6.0.
    # Actually maybe it's: for x>=0: ceil(x)+1; for x<0: floor(x)-? 
    # -6.0: floor=-6, need -7. -20.3: floor=-21, need -21. Inconsistent.
    # Try: round(x) with ties? -6.0 rounds to -6. no.
    # Maybe it's ceil(x)+1 for x>0, and floor(x)-1 for x<0? -20.3->-22 no.
    # Let me reconsider: maybe x<0: floor(x) but -6.0 is special? Or maybe it's trunc toward -inf then...
    # Actually: -6.0 -> -7 could be floor(-6.0)-1 = -7, but -20.3 floor-1=-22 no.
    # What if negative: round(x) then -1 if integer? -6->-7, -20.3 round=-20, -1=-21 yes! -61.7 round=-62,-1=-63 no.
    # Hmm -61.7->-62. round(-61.7)=-62. no -1.
    # Try: negative: floor(x) if not integer, else x-1. -20.3 floor=-21 ok. -61.7 floor=-62 ok. -24.3 floor=-25 ok. -50.4 floor=-51 ok. -6.0 integer -> -7 ok!
    # Positive: ceil(x)+1 if not integer, else x+1. 88.2 ceil=89+1=90 ok. 66.0 integer->67 ok. 2.9 ceil=3+1=4 ok. 72.7 ceil=73+1=74 ok. 21.3 ceil=22+1=23 ok.
    # So: x>0: ceil(x)+1 (works for integers too since ceil(66)=66, +1=67). 
    # Wait ceil(66.0)=66, +1=67 yes! So positive: ceil(x)+1 always.
    # Negative: floor(x) if non-integer, x-1 if integer. That's floor(x) for non-int, and for int x it's x-1 = floor(x)-1.
    # Actually for negative integer x, floor(x)=x, and we want x-1. For negative non-int, floor(x). 
    # Hmm, can unify: for x<0, if x is integer: x-1 else floor(x).
    # Alternatively: for x<0: floor(x) - (1 if x==floor(x) else 0).
    # Let's just code it.
    out = []
    for x in probe["x"]:
        if x > 0:
            out.append(math.ceil(x) + 1)
        elif x < 0:
            fl = math.floor(x)
            if x == fl:
                out.append(fl - 1)
            else:
                out.append(fl)
        else:  # x == 0
            out.append(1)  # guess: ceil(0)+1=1
    return {"y": out}

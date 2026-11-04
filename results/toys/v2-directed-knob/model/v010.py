import math

def predict(probe):
    # Beliefs (mechanism), each line cites evidence:
    # - switch has no effect on x,y,size [E1 vs E4]
    # - x depends only on a and b; c only affects y and size [E1,E2,E3]
    # - size is 1.0 at c=5, 2.5 at c=8; E12 size 2.0 at a=3,b=0,c=5 suggests size also depends on a,b
    # - y = c when b=5 [E1,E2,E3]; y = 5 when b=0,c=5 [E7,E8,E9]
    # - y = c+1 when a=8,b=5 [E5,E6]; y=6 when a=8,b=0,c=5 [E7]
    # - x: at a=5,b=5,c=5 -> 5 [E1]; a=5,b=8 -> 2 [E3]; a=5,b=0 -> 10 [E9]
    #   so x seems to decrease with b (b=5->5, b=8->2, b=0->10): x = 10 - b roughly
    # - a=8,b=5 -> x=10 [E5]; a=8,b=0 -> x=10 [E7]; a=2,b=0 -> x=4 [E8]; a=2,b=5 -> x=-1 [E11]
    #   a=3,b=0 -> x=6 [E12]
    #   Try x = a + (10 - b) - 10? a=5,b=5: 5+5-10=0 no.
    #   Try x = 10 - b + (a-5)*k. a=5: x=10-b. b=5->5 ok, b=8->2 ok, b=0->10 ok.
    #   a=8,b=5: 10-5+(3)k=5+3k=10 -> k=5/3? a=2,b=5: 5+(-3)k=-1 -> k=2. inconsistent.
    #   Try x = 10 - b + f(a). a=5: f=0. a=8,b=5: 10-5+f(8)=10 -> f(8)=5. a=8,b=0: 10+f(8)=10 -> f(8)=0. inconsistent.
    #   Maybe x = 10 - b when a=5; when a=8, x=10 regardless of b [E5,E7].
    #   a=2,b=0: x=4; a=2,b=5: x=-1. diff 5 over b diff 5 -> slope -1. x=4-b when a=2.
    #   a=3,b=0: x=6. x=6-b when a=3? 
    #   So x = (10 - b) + (a-5)*? Let's fit: a=5 -> 10-b. a=2,b=0 -> 4 = 10 + (2-5)*k -> -6=-3k -> k=2.
    #   Check a=2,b=5: 10-5+(-3)*2=5-6=-1 ok! a=3,b=0: 10-0+(-2)*2=6 ok! a=8,b=5: 10-5+3*2=11, but E5 says 10. Clamp at 10?
    #   a=8,b=0: 10-0+6=16 -> clamp 10 ok [E7]. a=8,b=5: 11 -> clamp 10 ok [E5].
    #   So x = clamp(10 - b + 2*(a-5), -inf, 10)? Check a=5,b=8: 2+0=2 ok. a=5,b=0: 10 ok. 
    #   Lower clamp? a=2,b=5 -> -1, so no lower clamp at 0.
    # - size: c=5 -> 1.0 generally [E1,E3,E4,E9], but E5,E7,E8,E10,E11 have size 2.5 at c=5.
    #   E12 size 2.0 at a=3,b=0,c=5. E2 c=8 -> 2.5, E6 c=8 -> 1.0.
    #   Looks like size depends on parity/region. E1(a5,b5,c5)=1; E3(a5,b8,c5)=1; E9(a5,b0,c5)=1 -> b=5 or 8 or 0 with a=5 all 1.
    #   E5(a8,b5,c5)=2.5; E7(a8,b0,c5)=2.5; E8(a2,b0,c5)=2.5; E11(a2,b5,c5)=2.5; E10(a8,b2,c5)=2.5.
    #   E12(a3,b0,c5)=2.0.
    #   E2(a5,b5,c8)=2.5; E6(a8,b5,c8)=1.0.
    #   Hypothesis: size = 1.0 if (a=5) XOR (c=8)? E1 a5,c5 ->1; E2 a5,c8 ->2.5; E6 a8,c8 ->1; E5 a8,c5 ->2.5. Yes!
    #   But E3 a5,c5 ->1 ok; E9 a5,c5->1 ok. E7 a8,c5->2.5 ok; E8 a2,c5->2.5 ok; E11 a2,c5->2.5 ok; E10 a8,c5->2.5 ok.
    #   E12 a3,c5 -> 2.0, not 2.5. So a=3 special? Maybe size depends on a: size=2.5 for a!=5, but a=3 gives 2.0?
    #   Or size = 1.0 + 1.5*|a-5|/3? a=5->1, a=8->1+1.5=2.5, a=2->2.5, a=3->1+1=2.0. Yes! size = 1 + 0.5*|a-5| when c=5.
    #   Check c=8: E2 a5 -> 1+0=1 but observed 2.5. So c matters.
    #   Maybe size = 1 + 0.5*|a-5| + something for c? E2 a5,c8 -> 2.5, so c=8 adds 1.5 when a=5.
    #   E6 a8,c8 -> 1.0, but formula gives 1+1.5+? = 2.5+. So no.
    #   Alternative: size = 1.0 if (a=5 and c=5) or (a=8 and c=8); else 2.5, except a=3 gives 2.0?
    #   Let's think: maybe size = 1 + 0.5*|a-5| when c=5, and when c=8 size = 1 + 0.5*|a-5|? E2 a5,c8: 1+0=1 no.
    #   Maybe size = 1 + 0.5*|a-5| + 0.5*|c-5|? E1:1+0+0=1 ok. E2 a5,c8:1+0+1.5=2.5 ok. E6 a8,c8:1+1.5+1.5=4 no.
    #   Maybe size = 1 + 0.5*|a-5| * something? 
    #   Try: size = 1.0 + 0.5*|a-5| if c=5; size = 1.0 + 0.5*|c-8|*? 
    #   E2 a5,c8 -> 2.5. E6 a8,c8 ->1.0. So at c=8, a=5 gives 2.5, a=8 gives 1.0. That's like size = 1 + 0.5*|a-5| but inverted? a5->1? no.
    #   Maybe size = 1.0 + 0.5*|a-5| when c=5 AND when c=8 it's 1.0 + 0.5*|a-8|? E2 a5,c8: 1+1.5=2.5 ok. E6 a8,c8:1+0=1 ok.
    #   So size = 1 + 0.5*|a - (5 if c==5 else 8)|? For c=8, center at a=8.
    #   But what about c other than 5,8? Unknown; assume linear in c? Mark with ?.
    #   Simplify: size = 1 + 0.5*|a - center(c)| where center(5)=5, center(8)=8. Maybe center(c)=c? Then size=1+0.5*|a-c|. Check E1:1+0=1 ok. E2:1+0.5*3=2.5 ok. E6:1+0=1 ok. E3 a5,c5:1 ok. E5 a8,c5:1+1.5=2.5 ok. E7 a8,c5:2.5 ok. E8 a2,c5:1+1.5=2.5 ok. E11 a2,c5:2.5 ok. E10 a8,c5:2.5 ok. E12 a3,c5:1+1=2.0 ok! E4 same as E1. E9 a5,c5:1 ok.
    #   So size = 1 + 0.5*|a - c|. 
    # - y: E1 a5,b5,c5 ->5; E2 a5,b5,c8 ->8 (y=c); E3 a5,b8,c5 ->5 (y=c? c=5 yes); E5 a8,b5,c5 ->6 (y=c+1); E6 a8,b5,c8 ->9 (y=c+1); E7 a8,b0,c5 ->6; E8 a2,b0,c5 ->5; E9 a5,b0,c5 ->5; E10 a8,b2,c5 ->6; E11 a2,b5,c5 ->5.
    #   So y = c + (1 if a=8 else 0)? E5,E6,E7,E10 all a=8 -> y=c+1. E8 a2 -> y=c=5. E11 a2 -> y=5. E1 a5 -> y=5. E3 a5 -> y=5. E9 a5 -> y=5. E2 a5 -> y=8=c.
    #   So y = c + (1 if a==8 else 0). But what about b? E7 a8,b0 ->6=c+1; E5 a8,b5->6=c+1; E10 a8,b2->6. So b doesn't matter for y. Good.
    # - x: x = 10 - b + 2*(a-5), clamped at 10? Check E1:10-5+0=5 ok. E2 same 5 ok. E3:10-8+0=2 ok. E5:10-5+6=11 ->10 ok. E6 same 10 ok. E7:10-0+6=16->10 ok. E8:10-0-6=4 ok. E9:10-0+0=10 ok. E10:10-2+6=14->10 ok. E11:10-5-6=-1 ok. E12:10-0-4=6 ok.
    #   So x = min(10, 10 - b + 2*(a-5)). No lower clamp observed.
    # - switch ignored entirely [E1 vs E4].

    a = float(probe.get("a", 5))
    b = float(probe.get("b", 5))
    c = float(probe.get("c", 5))
    # switch not used

    x = 10 - b + 2 * (a - 5)
    if x > 10:
        x = 10.0
    # no lower clamp observed; keep as is

    y = c + (1.0 if a == 8 else 0.0)

    size = 1.0 + 0.5 * abs(a - c)

    return {"x": round(x, 2), "y": round(y, 2), "size": round(size, 2)}

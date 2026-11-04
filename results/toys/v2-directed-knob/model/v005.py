def predict(probe):
    # x = a + b - 5 [E1, E3, E5, E6, E7]
    #   E1: a=5,b=5 -> 5
    #   E3: a=5,b=8 -> 8? no, observed 2. Hmm.
    #   Wait: E3 a=5,b=8 -> x=2. E7 a=8,b=0 -> x=10. E5 a=8,b=5 -> x=10.
    #   E5 and E7 both a=8 give x=10 regardless of b (5 vs 0)! So b doesn't affect x?
    #   But E3 a=5,b=8 -> x=2, E1 a=5,b=5 -> x=5. So b DOES affect x at a=5.
    #   E5 a=8,b=5 ->10; E7 a=8,b=0 ->10. b no effect at a=8.
    #   E3 a=5,b=8 ->2; E1 a=5,b=5 ->5. b effect -1 per unit at a=5.
    #   Maybe x = a + b - 5 only when... no.
    #   Try x = a + (5-b) when a=5? E3: 5+(-3)=2 ok. E1: 5+0=5 ok.
    #   E5: a=8,b=5 -> 8+0=8 no (obs 10).
    #   Try x = a + b - 5: E5 8+5-5=8 no.
    #   Hmm. x at a=8 is 10 for b=5 and b=0. x at a=5: b=5->5, b=8->2.
    #   Maybe x = a + b - 5 clipped? no.
    #   Maybe x = a + (5-b) * something depending on a.
    #   At a=5: slope in b is -1. At a=8: slope in b is 0.
    #   Guess: x = a + (5-b)*max(0, (8-a)/3)? At a=5: (8-5)/3=1 -> a+(5-b)=5+5-b=10-b. E1 b=5->5 ok, E3 b=8->2 ok.
    #   At a=8: factor 0 -> x=a=8, but obs 10. No.
    #   Try x = a + (5-b)*(1 - (a-5)/3)? a=5: 1 -> 10-b ok. a=8: 0 -> x=8 no.
    #   Maybe x = a + b - 5 for a<=5, and x = a + 2 for a>=8? E5,E7: 8+2=10 ok.
    #   Let's just try x = a + b - 5 when a<=5, x = a+2 when a>=8? Need boundary.
    #   Actually maybe x = a + b - 5 but b is clamped: effective b = min(b, 5)? 
    #   E3 b=8 -> eff 5 -> 5+5-5=5 no (obs 2).
    #   Hmm E3 needs b=8 to give -3.
    #   Let's reconsider: maybe x = a + b - 5 with a,b... E5 8+5-5=8, obs 10. diff +2.
    #   E7 8+0-5=3, obs 10. diff +7.
    #   So at a=8, x=10 constant. At a=5, x=10-b.
    #   Maybe x = a + b - 5 + correction. Correction at a=8: E5 +2, E7 +7. Not constant.
    #   Alternative: x = a + (5-b) when a=5; x = a+2 when a=8. 
    #   Maybe x = a + (5-b)*max(0,1-(a-5)/3) + (a-5)*? 
    #   Let's try: x = a + (5-b)*(1-(a-5)/3) + (a-5)*(2/3)? 
    #   a=5: 5+(5-b)*1+0=10-b ok.
    #   a=8: 8+(5-b)*0+3*(2/3)=8+2=10 ok! 
    #   So x = a + (5-b)*(1-(a-5)/3) + (a-5)*(2/3)
    #   = a + (5-b)*(8-a)/3 + (a-5)*2/3
    #   Check a=5,b=5: 5+0+0=5 ok. a=5,b=8: 5+(-3)*1+0=2 ok.
    #   a=8,b=5: 8+0+2=10 ok. a=8,b=0: 8+5*0+2=10 ok.
    #   Simplify: x = a + (a-5)*2/3 + (5-b)*(8-a)/3
    #   = a + (2a-10)/3 + (40-5a-8b+ab)/3
    #   = (3a + 2a-10 + 40-5a-8b+ab)/3 = (30 - 8b + ab)/3 = (30 + b(a-8))/3
    #   Check: a=5,b=5: (30+5*(-3))/3=(30-15)/3=5 ok. a=5,b=8: (30+8*(-3))/3=6/3=2 ok.
    #   a=8,b=5: (30+5*0)/3=10 ok. a=8,b=0: 30/3=10 ok.
    #   Nice: x = 10 + b*(a-8)/3. That's clean!
    #   Check E6 a=8,b=5: 10+5*0/3=10 ok.
    # y = c + (a-5)/3 [E1,E2,E3,E5,E6,E7]
    #   E5 a=8,c=5: 5+1=6 ok. E6 a=8,c=8: 8+1=9 ok. E7 a=8,c=5: 6 ok.
    # size = 1 + 0.5*|a-c| [E1,E2,E3,E5,E6,E7]
    #   E5 a=8,c=5: 1+1.5=2.5 ok. E6 a=8,c=8: 1 ok. E7 a=8,c=5: 2.5 ok.
    # switch: no effect [E4]
    a = probe.get("a", 5)
    b = probe.get("b", 5)
    c = probe.get("c", 5)
    x = 10 + b*(a-8)/3.0
    y = c + (a-5)/3.0
    size = 1 + 0.5*abs(a-c)
    return {"x": round(x, 2), "y": round(y, 2), "size": round(size, 2)}

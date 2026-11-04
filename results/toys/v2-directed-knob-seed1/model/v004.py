import math

def predict(probe):
    # x = a - 5 [E4: a=0 -> x=-5; E5: a=10 -> x=10? wait]
    #   E4 a=0 -> x=-5, E5 a=10 -> x=10, E1 a=5 -> x=5, E6 a=5 -> x=0?!
    #   E1 a=5,b=5,c=5 -> x=5; E6 a=5,b=10,c=5 -> x=0. So x depends on b too.
    #   x = a - 5 + ? E6: a=5,b=10 -> x=0 => a-5=0, so x=0 means b contributes 0 at b=10? 
    #   Hmm E1 b=5 -> x=5=a. E6 b=10 -> x=0. E4 a=0,b=5 -> x=-5. E5 a=10,b=5 -> x=10.
    #   At b=5: x=a. At b=10: x=a-5. So x = a - (b-5)? E1: 5-0=5 ok. E6: 5-5=0 ok.
    #   E4: 0-0=0 but observed -5. Contradiction.
    #   Try x = a - 5*(b-5)/5 = a-(b-5). E4 a=0,b=5: 0-0=0, observed -5. No.
    #   Reconsider: E4 a=0,b=5,c=5 -> x=-5. E5 a=10,b=5,c=5 -> x=10. E1 a=5,b=5 -> x=5.
    #   So at b=5: x = a-5? E1: 5-5=0 but observed 5. No.
    #   At b=5: a=0->-5, a=5->5, a=10->10. Not linear in a alone (0->-5,5->5,10->10).
    #   Slope 0..5: 2 per a; 5..10: 1 per a. Hmm.
    #   Maybe x = a - 5 + something. a=0:-5 => -5+0. a=5:5 => 5+0. a=10:10 => 10+0.
    #   So x=a-5 only at a=0. At a=5 x=5=a. At a=10 x=10=a.
    #   Actually a=5->5, a=10->10: x=a. a=0->-5: x=a-5.
    #   E6 a=5,b=10 -> x=0. So b matters.
    #   Guess: x = a - 5*(b-5)/5? E6: 5-5=0 ok. E1:5-0=5 ok. E4:0-0=0 no (obs -5).
    #   Maybe x = a - (b-5) - (something with a)? 
    #   Let's tabulate (a,b,c)->x: (5,5,5)->5, (5,5,0)->5, (5,5,5 on)->5, (0,5,5)->-5, (10,5,5)->10, (5,10,5)->0.
    #   At b=5,c=5: a=0->-5, a=5->5, a=10->10. 
    #   Piecewise? a<=5: x=2a-5? a=0->-5, a=5->5. a>=5: x=a? a=5->5,a=10->10.
    #   That's x = a + max(0, a-5) - 5*max(0,5-a)/5... messy. 
    #   Alternative: x = a - 5 + 2*min(a,5)? a=0: -5+0=-5 ok. a=5:0+10=10 no.
    #   Try x = 2a-5 for a<=5, x=a for a>=5. Check E6 a=5: 5. But obs 0. b matters.
    #   E6 b=10 shifts x by -5 from E1. So x = f(a) - (b-5)? E1: f(5)-0=5 => f(5)=5. E6: 5-5=0 ok.
    #   E4: f(0)-0=-5 => f(0)=-5. E5: f(10)-0=10 => f(10)=10.
    #   So f(0)=-5, f(5)=5, f(10)=10. And x = f(a) - (b-5).
    #   f: piecewise linear: 0->-5, 5->5 (slope 2), 5->10 (slope 1). 
    #   f(a) = 2a-5 for a<=5; f(a)=a for a>=5. Check f(5)=5 both. ok.
    #   So x = (2a-5 if a<=5 else a) - (b-5).
    #   Hmm but is b shift linear? Only one data point (b=10). Assume linear: x = f(a) - (b-5).
    #   Actually maybe simpler: x = a - 5 + 2*min(a,5) - (b-5)? a=0:-5+0-0=-5 ok. a=5:0+10-0=10 no.
    #   Keep piecewise.
    # y: E1 (5,5,5)->5. E2 (5,5,0)->0. E4 (0,5,5)->5. E5 (10,5,5)->6. E6 (5,10,5)->5.
    #   E6: b=10 but y=5, same as b=5! So b does NOT add to y. y independent of b.
    #   y at c=5: a=0->5, a=5->5, a=10->6. So y=5 + max(0,(a-5)/5).
    #   c scales: c=0->0, c=5->5. y = (5 + max(0,(a-5)/5)) * c/5.
    #   Check E2: (5+0)*0=0 ok. E1:5*1=5 ok. E4:5*1=5 ok. E5:(5+1)*1=6 ok. E6:(5+0)*1=5 ok.
    # size: E1 1.0, E2 3.5, E4 3.5, E5 3.5, E6 1.0.
    #   size = 1 + 2.5*|a-5|/5 + 2.5*(5-c)/5. E6 a=5,c=5:1 ok. E2:1+0+2.5=3.5 ok.
    #   E4:1+2.5+0=3.5 ok. E5:3.5 ok. E1:1 ok.
    # switch: no effect [E3].
    a = probe.get("a", 5)
    b = probe.get("b", 5)
    c = probe.get("c", 5)
    f = 2*a - 5 if a <= 5 else a
    x = f - (b - 5)
    y = (5 + max(0.0, (a - 5) / 5.0)) * (c / 5.0)
    size = 1.0 + 2.5 * abs(a - 5) / 5.0 + 2.5 * (5 - c) / 5.0
    return {"x": x, "y": y, "size": size}

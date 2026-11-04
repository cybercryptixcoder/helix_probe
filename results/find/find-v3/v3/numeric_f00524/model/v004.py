def predict(probe):
    # f(x) = ceil(x) if ceil(x) in {1,2,3,4} or {-1,-2,-3,-4}, else 0 [E1,E2,E3]
    # E4: 4.2->5, 4.8->0. So the positive band is 1..5, not 1..4.
    #     -4.8->0, -4.2->-4: negative band stays -4..-1.
    #     -4.001->-4 (ceil=-4, in band) yes; -4.999->0 (ceil=-4? no, ceil(-4.999)=-4)...
    #     Wait: ceil(-4.999) = -4, which IS in [-4,-1], but observed 0.
    #     So negatives are NOT ceil. -4.999->0, -4.001->-4, -4.2->-4, -4.8->0.
    #     That's round-half-up? round(-4.2)=-4, round(-4.8)=-5->0, round(-4.001)=-4. Yes!
    #     Positives: 4.2->5, 4.8->0, 3.8->4, 2.2->3, 1.8->2, 0.8->1, 0.2->1.
    #     round-half-up: 0.2->0 no. So positives use ceil. Negatives use round.
    #     Check -1.2->-1 (round=-1 yes), -1.8->-1 (round=-2? no, observed -1).
    #     Hmm -1.8->-1: that's ceil(-1.8)=-1. But -4.8->0 not -4.
    #     So: negatives ceil too, but band is -4..-1 AND ceil must equal... -4.8 ceil=-4 in band but 0.
    #     Difference: -4.8 rounds to -5 (out of band), -1.8 rounds to -2 (in band).
    #     Try: r = round-half-up(x); if r in {1..5} or {-4..-1} output r else 0.
    #     -1.8 round=-2 in band -> -2, but observed -1. Contradiction.
    #     Try: r = ceil(x) for x>0, floor(x) for x<0? -1.8 floor=-2 no.
    #     Recheck: -1.2->-1, -1.8->-1, -2.2->-2, -3.8->-3, -4.2->-4, -4.8->0.
    #     -1.8->-1 = ceil. -4.8->0: ceil=-4 in band, so why 0? Maybe band is -4..-1 but
    #     the value must satisfy ceil in band AND... -4.8: maybe threshold at -4.5?
    #     -4.2->-4, -4.8->0: cutoff between -4.2 and -4.8. -4.001->-4, -4.999->0.
    #     Looks like round-half-up on negatives: -4.2->-4, -4.8->-5(out)->0, -4.001->-4, -4.999->-5->0.
    #     -1.8 round=-2 but observed -1. Unless -1.8->-1 means round-half... no.
    #     Actually maybe it's ceil for all, but band check uses ceil in [-4,-1] AND x >= -4.5?
    #     -4.8 < -4.5 -> 0. -4.2 >= -4.5 -> -4. -1.8 -> -1. Consistent!
    #     Positive: 4.8->0, 4.2->5. ceil(4.8)=5, 5 not in 1..5? it is. But observed 0.
    #     So positive band 1..5 but 4.8->0. ceil(4.8)=5 in band yet 0. So maybe band is 1..4 for
    #     ceil but 4.2->5 contradicts. 4.2 ceil=5, observed 5. 4.8 ceil=5, observed 0.
    #     Difference: 4.2<4.5, 4.8>4.5. So threshold 4.5 on positives too!
    #     So: r=ceil(x); if x in (-4.5, 4.5) and r in {1..4} or {-4..-1}... but 4.2->5.
    #     r=ceil(4.2)=5, output 5. So band includes 5 for x<4.5.
    #     Simplest: r=ceil(x); output r if r in {-4..-1} or {1..5}, else 0, BUT x must be in (-4.5,4.5).
    #     Check 4.8: x>4.5 -> 0. 4.2: r=5 in band -> 5. 0.2: r=1 ->1. -4.8: x<-4.5->0.
    #     -4.2: r=-4 ->-4. -4.999: x<-4.5->0. -4.001: r=-4->-4. All match E4.
    #     E2: 5->0 (r=5 in band but x=5>4.5 ->0) yes. 4->4 yes. -5->0 (x<-4.5) yes.
    #     E1: 2.9->3 yes. E3: 1.2->2 yes.
    import math
    out = []
    for x in probe["x"]:
        r = math.ceil(x)
        if -4.5 < x < 4.5 and ((1 <= r <= 5) or (-4 <= r <= -1)):
            out.append(float(r))
        else:
            out.append(0.0)
    return {"y": out}

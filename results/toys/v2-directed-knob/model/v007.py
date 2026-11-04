def predict(probe):
    # x: at a=5, x=10-b [E1 b=5->5, E3 b=8->2, E9 b=0->10]
    #    at a=8, x=10 regardless of b [E5 b=5->10, E6 b=5->10, E7 b=0->10]
    #    at a=2,b=0 -> x=4 [E8]
    #    So x=10-b when a=5; x=10 when a=8; x=4 when a=2,b=0.
    #    Try x = 10 - b*(8-a)/3 : a=5 -> 10-b [E1,E3,E9 ok]; a=8 -> 10 [E5,E6,E7 ok];
    #       a=2,b=0 -> 10 [E8 obs 4, FAILS].
    #    Hmm E8 a=2,b=0 -> 4. So x=10-b*(8-a)/3 gives 10 at a=2,b=0, wrong.
    #    Try x = a+2 - b*(8-a)/3: a=5 -> 7-b [E9 b=0->7 obs10 FAILS].
    #    So neither pure form. Let's tabulate x:
    #      (a=5,b=5)->5, (5,8)->2, (5,0)->10  => x=10-b at a=5
    #      (8,5)->10, (8,0)->10              => x=10 at a=8
    #      (2,0)->4
    #    At b=0: a=5->10, a=8->10, a=2->4. Not linear in a (5->10,8->10 flat then 2->4).
    #    Maybe x = 10 - b*(8-a)/3 for a>=5, and something else for a<5.
    #    At a=2,b=0: x=4. Guess x = a+2 for a<5 at b=0? a=2->4 ok.
    #    Try x = 10 - b*(8-a)/3 when a>=5; x = a+2 when a<5 (b irrelevant?).
    #    Check a=5 falls in a>=5: 10-b ok [E1,E3,E9].
    #    a=8: 10 ok [E5,E6,E7]. a=2,b=0: 4 ok [E8].
    #    This is a clean piecewise rule. Use it.
    # y = c + max(0,(a-5)/3) [E1,E2,E5,E6,E8,E9]
    # size = 1 + 0.5|a-c| [E1,E2,E3,E5,E6,E7,E8,E9]
    # switch: no effect [E4]
    a = probe.get("a", 5)
    b = probe.get("b", 5)
    c = probe.get("c", 5)
    if a >= 5:
        x = 10 - b*(8-a)/3.0
    else:
        x = a + 2
    y = c + max(0, (a-5)/3.0)
    size = 1 + 0.5*abs(a-c)
    return {"x": round(x, 2), "y": round(y, 2), "size": round(size, 2)}

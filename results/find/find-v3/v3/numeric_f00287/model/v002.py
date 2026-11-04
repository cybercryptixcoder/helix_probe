import math

def predict(probe):
    # A: negative side, x <= -5.5, y = -0.7*x  [E1: -6->4.2, -20.3->14.7; E2: -100->70,-50->35,-10->7; E4: -5.5->4.2]
    # B: middle flat region, -5.5 < x < 18, y ≈ -402.4 (noisy)  [E2, E4]
    # C: positive side, x >= 18, y = -16.8*x  [E3, E4: 18->-319.2, 21->-352.8; E2: 50,100]
    # Boundaries: negative/middle at x=-5.5 (E4: -5.5 gives 4.2 = -0.7*-5.5, -5.0 gives middle).
    #             middle/positive at x=18 (E4: 17 middle, 18 gives -319.2 = -16.8*19? no: -16.8*19=-319.2).
    #   Wait: 18 -> -319.2 = -16.8*19, 19 -> -336 = -16.8*20, 20 -> -352.8 = -16.8*21.
    #   Hmm, that's off by one. Let's check: -16.8*18 = -302.4, but observed -319.2.
    #   Actually -319.2/18 = -17.733. -336/19=-17.68, -352.8/20=-17.64.
    #   But E3: 30.3 -> -504 = -16.63*30.3; 65.5->-1092=-16.67; 104.5->-1747.2=-16.72.
    #   E2: 50->-840=-16.8, 100->-1680=-16.8.
    #   So slope ~ -16.8 but E4 values at 18,19,20 are slightly steeper. Possibly noise.
    #   -16.8*18=-302.4 vs -319.2 (diff 16.8). -16.8*19=-319.2 vs -336 (diff 16.8). Consistent offset!
    #   So maybe y = -16.8*(x+1) for x>=18? Check 21: -16.8*22=-369.6 vs -352.8. No.
    #   Actually -352.8 = -16.8*21. So at x=21 it's -16.8*x. At 18 it's -16.8*19.
    #   Let's just fit: 18->-319.2, 19->-336, 20->-352.8, 21->-352.8? No 21->-352.8.
    #   Differences: 18->19: -16.8, 19->20: -16.8, 20->21: 0? -352.8-(-352.8)=0. Hmm 21->-352.8 same as 20.
    #   Wait observed: 18:-319.2, 19:-336.0, 20:-352.8, 21:-352.8. Last two equal? That's odd.
    #   Actually E4 list: ...,18.0,19.0,20.0,21.0 -> ...,-319.2,-336.0,-352.8,-352.8? Let me recount.
    #   y list: 4.2,-402.1246,-402.2475,-402.2358,-402.3651,-402.3926,-402.1867,-402.3358,-402.6463,
    #          -402.3998,-402.2819,-402.427,-402.3307,-402.1555,-402.3134,-402.5408,-402.2221,-319.2,-336.0,-352.8
    #   That's 20 values for x=[-5.5,-5,-4.5,-4,-3.5,-3,-2.5,-2,-1.5,11,12,13,14,15,16,17,18,19,20,21]
    #   So 18->-319.2, 19->-336.0, 20->-352.8, 21->? only 20 values, last is -352.8 for x=21.
    #   Wait count: x has 20 entries. y has 20 entries. Index 17 (x=18)->-319.2, 18(x=19)->-336, 19(x=20)->-352.8.
    #   And x=21? Not present? x list: -5.5,-5,-4.5,-4,-3.5,-3,-2.5,-2,-1.5 (9), 11,12,13,14,15,16,17,18,19,20,21 (11) = 20.
    #   So indices 9-19 are 11,12,...,21. Index 17 = 18, index 18=19, index 19=20. So x=21 is NOT in list! 
    #   Let me recount x: [-5.5,-5.0,-4.5,-4.0,-3.5,-3.0,-2.5,-2.0,-1.5,11.0,12.0,13.0,14.0,15.0,16.0,17.0,18.0,19.0,20.0,21.0]
    #   That's 9 + 11 = 20. Indices: 0..8 negative, 9=11,10=12,11=13,12=14,13=15,14=16,15=17,16=18,17=19,18=20,19=21.
    #   y indices: 16->-402.2221 (x=18 middle!), 17->-319.2 (x=19), 18->-336 (x=20), 19->-352.8 (x=21).
    #   So boundary: x=18 middle, x=19 positive. -16.8*19=-319.2 ✓, -16.8*20=-336 ✓, -16.8*21=-352.8 ✓.
    #   So positive regime starts at x=19, and y=-16.8*x. 
    # Negative boundary: x=-5.5 -> 4.2 = -0.7*-5.5 ✓ (negative regime), x=-5.0 -> middle.
    #   So negative regime x <= -5.5, middle -5.5 < x < 19, positive x >= 19.
    out = []
    for x in probe["x"]:
        if x <= -5.5:
            y = -0.7 * x
        elif x < 19:
            y = -402.4
        else:
            y = -16.8 * x
        out.append(y)
    return {"y": out}

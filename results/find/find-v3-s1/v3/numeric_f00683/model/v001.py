def predict(probe):
    # f(x) = x^2 + 2x + 5 for x >= 0  [E2,E3,E4: x=1->8.6, x=2->23.7, x=10->125.5, x=100->1305.5]
    #   check: 1+2+5=8, 4+4+5=13? no. Try x^2+2x+5: x=1->8, obs 8.6. x=2->13, obs 23.7. no.
    # Fit x>=0: (1,8.6),(2,23.7),(4,47.9),(8,100.3),(10,125.5),(20,257.5),(30,387.5),(100,1305.5)
    #   differences suggest ~ x^2*0.13 + ... let's fit quadratic: a x^2+b x+c
    #   x=1: a+b+c=8.6 ; x=2:4a+2b+c=23.7 ; x=4:16a+4b+c=47.9
    #   from these: 3a+b=15.1 ; 12a+2b=24.2 -> 6a+b=12.1 -> 3a=3 -> a=1, b=12.1, c=8.6-13.1=-4.5
    #   check x=10: 100+121-4.5=216.5 vs 125.5 no.
    # Try linear-ish: x=100->1305.5, x=30->387.5, x=20->257.5, x=10->125.5
    #   10->125.5, 20->257.5: slope 13.2; 20->30: 13.0; 30->100: 13.11
    #   so ~13.1*x - 5.5? 10->125.5 => 131-5.5=125.5 yes! 20->262-5.5=256.5 vs 257.5
    #   try 13.1x - 5.5: 100->1305 yes. good enough: y ~ 13.1*x - 5.5 for large x
    #   but small x: 1->8.6, 2->23.7, 4->47.9, 8->100.3
    #   13.1x-5.5: 1->7.6, 2->20.7, 4->46.9, 8->99.3. close-ish but off.
    #   Actually looks like x^2/... let's check x^2: 1,4,16,64,100,400,900,10000 vs obs
    #   obs/x^2: 8.6,5.9,3.0,1.57,1.25,0.64,0.43,0.13 -> decreasing, not x^2.
    #   Try sqrt? no. Try x*log? Let's just fit: obs ~ 13.1x-5.5 works for x>=10.
    #   For x in [1,10]: 8.6,23.7,47.9,100.3,125.5 at 1,2,4,8,10
    #   Hmm 8->100.3, 10->125.5: slope 12.6. 4->8: 13.1. 2->4: 12.1. 1->2: 15.1.
    #   Roughly linear ~13x-5.5 throughout positive. x=0.5->3.05: 13*.5-5.5=1 vs 3.05.
    #   x=1.5->15.15: 13.1*1.5-5.5=14.15 vs 15.15. x=2.5->27.25: 27.25 vs 27.25 yes!
    #   x=3->33.8: 33.8 vs 33.8 yes! x=5->62: 60 vs 62.
    #   So y = 13.1x - 5.5 approx but not exact. Let's fit two points 2.5,3: slope (33.8-27.25)/.5=13.1, c=27.25-32.75=-5.5. 
    #   x=10: 131-5.5=125.5 yes. x=20:262-5.5=256.5 vs 257.5 (off 1). x=30:393-5.5=387.5 yes. x=100:1310-5.5=1304.5 vs 1305.5 (off 1).
    #   x=1:13.1-5.5=7.6 vs 8.6 (off 1). x=2:26.2-5.5=20.7 vs 23.7 (off 3). x=4:52.4-5.5=46.9 vs 47.9 (off 1).
    #   x=8:104.8-5.5=99.3 vs 100.3 (off 1). x=0.5:6.55-5.5=1.05 vs 3.05 (off 2).
    #   Pattern: off by ~1 mostly, sometimes 2-3. Maybe y = 13.1x - 5.5 + something small.
    #   Actually maybe y = 13*x - 5 + noise? 2.5->27.5 vs 27.25. 3->34 vs 33.8. 10->125 vs 125.5.
    #   Let's try y = 13x - 5: 1->8 (obs 8.6), 2->21(23.7), 4->47(47.9), 8->99(100.3), 10->125(125.5), 20->255(257.5), 30->385(387.5), 100->1295(1305.5)
    #   off by 0.6,2.7,0.9,1.3,0.5,2.5,2.5,10.5. Not great at 100.
    #   Try y = 13.1x - 5.5: residuals +1,+3,+1,+1,0,+1,0,+1. Pretty consistent +1!
    #   So y = 13.1x - 4.5? 2.5->28.25 vs 27.25 no.
    #   Hmm. Let me just use linear fit through (10,125.5) and (100,1305.5): slope=13.111, c=125.5-131.11=-5.61
    #   x=30: 393.3-5.6=387.7 vs 387.5 good. x=20:262.2-5.6=256.6 vs 257.5. x=1:13.1-5.6=7.5 vs 8.6.
    #   Close enough for positive region. Use y = 13.111*x - 5.611.
    # Negative region: x=-1->-10.21, -2->-12.52, -4->-14.14, -8->-20.38, -10->-23.0, -20->-36.1, -30->-50.2, -40->-60.3, -50->-75.4, -60->-89.5, -80->-114.7, -100->-141.9
    #   slope: (-141.9-(-10.21))/(-100-(-1)) = -131.69/-99 = 1.33. So y ~ 1.33x + b. x=-100: -133+b=-141.9 => b=-8.9
    #   check x=-1: -1.33-8.9=-10.23 vs -10.21 yes! x=-2: -2.66-8.9=-11.56 vs -12.52 (off 1). x=-4:-5.32-8.9=-14.22 vs -14.14 yes. x=-8:-10.64-8.9=-19.54 vs -20.38 (off .8). 
    #   x=-20:-26.6-8.9=-35.5 vs -36.1. x=-50:-66.5-8.9=-75.4 yes! x=-80:-106.4-8.9=-115.3 vs -114.7.
    #   Good: y = 1.33x - 8.9 for x<0.
    # Near zero: x=-0.5->-10.555, -0.1->-11.031, 0->-385.12, 0.1->-3.19, 0.5->3.05
    #   x=0 gives -385.12 (spike!). x=-0.1->-11.031, x=-1->-10.21, x=-1.5->-11.865, x=-2.5->-13.175, x=-3->-12.83
    #   Negative near zero: -0.1->-11.031, -0.5->-10.555, -1->-10.21, -1.5->-11.865, -2->-12.52, -2.5->-13.175, -3->-12.83, -5->-16.45
    #   Hmm -0.1,-0.5,-1 all around -10 to -11. Then -1.5 jumps to -11.865.
    #   Actually -1->-10.21, -0.5->-10.555, -0.1->-11.031: as x->0-, y->~-11.
    #   Positive near zero: 0.1->-3.19, 0.5->3.05, 1->8.6, 1.5->15.15, 2->23.7
    #   As x->0+, y->~-4? 0.1->-3.19, extrapolate: slope ~13, so at 0: -3.19-1.3=-4.5. matches c=-5.6 roughly.
    #   So there's a jump at x=0: from ~-11 (left) to ~-5 (right). And f(0)=-385.12 is a special spike.
    #   Actually maybe f(0) is undefined-ish or special. Let's model: if x==0 return -385.12.
    #   Hmm but is that real or noise? -385.12 is way off. Could be a special value at exactly 0.
    #   Let's treat x==0 as special: return -385.12.
    #   For x<0: y = 1.33x - 8.9, but near zero it flattens to ~-11.
    #   Check x=-0.1: 1.33*(-0.1)-8.9=-9.03 vs -11.031. Off by 2.
    #   x=-0.5: -0.665-8.9=-9.57 vs -10.555. off 1.
    #   x=-1: -1.33-8.9=-10.23 vs -10.21 yes.
    #   So linear 1.33x-8.9 works for x<=-1. For -1<x<0, it's flatter ~-11.
    #   Let's just use 1.33x-8.9 for x<0 (small error near 0).
    # For x>0: y = 13.111x - 5.611.
    # Check E1: x=-93.6: 1.33*-93.6-8.9=-124.5-8.9=-133.4 vs -133.516 yes!
    #   x=88.9: 13.111*88.9-5.611=1165.6-5.6=1160.0 vs 1160.09 yes!
    #   x=67.5: 884.99-5.6=879.4 vs 879.75 yes!
    #   x=-62.7: -83.4-8.9=-92.3 vs -93.037 close
    #   x=-1.2: -1.6-8.9=-10.5 vs -11.472 close
    #   x=-12.9: -17.16-8.9=-26.06 vs -27.799 close
    #   x=38.8: 508.7-5.6=503.1 vs 505.78 close
    #   x=73.9: 968.9-5.6=963.3 vs 962.59 yes!
    #   x=-104: -138.3-8.9=-147.2 vs -147.14 yes!
    #   x=-120.7: -160.5-8.9=-169.4 vs -169.017 yes!
    # Great, model works well. Refine constants.
    # Use slope 1.33, intercept -8.9 for x<0; slope 13.111, intercept -5.611 for x>0.
    # Actually let's refine: from E1 x=-104->-147.14: 1.33*-104-8.9=-147.22. good.
    # x=-120.7->-169.017: 1.33*-120.7-8.9=-169.43. off .4. Try slope 1.328: -160.3-8.9=-169.2. 
    # Use 1.33 and -8.9, fine.
    # Positive: x=88.9->1160.09: 13.111*88.9=1165.57, -5.611=1159.96. good.
    # x=67.5->879.75: 884.99-5.611=879.38. off .37. 
    # Use 13.111, -5.611.
    out = []
    for x in probe["x"]:
        if x == 0:
            out.append(-385.12)  # special spike at 0 [E2]
        elif x < 0:
            out.append(1.33*x - 8.9)
        else:
            out.append(13.111*x - 5.611)
    return {"y": out}

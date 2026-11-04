def predict(probe):
    # f(x) = x^2 + 100 for x >= 0  [E2: 0->106, 1->217, 2->329, 3->440, 5->663,
    #   7->886, 10->1220, 15->1777, 25->2892, 45->5120, 60->6792; all = x^2+~100]
    # f(x) = x^2 + 100 for x < 0 too? Check E2 negatives:
    #   -1 -> 6.85, but (-1)^2+100=101. NO. Negatives are ~x^2 - something.
    #   -0.5 -> 50.3, -1 -> 6.85, -2 -> 26.7, -3 -> 52.8, -5 -> 104.9,
    #   -7 -> 157.1, -10 -> 235.3, -15 -> 365.6
    #   These look like x^2 + 100 shifted? -10: 100+100=200 vs 235. Hmm.
    #   Try (|x|-10)^2? -10->0 no.
    #   Try x^2 + 100 + 10*x? -10: 100+100-100=100 no.
    #   Look at differences: -15:365.6, -10:235.3 diff 130 over 5; 
    #   -7:157.1, -5:104.9; -3:52.8,-2:26.7,-1:6.85,-0.5:50.3
    #   Wait -0.5 -> 50.3 is HIGHER than -1 -> 6.85. Non-monotonic near 0!
    #   -1:6.85, -0.5:50.3, 0:106. So it's increasing through 0.
    #   For x<0: looks like (x+something)^2? -1:6.85 ~ (x+? )... 
    #   Try x^2 + 100 + 10*x for x<0: -1:1+100-10=91 no.
    #   Try (x-? )... Let's fit negatives as a*x^2+b*x+c.
    #   Use -15:365.6, -10:235.3, -5:104.9
    #   225a-15b+c=365.6; 100a-10b+c=235.3; 25a-5b+c=104.9
    #   diff1: 125a-5b=130.3; diff2: 75a-5b=130.4 -> 50a=-0.1 -> a~0
    #   So linear on negatives?! b: 125*0-5b=130.3 -> b=-26.06
    #   c from -5: 0+130.3+c=104.9 -> c=-25.4
    #   Check -1: 0+26.06-25.4=0.66 vs 6.85. Not great. -2: 52.1-25.4=26.7 YES
    #   -3: 78.2-25.4=52.8 YES. -7: 182.4-25.4=157.0 YES. -0.5:13-25.4=-12 no.
    #   So for x <= -1: y = -26*x - 25.4 approx? But -0.5 and 0 break it.
    #   Actually maybe it's x^2+100 for x>=0 and linear for very negative,
    #   with a transition. But -1:6.85 fits linear (-26*-1-25.4=0.6, off by 6).
    #   Hmm -1 is 6.85. Let's reconsider: maybe piecewise with kink near 0.
    #   For x>=0: x^2+100 exactly (0:106, 1:217, 2:329... 106=0+106? 
    #     actually 0^2+106=106, 1+106=107 no it's 217. 1^2+? =217 -> +216? 
    #     Wait 1->217.48, 2->328.9, 3->440.3. Diffs: 111.4, 111.4. Linear!
    #     So x>=0 is LINEAR: slope ~111.4, intercept 106. 0:106, 1:217.5 yes.
    #     5:106+557=663 yes. 10:106+1114=1220 yes. 60:106+6684=6790 yes!
    #   So x>=0: y = 111.4*x + 106.
    #   x<0: from -1:6.85,-2:26.7,-3:52.8,-5:104.9,-7:157.1,-10:235.3,-15:365.6
    #     diffs per unit: -1 to -2: 19.85; -2 to -3: 26.1; -3 to -5: 52.1/2=26;
    #     -5 to -7: 52.2/2=26.1; -7 to -10: 78.2/3=26.1; -10 to -15: 130.3/5=26.06
    #     So slope ~ -26.1 (as x decreases, y increases). y = -26.1*x + c.
    #     -10: 261+c=235.3 -> c=-25.7. -1: 26.1-25.7=0.4 vs 6.85. off.
    #     -0.5: 13.05-25.7=-12.6 vs 50.3. Way off.
    #   So near 0 (between -1 and 0) there's a kink/transition.
    #   -0.5 -> 50.3. Linear x>=0 would give 111.4*-0.5+106=50.3! YES!
    #   So the x>=0 line extends to x=-0.5. And -1 -> 6.85: linear gives 111.4*-1+106=-5.4, no.
    #   So boundary between -1 and -0.5. At x=-0.5 it's on the positive branch.
    #   Let's say: for x >= -0.5 (or some threshold), y = 111.4*x+106.
    #   For x <= -1, y = -26.1*x - 25.7.
    #   Check E1: 88.9 -> 111.4*88.9+106=9902+106=10008 vs 10012 close.
    #     67.5->7520+106=7626 vs 7627 YES. 38.8->4322+106=4428 vs 4429 YES.
    #     73.9->8233+106=8339 vs 8341 YES.
    #   Negatives E1: -93.6 -> -26.1*-93.6-25.7=2443-25.7=2417 vs 2414.9 close.
    #     -62.7->1636-25.7=1610 vs 1609 YES. -104->2714-25.7=2689 vs 2686 close.
    #     -120.7->3150-25.7=3124 vs 3121 close.
    #   Great. Refine constants.
    # Positive slope: (217.48-106.05)/1 = 111.43; use points 0 and 60:
    #   (6791.72-106.05)/60 = 111.428. intercept 106.05.
    # Negative: slope from -10,-15: (365.63-235.27)/(-15+10)=130.36/-5=-26.07
    #   intercept: 235.27 - (-26.07*-10)=235.27-260.7=-25.43
    # Threshold: where do branches meet? 111.43x+106.05 = -26.07x-25.43
    #   137.5x = -131.48 -> x=-0.956. So kink near x=-0.96.
    #   -1 is just below kink -> negative branch: -26.07*-1-25.43=0.64 vs 6.85. off by 6.
    #   Hmm. Maybe threshold is exactly -1 and there's a jump, or my fit is off.
    #   Let's just use: x >= -0.75 -> positive line; else negative line. (?) 
    #   Actually -1:6.85. Positive line at -1: -5.4. Negative line at -1: 0.64.
    #   Neither matches 6.85 well. There may be a smooth transition (MLP).
    #   Best guess: two linear regimes with a kink around x=-0.9.
    import math
    out=[]
    for x in probe["x"]:
        if x >= -0.9:
            y = 111.43*x + 106.05
        else:
            y = -26.07*x - 25.43
        out.append(y)
    return {"y":out}

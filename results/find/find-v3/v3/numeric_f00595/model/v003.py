def predict(probe):
    # f(x) = round half up, then +1 for x>0, -1 for x<=0? Let's derive from data.
    # Positive x: E6 shows 58.8->59, 102.1->103, 0.2->1, 0.8->1, 1.01->2, 1.99->2
    #   => ceil(x) for positives (0.2->1, 0.8->1, 1.01->2, 1.99->2, 58.8->59)
    # E8 positives: 2.5->3, 2.01->3, 1.5->2, 1.49->2, 0.99->1, 0.01->1, 3.99->4, 4.01->5, 10.5->11, 0.5->1
    #   => ceil(x) for positives (2.5->3, 1.5->2, 0.5->1, 10.5->11, 4.01->5, 3.99->4)
    # E1: 88.2->89, 66.0->66? observed E1 not shown but model v2 got it ok with ceil+1... 
    #   Wait E1 [ok] with v2 which was ceil+1. But E6 contradicts ceil+1 (58.8->59 not 60).
    #   E1 must be consistent with ceil: 88.2->89 ok, 66.0->66? v2 gave 67. Hmm E1 marked ok.
    #   Let me recheck: E1 x=[88.2,66.0,-20.3,-61.7,2.9,-24.3,72.7,-50.4,-6.0,21.3]
    #   v2 (ceil+1 pos, floor-1 neg): 89,67,-22,-63,3,-26,73,-52,-7,22
    #   E1 marked [ok] means observed matches that. But E6 says 58.8->59=ceil not ceil+1.
    #   Contradiction! Unless E1 observed differs. E1 is [ok] for v2, so observed = v2 output.
    #   So 66.0->67, 2.9->3, 21.3->22, 88.2->89. That's ceil+1 for positives.
    #   But E6: 58.8->59, 102.1->103, 47.1->48, 28.4->29, 105.7->106, 119.5->120 = ceil.
    #   And 0.2->1, 0.8->1, 1.01->2, 1.99->2 = ceil.
    #   E5: 58.8->59, 102.1->103, 47.1->48, 28.4->29, 105.7->106, 119.5->120 = ceil.
    #   E7: 93.5->94, 78.1->79, 12.5->13, 56.2->57, 83.2->84, 43.0->44 = ceil.
    #   E8: all positive = ceil.
    #   So positives: ceil(x). But E1 says 66.0->67, 2.9->3(ceil=3 ok), 21.3->22(ceil=22 ok), 88.2->89(ceil=89 ok).
    #   66.0: ceil(66.0)=66 but E1 observed 67?? Only integer 66.0 differs.
    #   Hmm. Maybe E1 observed is actually ceil and v2 got 66.0 wrong but overall [ok]? No, [ok] means full match.
    #   Let me reconsider: maybe E1 observed: 89,67,... Actually maybe rule is ceil for non-integers, +1 for integers?
    #   66.0 integer -> 67. 2.9->3, 21.3->22, 88.2->89. Consistent with ceil for non-integer, x+1 for integer.
    #   Check E6: 1.01->2 (ceil), 1.99->2(ceil), 0.2->1,0.8->1. No integers tested there except none.
    #   E8: 2.01->3, 1.49->2, 0.99->1, 0.01->1, 3.99->4, 4.01->5, 10.5->11, 2.5->3, 1.5->2, 0.5->1. All ceil.
    #   E5: 43.0->44! integer -> +1. Yes! 43.0->44 = 43+1. ceil(43)=43. So integer gets +1.
    #   E7: 43.0->44 confirms integer +1.
    #   So positive: if integer, x+1; else ceil(x).
    #   Equivalently floor(x)+1 for all positives? floor(2.9)+1=3 ok, floor(88.2)+1=89 ok, floor(66)+1=67 ok, floor(43)+1=44 ok, floor(0.2)+1=1 ok, floor(1.99)+1=2 ok, floor(10.5)+1=11 ok, floor(2.5)+1=3 ok, floor(4.01)+1=5 ok, floor(3.99)+1=4 ok, floor(0.01)+1=1 ok, floor(0.99)+1=1 ok, floor(1.49)+1=2 ok, floor(1.5)+1=2 ok, floor(2.01)+1=3 ok, floor(0.5)+1=1 ok.
    #   YES! Positive: floor(x)+1. That's it.
    # Negative: E8: -0.01->-2, -0.99->-2, -1.49->-3, -1.5->-3, -2.01->-4, -2.5->-4, -3.99->-5, -4.01->-6, -10.5->-12, -0.5->-2
    #   floor(x)-1? floor(-0.01)=-1, -1-1=-2 ok. floor(-0.99)=-1,-2 ok. floor(-1.49)=-2,-3 ok. floor(-1.5)=-2,-3 ok. floor(-2.01)=-3,-4 ok. floor(-2.5)=-3,-4 ok. floor(-3.99)=-4,-5 ok. floor(-4.01)=-5,-6 ok. floor(-10.5)=-11,-12 ok. floor(-0.5)=-1,-2 ok.
    #   E2: -0.5->-2 ok, -0.1->-2 ok, -1.5->-3 ok, -3.2->-5? floor(-3.2)=-4,-5 ok. -100->-101 ok.
    #   E5: -48.6->-50? floor(-48.6)=-49,-50 ok. -7.1->-9? floor(-7.1)=-8,-9 ok. -102.2->-104? floor=-103,-104 ok. -16.9->-18? floor=-17,-18 ok.
    #   E7: -5.9->-7? floor=-6,-7 ok. -61.3->-63? floor=-62,-63 ok. -124.4->-126? floor=-125,-126 ok. -25.9->-27? floor=-26,-27 ok.
    #   E1: -20.3->-22? floor=-21,-22 ok. -61.7->-63? floor=-62,-63 ok. -24.3->-26? floor=-25,-26 ok. -50.4->-52? floor=-51,-52 ok. -6.0->-7? floor(-6)=-6,-7 ok.
    #   E4: -0.9->-2 ok, -0.1->-2 ok, -1.1->-3? floor=-2,-3 ok. -2.0->-3? floor(-2)=-2,-3 ok. -50.5->-52? floor=-51,-52 ok.
    #   So negative: floor(x)-1.
    # Zero: E4 0.0->-1. floor(0)-1=-1 ok. So x<=0: floor(x)-1.
    # Positive: floor(x)+1.
    import math
    out = []
    for x in probe["x"]:
        if x > 0:
            out.append(float(math.floor(x) + 1))
        else:
            out.append(float(math.floor(x) - 1))
    return {"y": out}

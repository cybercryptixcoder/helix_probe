import math

def predict(probe):
    # A: negative side, x <= -5.1, y = -0.7*x  [E1, E2, E3, E5, E6: -5.1->3.57? no...]
    #   E6: -5.4,-5.3,-5.2,-5.1 all give 4.2 = -0.7*(-6)? No, -0.7*-5.4=3.78.
    #   Observed 4.2 for -5.4,-5.3,-5.2,-5.1. That's constant 4.2, not -0.7*x!
    #   Hmm. -0.7*-6=4.2. So maybe y = -0.7*floor-ish? Or y=-0.7*(x rounded to -6)?
    #   E1: -6.0 -> 4.2 (= -0.7*-6). -20.3 -> 14.7 (= -0.7*-21). -24.3 -> 17.0? E1 has -24.3.
    #   E2: -100->70 (=-0.7*-100), -50->35, -10->7. Those are exact -0.7*x.
    #   E3: -55.8->39.2 (=-0.7*-56), -63.9->44.8 (=-0.7*-64).
    #   E5: -48.6->34.3 (=-0.7*-49), -102.2->72.1 (=-0.7*-103), -16.9->11.9 (=-0.7*-17).
    #   So negative side: y = -0.7 * round(x) (round half away? -20.3->-21? round(-20.3)=-20, but 14.7=-0.7*-21).
    #   Actually floor: floor(-20.3)=-21 -> 14.7 ✓. floor(-55.8)=-56 -> 39.2 ✓. floor(-63.9)=-64 ✓.
    #   floor(-48.6)=-49 -> 34.3 ✓. floor(-102.2)=-103 -> 72.1 ✓. floor(-16.9)=-17 -> 11.9 ✓.
    #   floor(-5.4)=-6 -> 4.2 ✓. floor(-5.1)=-6 -> 4.2 ✓. floor(-100)=-100 ✓. floor(-10)=-10 ✓.
    #   So negative regime: y = -0.7 * floor(x). Boundary: -5.05 gives middle, -5.1 gives 4.2.
    #   floor(-5.1)=-6, floor(-5.05)=-6 too. But -5.05 gave middle. So boundary is between -5.1 and -5.05.
    #   Maybe threshold x <= -5.1? Or floor-based? -5.05 floor=-6 would give 4.2 but observed middle.
    #   So it's a plain threshold: x <= -5.1 (approx) -> -0.7*floor(x). Let's say x < -5.05.
    # B: middle, -5.05 <= x < 18.5, y ≈ -402.4 (noisy)  [E2,E4,E6]
    #   E6: 18.1,18.3,18.5 middle; 18.7 -> -302.4.
    # C: positive, x >= 18.5 (approx), y = -16.8 * floor(x)? 
    #   E6: 18.7->-302.4 (=-16.8*18), 18.9->-302.4 (=-16.8*18), 19.0->-319.2(=-16.8*19),
    #   19.1->-319.2, 19.5->-319.2, 20->-336(=-16.8*20), 25->-420(=-16.8*25), 30->-504, 35->-588, 40->-672, 45->-756.
    #   So y = -16.8 * floor(x). Check E2: 50->-840=-16.8*50 ✓, 100->-1680 ✓.
    #   E3: 104.5->-1747.2=-16.8*104 ✓, 65.5->-1092=-16.8*65 ✓, 30.3->-504=-16.8*30 ✓,
    #       104.9->-1747.2=-16.8*104 ✓, 123.6->-2066.4=-16.8*123 ✓, 79.4->-1327.2=-16.8*79 ✓, 103->-1730.4=-16.8*103 ✓.
    #   E5: 58.8->-974.4=-16.8*58 ✓, 102.1->-1713.6=-16.8*102 ✓, 47.1->-789.6=-16.8*47 ✓,
    #       28.4->-470.4=-16.8*28 ✓, 105.7->-1764=-16.8*105 ✓, 119.5->-1999.2=-16.8*119 ✓.
    #   Great, positive: y = -16.8 * floor(x).
    # Boundary positive: 18.5 middle, 18.7 positive. floor(18.7)=18, floor(18.5)=18. 
    #   So threshold not floor-based; plain x threshold between 18.5 and 18.7. Say x >= 18.6.
    #   But wait: at 18.7, floor=18, gives -302.4. At 18.5 middle. So threshold ~18.6.
    #   Hmm but is it maybe x > 18.5? 18.5 gave middle. So x > 18.5 -> positive. 18.7>18.5 ✓.
    #   Let's use x > 18.5.
    # Negative boundary: -5.1 -> 4.2, -5.05 -> middle. So x <= -5.1? Or x < -5.05.
    #   floor(-5.1)=-6 -> 4.2. floor(-5.05)=-6 too but middle. So plain threshold x <= -5.1.
    #   Actually maybe threshold is x <= -5.1 exactly? -5.1 gave 4.2. Let's use x <= -5.1.
    #   Hmm, but could be x < -5.05. Both fit. Use x <= -5.1.
    out = []
    for x in probe["x"]:
        if x <= -5.1:
            y = -0.7 * math.floor(x)
        elif x > 18.5:
            y = -16.8 * math.floor(x)
        else:
            y = -402.4
        out.append(y)
    return {"y": out}

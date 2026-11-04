def predict(probe):
    # Model of f(x):
    # Left region x < 0: f(x) = -0.7 * x  [E2: -120->84, -10->7; E1: -6->4.2]
    #   E1 left values slightly high (~0.5) but E2 exact; treat as noise/rounding.
    # Flat region 0 <= x < 19: f(x) ~ -402.3 (noisy)  [E4: -2..18 all ~-402.3]
    #   E4 shows flat region extends to x=18 (=-402.4158) and x=19 is -319.2.
    # Right region x >= 19: f(x) = -16.8 * x  [E2: 20->-336, 30->-504 ... 100->-1680]
    #   E4: 19->-319.2 = -16.8*19 exactly; 19.5->-319.2 (same as 19, odd - maybe floor/step?)
    #   E4: 20->-336, 20.5->-336 (same as 20), 21->-352.8, 22->-369.6, 25->-420.
    #   Note 19.5 and 20.5 give same as 19 and 20 -> suggests integer step in right region?
    #   But E3: 30.3->-504 = -16.8*30 exactly (not 30.3). 65.5->-1092=-16.8*65.
    #   E3: 104.5->-1747.2=-16.8*104. 79.4->-1327.2=-16.8*79. 123.6->-2066.4=-16.8*123.
    #   So right region: f(x) = -16.8 * floor(x)  [E3, E4]
    #   Check E1: 21.3->-352.8=-16.8*21 (floor 21.3=21). 66->-1108.8=-16.8*66. 
    #     72.7->-1209.6=-16.8*72 (floor 72.7=72). 88.2->-1478.4=-16.8*88 (floor 88.2=88). Yes!
    # Flat region: 0 <= x < 19, value ~-402.3 (noisy).
    #   E4: x=19 -> -319.2 = -16.8*19, so boundary at 19.
    #   Left boundary: E4 x=-0.5 -> -402.3083 (flat), x=-1 -> -402.4356 (flat!).
    #   Wait E4: -2->-402.2307, -1->-402.4356, -0.5->-402.3083 all flat.
    #   So flat region extends into negatives! Left boundary is below -2.
    #   E1: -6->4.2 = -0.7*-6 (left line). So boundary between -6 and -2.
    #   E2: -10->7 (left line). So left boundary in (-6, -2]. Guess -3? Unknown.
    #   Hmm, need boundary. E4 doesn't pin it. Use -3 as guess? Mark uncertain.
    #   Actually check: is flat region maybe x in [-3, 19)? Left boundary unknown between -6 and -2.
    #   Let's guess left boundary at -3 (midpoint-ish). Mark with ?.
    import math
    out = []
    for x in probe.get("x", []):
        try:
            if x < -3:
                y = -0.7 * x
            elif x < 19:
                y = -402.3
            else:
                y = -16.8 * math.floor(x)
        except Exception:
            y = None
        out.append(y)
    return {"y": out}

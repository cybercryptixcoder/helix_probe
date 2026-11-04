def predict(probe):
    # Piecewise function with three regions:
    # Region 1: x <= -10 -> linear: y = -0.7*x  [E2: -40->28, -30->21, -20->14, -10->7]
    # Region 2: -10 < x < 20 -> constant ~ -402.2 (noisy) [E2: -5..10 all ~-402.2..-402.33]
    # Region 3: x >= 20 -> linear: y = -16.8*x  [E2: 20->-336, 30->-504, 40->-672, 60->-1008, 80->-1344, 100->-1680, 120->-2016, 128->-2150.4]
    # E1 check: 88.2->-1478.4 (=-16.8*88.2 ✓), 66->-1108.8 (✓), -20.3->14.7 (=-0.7*-20.3=14.21? close-ish, noisy), -61.7->43.4 (=-0.7*-61.7=43.19 ✓), 2.9->-402.122 (region2 ✓), -24.3->17.5 (=-0.7*-24.3=17.01, noisy), 72.7->-1209.6 (=-16.8*72.7=-1221.36? off... let me recheck)
    # Recheck E1: 72.7 -> -1209.6. -16.8*72.7 = -1221.36. Not matching. Hmm.
    # Actually -1209.6/72.7 = -16.63... Let's check slope from E2: 20->-336, 128->-2150.4. slope=(-2150.4+336)/(128-20)=-1814.4/108=-16.8. intercept: -336-(-16.8*20)=-336+336=0. So y=-16.8x.
    # 72.7*-16.8=-1221.36 but observed -1209.6. Discrepancy. Maybe noise? -1209.6 vs -1221.36 is ~1% off.
    # 66*-16.8=-1108.8 exact. 88.2*-16.8=-1481.76 vs -1478.4, ~0.2% off.
    # So region3 has some noise (~1%).
    # Region1: -61.7*-0.7=43.19 vs 43.4; -24.3*-0.7=17.01 vs 17.5; -20.3*-0.7=14.21 vs 14.7. Noise ~2%.
    # Region2: constant ~-402.2 with noise ~0.1.
    import math
    xs = probe["x"]
    ys = []
    for x in xs:
        if x <= -10:
            ys.append(-0.7 * x)
        elif x < 20:
            ys.append(-402.2)
        else:
            ys.append(-16.8 * x)
    return {"y": ys}

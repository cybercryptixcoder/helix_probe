import math

def predict(probe):
    # Model hypotheses from evidence:
    # E1: for |x| large-ish (e.g. 88.2, 66, -61.7, 72.7, -50.4, 21.3) y is negative and ~ -16.8*x
    #     e.g. 88.2 -> -1478.4 (= -16.76*x), 66 -> -1108.8 (= -16.8*x), -61.7 -> 43.4? no...
    # E1 details:
    #   88.2 -> -1478.4  ratio -16.76
    #   66.0 -> -1108.8  ratio -16.8
    #   -20.3 -> 14.7    ratio -0.724
    #   -61.7 -> 43.4    ratio -0.703
    #   2.9 -> -402.2429  (near -402)
    #   -24.3 -> 17.5    ratio -0.72
    #   72.7 -> -1209.6  ratio -16.64
    #   -50.4 -> 35.7    ratio -0.708
    #   -6.0 -> 4.2      ratio -0.7
    #   21.3 -> -352.8   ratio -16.56
    # E2:
    #   -100 -> 70    ratio -0.7
    #   -50 -> 35     ratio -0.7
    #   -10 -> 7      ratio -0.7
    #   -1 -> -402.4487  (near -402)
    #   0 -> -402.3624   (near -402)
    #   1 -> -402.2633   (near -402)
    #   10 -> -402.5044  (near -402)
    #   50 -> -840    ratio -16.8
    #   100 -> -1680  ratio -16.8
    #
    # Pattern: there appear to be two linear regimes plus a constant-ish middle.
    # For x <= -10 (negative side): y = -0.7*x  (E2: -100->70, -50->35, -10->7; E1: -20.3->14.7, -24.3->17.5, -50.4->35.7, -6.0->4.2? -6 gives 4.2 = -0.7*-6 yes)
    #   Wait -6 -> 4.2 matches -0.7*x. So negative side rule y=-0.7x holds for x<=-6 at least.
    # For x >= ~21 (positive side): y = -16.8*x (E1: 88.2, 66, 72.7, 21.3; E2: 50, 100)
    # Middle region: y ≈ -402.4 (E2: -1,0,1,10; E1: 2.9 -> -402.2429)
    #
    # So there's a middle interval where y is roughly constant ~ -402.4.
    # Need boundaries. E2 shows x=10 -> -402.5 (middle), x=50 -> -840 (positive regime).
    # E1 shows x=21.3 -> -352.8 which is -16.56*21.3, so positive regime at 21.3.
    # Negative side: x=-6 -> 4.2 (negative regime), x=-1 -> -402.4 (middle). Boundary between -6 and -1.
    # Positive side: x=10 middle, x=21.3 positive regime. Boundary between 10 and 21.3.
    #
    # Middle constant: values -402.4487, -402.3624, -402.2633, -402.5044, -402.2429. Slight variation/noise.
    # Maybe middle is y = -402.4 + small noise, or maybe it's a specific function. Let's guess constant -402.4.
    #
    # Actually maybe the middle is y = -402.4 exactly-ish with noise. Use -402.4.
    #
    # Boundaries: guess symmetric-ish? Negative boundary between -6 and -1, positive between 10 and 21.3.
    # Could be |x| < some threshold. But -6 is negative regime while 10 is middle, so not symmetric.
    # Let's guess boundaries: negative regime for x < -5, middle for -5 <= x < 15, positive for x >= 15? 
    # Check: -6 < -5 -> negative regime, y=-0.7*-6=4.2 ✓. -1 in middle ✓. 10 in middle ✓. 21.3 >=15 positive ✓.
    # 50,100 positive ✓. 2.9 middle ✓.
    # Boundary guesses: -5 and 15 (uncertain, mark ?).
    #
    # Slopes: negative side -0.7 exactly (70/100=0.7, 35/50=0.7, 7/10=0.7, 14.7/20.3=0.724?, 17.5/24.3=0.72, 35.7/50.4=0.708, 4.2/6=0.7)
    #   Hmm -20.3 -> 14.7 gives 0.724, not 0.7. -24.3->17.5 gives 0.720. -50.4->35.7 gives 0.708.
    #   Maybe there's noise, or slope slightly different. -0.7 gives -20.3->14.21 vs 14.7. Close-ish.
    #   Could be noise. Use -0.7.
    # Positive side: -16.8 (66->-1108.8 exact, 50->-840 exact, 100->-1680 exact, 88.2->-1478.4 = -16.76, 72.7->-1209.6=-16.64, 21.3->-352.8=-16.56)
    #   Slight variation, likely noise. Use -16.8.
    #
    # Middle: -402.4 constant (noise).
    #
    # Let's write it.
    out = []
    for x in probe["x"]:
        if x < -5:
            y = -0.7 * x
        elif x < 15:
            y = -402.4
        else:
            y = -16.8 * x
        out.append(y)
    return {"y": out}

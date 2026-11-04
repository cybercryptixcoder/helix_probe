import math

def predict(probe):
    # Observations:
    # - For x in [-40,-30,-20,-10]: y = -0.7*x  (28,21,14,7) [E2]
    # - For x in [-5,-2,-1,-0.5,0,0.5,1,2,5,10]: y ≈ -402.3 (roughly constant, noisy) [E2]
    # - For x in [20,30,40,60,80,100]: y = -16.8*x (-336,-504,-672,-1008,-1344,-1680) [E2]
    # - E1: x=88.2 -> -1478.4 = -16.76*88.2 ; x=66 -> -1108.8 = -16.8*66 ; x=72.7 -> -1209.6 = -16.64*72.7
    #   x=-20.3 -> 14.7 ≈ -0.72*(-20.3) ; x=-61.7 -> 43.4 ≈ -0.70*(-61.7) ; x=-50.4 -> 35.7 ≈ -0.71*(-50.4)
    #   x=2.9 -> -402.2448 ; x=-24.3 -> 17.5 ≈ -0.72*(-24.3) ; x=-6.0 -> 4.2 ≈ -0.7*(-6.0) ; x=21.3 -> -352.8 = -16.56*21.3
    # So: three regions:
    #   x <= -10 (or so): y ≈ -0.7*x
    #   middle region: y ≈ -402.3 (constant, noisy)
    #   x >= 20 (or so): y ≈ -16.8*x
    # Boundaries: between -10 and -5 the linear -0.7x would give 3.5 and 7; observed -402. So break between -10 and -5.
    #   Between 10 and 20: -16.8*10=-168 but observed -402; -16.8*20=-336 matches. Break between 10 and 20.
    # E1: x=-6.0 -> 4.2 = -0.7*(-6) so -6 is in linear region! But E2 x=-5 -> -402.24. So break between -6 and -5.
    #   E1 x=2.9 -> -402.24 (middle). E1 x=21.3 -> -352.8 = -16.56*21.3 (linear). E2 x=20 -> -336 matches -16.8*20.
    #   So right break between 10 and 20; E1 x=21.3 in linear. Need finer: E2 x=10 -> -402.177 (middle), x=20 -> -336 (linear).
    # Left break: between -6 and -5 (E1 x=-6 linear, E2 x=-5 middle).
    # Middle value: ~-402.3 with noise. Use -402.3.
    # Slopes: left -0.7, right -16.8. Check E1: -0.7*88.2=-61.74 no! Wait 88.2 -> -1478.4, that's -16.76*88.2. Right slope ~-16.8.
    #   E1 x=66 -> -1108.8 / 66 = -16.8. x=72.7 -> -1209.6/72.7 = -16.64. x=21.3 -> -352.8/21.3=-16.56.
    #   Hmm right slope maybe -16.8 exactly for some, but 21.3 gives -16.56. Noise? E2 exact: -16.8.
    #   Use -16.8.
    # Left slope: E2 exact -0.7. E1: -20.3->14.7 => -0.724; -61.7->43.4 => -0.703; -50.4->35.7=>-0.708; -24.3->17.5=>-0.720; -6.0->4.2=>-0.7.
    #   Use -0.7 (E2 exact, E1 noisy).
    # Middle: E2 values around -402.3 (range -402.18 to -402.51). E1 x=2.9 -> -402.2448. Use -402.3.
    # Boundaries uncertain: left between -6 and -5; right between 10 and 20. Guess left=-5.5, right=15? 
    #   E1 x=21.3 linear, E2 x=20 linear, x=10 middle. So right boundary in (10,20]. Guess 15.
    #   Left: x=-6 linear, x=-5 middle. Boundary in (-6,-5]. Guess -5.5.
    # "?" boundaries approximate.
    out = []
    for x in probe.get("x", []):
        try:
            if x <= -5.5:
                out.append(-0.7 * x)
            elif x < 15:
                out.append(-402.3)
            else:
                out.append(-16.8 * x)
        except Exception:
            out.append(None)
    return {"y": out}

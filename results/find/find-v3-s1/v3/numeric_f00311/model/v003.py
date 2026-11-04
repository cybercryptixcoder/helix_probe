def predict(probe):
    # Rules (evidence):
    # For x >= 0: y = 8 - 9.6*x exactly [E2, E4: 0->8, 1->-1.6, 25->-232, 125->-1192]
    # For x < 0: y = 8 + 9.6*x exactly [E4: -0.5->12.8, -5->56; E1: -1.2->-3.52? no...]
    #   Wait: E4 -0.5->12.8 = 8+9.6*0.5 ✓; -5->56 = 8+9.6*5 ✓
    #   But E1 -1.2->19.52 = 8+9.6*1.2 = 19.52 ✓ !! (not an outlier after all)
    #   E1 -12.9->8.1319, -62.7->8.0343, -93.6->7.8956, -104->7.9716, -120.7->8.0586
    #   These are ~8, NOT 8+9.6|x|. So negative side is NOT simply 8+9.6x.
    #   E4 -5->56 fits 8+9.6*5; E1 -12.9->8.13 does not (would be 131.8).
    #   Hmm. Maybe |x| small negative uses 8+9.6|x|, large negative uses ~8?
    #   E4 -0.5->12.8, -5->56 both fit 8+9.6|x|. E1 -1.2->19.52 fits 8+9.6*1.2.
    #   E1 -12.9->8.13: 8+9.6*12.9=131.8, no. So threshold between 5 and 12.9 on negative side.
    #   Actually maybe it's y = 8 - 9.6*x for x in [-5, ...]? -5: 8+48=56 ✓, -1.2: 19.52 ✓,
    #   -0.5: 12.8 ✓. And for x < -5ish, y ~ 8 (baseline).
    #   Check E1 -12.9->8.13 (baseline), -62.7->8.03, -93.6->7.90, -104->7.97, -120.7->8.06.
    #   So: x >= -5 (approx): y = 8 - 9.6*x ; x < -5: y ≈ 8.
    #   But E2 -30->8.07, -50->8.15, -80->7.98 confirm baseline for x<-5.
    #   Where exactly is the negative threshold? Between -5 (linear) and -12.9 (flat).
    #   E1 -1.2 linear. Need boundary; guess -8? Unknown. Mark "?".
    #   Positive side: all positive x linear 8-9.6x, including small (E4 0.25->5.6=8-2.4 ✓).
    #   So positive threshold is x>=0 (0->8 fits both). 
    #   Negative: linear for x in [T,0), flat ~8 for x<T, T between -12.9 and -5.
    #   Guess T=-8? Actually could be -10. Use -8 as midpoint guess "?".
    out = []
    for x in probe["x"]:
        if x >= 0:
            y = 8 - 9.6 * x
        elif x >= -8:   # ? boundary between -12.9 (flat) and -5 (linear)
            y = 8 - 9.6 * x
        else:
            y = 8.0
        out.append(round(y, 4))
    return {"y": out}

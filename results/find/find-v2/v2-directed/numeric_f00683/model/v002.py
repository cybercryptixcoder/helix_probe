def predict(probe):
    # Positive side, x >= ~0.5: f(x) = 13x - 3 [E6,E7,E8,E9]
    #   E9: 0.9->8.29 (13*.9-3=8.7), 1.1->8.91 (11.3), 2.2->23.32 (25.6),
    #   4.2->49.52 (51.6), 10->129.5 (127), 17->218.2 (218). Slope ~13, intercept ~-3.
    #   E8: 1.5->16.15 (16.5), 5->61 (62), 25->323 (322), 40->518.5 (517). Good.
    #   E6: 24->309.9 (309), 16->204.1 (205). Good.
    # Small positive x (0 < x < ~0.5): anomaly, roughly constant ~ -3 to -4 [E6,E7,E8]
    #   0.05->-2.845/-3.845, 0.1->-4.19, 0.2->-0.88/-2.88, 0.3->-1.57/-0.57,
    #   0.4->-0.26/1.74, 0.5->2.05/3.05. Noisy; ramps up from ~-4 to ~+2.
    #   Model as linear ramp from (0, -4) to (0.5, 2): slope 12, intercept -4.
    #   Actually 13x-3 at x=0.5 gives 3.5; observed 2-3. Use ramp 12x-4 for 0<x<0.5.
    # Negative side: f(x) = 1.31x - 10 approx [E2,E3,E4,E5]
    #   E4: -128->-178.58 (1.31*-128-10=-177.7), -96->-136.66 (-135.8),
    #   -48->-71.78 (-72.9), -24->-41.34 (-41.4), -12->-25.62 (-25.7). Good.
    #   E2: -3->-14.83 (-13.93), -2->-13.52 (-12.62), -1->-11.21 (-11.31). Noisy.
    #   E5 dense: noisy around 1.31x-10 with ±2 scatter. Use 1.31x-10.
    # x == 0: spike to ~ -385 [E1,E2,E4]
    out = []
    for x in probe["x"]:
        try:
            if x == 0:
                out.append(-385.12)
            elif x > 0:
                if x < 0.5:
                    out.append(12.0*x - 4.0)
                else:
                    out.append(13.0*x - 3.0)
            else:
                out.append(1.31*x - 10.0)
        except Exception:
            out.append(None)
    return {"y": out}

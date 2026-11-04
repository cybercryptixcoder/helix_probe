def predict(probe):
    # Positive side, x >= 0.5: f(x) = 12.55x + 0.05 [E7,E8,E9]
    #   E8: 0.5->3.05, 1->7.6, 5->61, 40->518.5 (12.55*40+0.05=502.05? no)
    #   Check: 12.55*40=502 -> observed 518.5. Slope ~12.95. 13x-3: 517. 
    #   E9: 10->129.5 (13*10-3=127), 17->218.2 (218). Slope 13, intercept -3 fits.
    #   Use 13x-3 for x>=0.5.
    # Small positive x (0 < x < 0.5): noisy, roughly linear ramp [E6,E8,E12]
    #   E12 dense: values scatter around a line. Fit: at 0.02->-4.24, 0.48->0.79.
    #   Slope ~ (0.79-(-4.24))/0.46 ~ 10.9, intercept ~ -4.5. Noisy ±1.
    #   Use 11x - 4.5 for 0<x<0.5.
    # Negative side: f(x) = 1.31x - 10 approx [E4,E10,E11]
    #   E10: -128->-176.58 (1.31*-128-10=-177.7), -8->-19.38 (-20.48).
    #   E11: -120->-167.1 (1.31*-120-10=-167.2). Good.
    # x == 0: spike ~ -382 to -385 [E1,E2,E4,E10]
    out = []
    for x in probe["x"]:
        try:
            if x == 0:
                out.append(-383.0)
            elif x > 0:
                if x < 0.5:
                    out.append(11.0*x - 4.5)
                else:
                    out.append(13.0*x - 3.0)
            else:
                out.append(1.31*x - 10.0)
        except Exception:
            out.append(None)
    return {"y": out}

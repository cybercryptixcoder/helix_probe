import math

def predict(probe):
    # Positive side, x >= ~0.5: f(x) = 13x - 3, clean [E21,E22,E9,E8]
    #   E22: 0.5->2.05, 1->8.6, 2->20.7, 5->60, 10->126.5, 36->468.1. 13x-3 fits.
    # Small positive x (0 < x < ~0.5): noisy/oscillatory, NOT the 13x-3 line [E12,E19,E20,E23]
    #   E23 dense: values scatter widely, e.g. 0.01->-5.37, 0.06->-4.71, 0.33->2.82, 0.42->3.00.
    #   Mean trend roughly rises from ~-4 to ~+1 over 0..0.5. Use 10x - 4 with noise.
    #   The transition to clean line seems to happen around x~0.5-0.6 [E20: 0.5->5.05, 0.6->3.36 noisy].
    # Negative side: f(x) = 1.31x - 10 plus noise [E10,E11,E13,E14,E16,E17,E18]
    #   E13/E14/E16/E17/E18 show scatter ±1-2 around the line, no clean periodicity found.
    #   Use 1.31x - 10 with noise.
    # x == 0: spike ~ -382 to -385 [E1,E2,E4,E10]
    out = []
    for x in probe["x"]:
        try:
            if x == 0:
                out.append(-383.0)
            elif x > 0:
                if x < 0.5:
                    out.append(10.0*x - 4.0)
                else:
                    out.append(13.0*x - 3.0)
            else:
                out.append(1.31*x - 10.0)
        except Exception:
            out.append(None)
    return {"y": out}

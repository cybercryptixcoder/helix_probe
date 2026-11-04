def predict(probe):
    # Baseline: rises ~linearly with |x|, slope ~0.0004 [E1-E12]
    # Positive bump near x~-6 (peak ~0.047) [E1,E3,E4,E8]
    # Sharp positive spike just left of 0 (x~-1.6 -> 0.078) [E5]
    # Negative dip near x~1-2 (1.2->-0.0895, 2.0->-0.0595, 2.9->-0.0469) [E1,E2,E6]
    # Negative dip near x~10-13 (10.3->-0.0243, 10.4->-0.0241, 12.1->-0.0206,
    #   12.5->-0.0198, 13.1->-0.0185) [E4,E6,E7,E9]
    # Negative dip near x~17 (17.3->-0.0099) [E5]
    # Mid positive x (19-30): small negative values, ~0 or slightly below [E1,E2,E7,E9,E10,E12]
    #   e.g. 21.3->-0.0017, 22.4->-0.0005, 23.0->-0.0002, 28.4->0.0027, 30.3->0.0037
    #   but 18.9->-0.0066, 20.4->-0.0035, 27.2->0.002, 34.6->0.006 [E10,E12]
    # Small negative dip near x~8-9 (8.8->-0.0274) [E12]
    import math
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            ax = abs(x)
            v = 0.0004 * ax
            # positive bump near x ~ -6
            v += 0.045 * math.exp(-((x + 6.0) ** 2) / 8.0)
            # sharp positive spike just left of 0
            v += 0.080 * math.exp(-((x + 1.6) ** 2) / 2.0)
            # deep negative dip near x ~ 1.5
            v -= 0.095 * math.exp(-((x - 1.5) ** 2) / 4.0)
            # negative dip near x ~ 8.8
            v -= 0.030 * math.exp(-((x - 8.8) ** 2) / 4.0)
            # negative dip near x ~ 11
            v -= 0.028 * math.exp(-((x - 11.0) ** 2) / 8.0)
            # negative dip near x ~ 17
            v -= 0.015 * math.exp(-((x - 17.0) ** 2) / 6.0)
            # broad shallow negative trough across mid positive x (18-30)
            v -= 0.008 * math.exp(-((x - 22.0) ** 2) / 60.0)
            out.append(round(v, 4))
        except Exception:
            out.append(None)
    return {"y": out}

import math

def predict(probe):
    # Beliefs (v9):
    # - Main positive bump: peak ~0.28 near x=0.4, asymmetric.
    #   Positive side sigma^2~3.0: x=1.2->0.23, x=2.0->0.12, x=2.9->0.036 [E2,E6,E1]
    #   Negative side sigma^2~3.5: x=-1.6->0.092 [E5]
    # - Negative-side baseline: -0.0044*tanh(|x|/60), saturates ~-0.0044 at -128 [E5,E6,E3,E11,E12,E8,E13]
    # - Positive-side baseline: shallow plateau ~-0.0004 from x~22 to ~65, fading to 0 at 128 [E7,E11,E12,E4,E9,E2,E8]
    # - Negative dip centered ~12.5, depth ~-0.006, sigma^2~30 [E6,E4,E9,E7,E12,E5,E10,E1]
    # - Small positive bump near x=-3.5: E10 x=-3.5 -> 0.0066 (was treated as tail of main bump; too far).
    #   Fit: center ~-3.5, height ~0.0066, sigma^2~2.0. Check E4 x=-5.9 -> 0.0003 (obs 0.0003).
    #   E8 x=-6.0 -> 0.0 (obs 0.0). E1 x=-6.0 -> 0.0 (obs 0.0). Good.
    # - E13: x=19.4->-0.0017 (dip tail ok), x=-27.9->-0.0019, x=-33.2->-0.0024,
    #   x=-80.6->-0.0035, x=-96.3->-0.0038, x=-74.1->-0.0034, x=118->-0.0001, x=123->-0.0001.
    #   Negative baseline at -27.9: tanh(0.465)=0.434 -> -0.0019 (obs -0.0019). 
    #   At -33.2: tanh(0.553)=0.503 -> -0.0022 (obs -0.0024). Slightly low; use /55.
    #   tanh(27.9/55)=tanh(0.507)=0.468 -> -0.0021 (obs -0.0019). /60 better for -27.9.
    #   At -33.2 /60: tanh(0.553)=0.503 -> -0.0022 (obs -0.0024). Use /58 compromise.
    #   At -80.6 /58: tanh(1.39)=0.884 -> -0.0039 (obs -0.0035). Hmm too high.
    #   At -96.3 /58: tanh(1.66)=0.930 -> -0.0041 (obs -0.0038).
    #   At -74.1 /58: tanh(1.28)=0.857 -> -0.0038 (obs -0.0034).
    #   Observed negative baseline seems to saturate around -0.0044 but slower. 
    #   Try -0.0044*tanh(|x|/70): -27.9: tanh(0.399)=0.379->-0.0017 (obs -0.0019)
    #   -33.2: tanh(0.474)=0.442->-0.0019 (obs -0.0024). Too low.
    #   The data is noisy; keep /60 but note E13 suggests slightly steeper at mid-range.
    #   Actually check E13 -33.2 obs -0.0024 vs /60 pred -0.0022: diff 0.0002. Fine.
    #   -80.6 obs -0.0035 vs /60 pred tanh(1.343)=0.873->-0.0038: diff 0.0003. Fine.
    #   Keep /60.
    xs = probe.get("x", []) if isinstance(probe, dict) else []
    ys = []
    for x in xs:
        try:
            x = float(x)
        except Exception:
            ys.append(None)
            continue
        try:
            # main positive bump, asymmetric width
            if x >= 0.4:
                bump = 0.28 * math.exp(-((x - 0.4) ** 2) / 3.0)
            else:
                bump = 0.28 * math.exp(-((x - 0.4) ** 2) / 3.5)
            # small positive bump near x=-3.5
            bump2 = 0.0066 * math.exp(-((x + 3.5) ** 2) / 2.0)
            # baseline
            if x < 0:
                base = -0.0044 * math.tanh(abs(x) / 60.0)
            else:
                if x <= 22.0:
                    base = -0.0004 * (x / 22.0)
                elif x <= 60.0:
                    base = -0.0004
                else:
                    base = -0.0004 * (128.0 - x) / 68.0
            # negative dip near x=12.5 (positive side only)
            if x > 0:
                dip = -0.0062 * math.exp(-((x - 12.5) ** 2) / 30.0)
            else:
                dip = 0.0
            ys.append(bump + bump2 + base + dip)
        except Exception:
            ys.append(None)
    return {"y": ys}

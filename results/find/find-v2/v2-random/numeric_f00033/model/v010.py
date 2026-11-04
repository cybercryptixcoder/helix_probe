import math

def predict(probe):
    # Beliefs (v10):
    # - Main positive bump: peak ~0.28 near x=0.4, asymmetric.
    #   Positive side sigma^2~3.0: x=1.2->0.23, x=2.0->0.12, x=2.9->0.036 [E2,E6,E1]
    #   Negative side sigma^2~3.5: x=-1.6->0.092 [E5]
    # - Negative-side baseline: -0.0044*tanh(|x|/60), saturates ~-0.0044 [E5,E6,E3,E11,E12,E8,E13]
    #   E13/E14/E16 confirm ~-0.0043 at |x|~120; /60 slightly low there but close.
    # - Positive-side baseline: shallow plateau ~-0.0004 from x~22 to ~65, fading to 0 at 128 [E7,E11,E12,E4,E9,E2,E8]
    # - Negative dip centered ~12.5, depth ~-0.006, sigma^2~30 [E6,E4,E9,E7,E12,E5,E10,E1]
    # - Small positive bump near x=-3.5: E10 x=-3.5 -> 0.0066. sigma^2~2.0.
    #   E16 x=-14.8 -> -0.0008: dip tail + baseline; bump2 negligible there. OK.
    # - E16 checks: x=44.2->-0.0004 (plateau ok), x=119.4->-0.0001 (fade ok),
    #   x=-113.1->-0.0042 (baseline tanh(1.885)=0.955->-0.0042 ok),
    #   x=-40.4->-0.003 (tanh(0.673)=0.587->-0.0026; obs -0.003, a bit low),
    #   x=-63.8->-0.0032 (tanh(1.063)=0.787->-0.0035; obs -0.0032, a bit high),
    #   x=-83.2->-0.0036 (tanh(1.387)=0.883->-0.0039; obs -0.0036, a bit high).
    #   Negative baseline seems to saturate slower / lower than -0.0044*tanh(|x|/60).
    #   Refit: at -40.4 obs -0.003, at -63.8 obs -0.0032, at -83.2 obs -0.0036,
    #   at -113.1 obs -0.0042, at -122 obs -0.0043. Use -0.0044*tanh(|x|/75):
    #   -40.4: tanh(0.539)=0.492->-0.0022 (too low). Hmm.
    #   Try -0.0045*tanh(|x|/50): -40.4: tanh(0.808)=0.668->-0.0030 ok;
    #   -63.8: tanh(1.276)=0.855->-0.0038 (obs -0.0032 too high).
    #   Data noisy; keep /60 but reduce amplitude slightly to -0.0043.
    xs = probe.get("x", []) if isinstance(probe, dict) else []
    ys = []
    for x in xs:
        try:
            x = float(x)
        except Exception:
            ys.append(None)
            continue
        try:
            if x >= 0.4:
                bump = 0.28 * math.exp(-((x - 0.4) ** 2) / 3.0)
            else:
                bump = 0.28 * math.exp(-((x - 0.4) ** 2) / 3.5)
            bump2 = 0.0066 * math.exp(-((x + 3.5) ** 2) / 2.0)
            if x < 0:
                base = -0.0043 * math.tanh(abs(x) / 60.0)
            else:
                if x <= 22.0:
                    base = -0.0004 * (x / 22.0)
                elif x <= 60.0:
                    base = -0.0004
                else:
                    base = -0.0004 * (128.0 - x) / 68.0
            if x > 0:
                dip = -0.0062 * math.exp(-((x - 12.5) ** 2) / 30.0)
            else:
                dip = 0.0
            ys.append(bump + bump2 + base + dip)
        except Exception:
            ys.append(None)
    return {"y": ys}

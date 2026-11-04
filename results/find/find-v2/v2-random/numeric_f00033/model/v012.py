import math

def predict(probe):
    # Beliefs (v12):
    # - Main positive bump: peak ~0.28 near x=0.4, asymmetric.
    #   Positive side sigma^2~3.0: x=1.2->0.23, x=2.0->0.12, x=2.9->0.036 [E2,E6,E1]
    #   Negative side sigma^2~3.5: x=-1.6->0.092 [E5]
    #   E21: x=-1.4->0.1218, x=-3.3->0.0072. Peak may be slightly left of 0.4.
    #   Refit: x=-1.4->0.1218, x=2.2->0.0941 [E17], x=0.9->? [E15].
    #   Try peak at 0.2, sigma^2~3.0 both sides: x=-1.4: exp(-2.56/3)=0.425->0.119 ok;
    #   x=2.2: exp(-4/3)=0.264->0.074 (obs 0.094, a bit low). Keep asymmetric.
    # - Negative-side baseline: -0.0044*tanh(|x|/60), saturates ~-0.0044 [E5,E6,E3,E11,E12,E8,E13]
    #   E13/E14/E16 confirm ~-0.0043 at |x|~120.
    # - Positive-side baseline: shallow plateau ~-0.0004 from x~22 to ~65, fading to 0 at 128 [E7,E11,E12,E4,E9,E2,E8]
    # - Negative dip centered ~13.5, depth ~-0.006, sigma^2~28 [E6,E4,E9,E7,E12,E5,E10,E1]
    #   E21: x=7.1->-0.0011 (dip+bump tail), x=15.7->-0.0039 (dip). 
    #   E17: x=15.5->-0.004, x=17.7->-0.0027. Dip center ~14, sigma^2~30.
    #   Refit dip: x=10.4->-0.0047 [E9], x=15.7->-0.0039, x=17.7->-0.0027,
    #   x=18.9->-0.002 [E12], x=19.4->-0.0017 [E13], x=20.4->-0.0011 [E10].
    #   Center ~13, sigma^2~25: x=10.4: exp(-6.76/25)=0.763->-0.0047 ok;
    #   x=15.7: exp(-7.29/25)=0.747->-0.0046 (obs -0.0039, a bit deep);
    #   x=17.7: exp(-22/25)=0.414->-0.0026 ok; x=20.4: exp(-54.8/25)=0.111->-0.0007 (obs -0.0011).
    #   Use center 13.5, sigma^2~28, depth -0.006.
    # - Small positive bump near x=-3.5: E10 x=-3.5 -> 0.0066. sigma^2~2.0.
    #   E21: x=-3.3->0.0072 (bump2 + main bump tail). Main bump at -3.3: exp(-12.25/3.5)=0.030->0.0085.
    #   That's too much; bump2 alone ~0.0066. So main bump negative side is narrower.
    #   Refit: x=-1.4->0.1218, x=-1.6->0.092 [E5], x=-3.3->0.0072 (minus bump2 ~0.0066 -> ~0.0006 from main).
    #   Main bump negative sigma^2~2.0: x=-1.4: exp(-2.56/2)=0.278->0.078 (obs 0.122 too low).
    #   Hmm. Maybe bump2 is wider/centered differently. E21 x=-3.3->0.0072, E10 x=-3.5->0.0066.
    #   Keep bump2 sigma^2~2.0 centered -3.5, and main bump negative sigma^2~3.0.
    #   x=-3.3: main exp(-12.25/3)=0.017->0.0048 + bump2 0.0065 = 0.0113 (obs 0.0072, a bit high).
    #   Reduce bump2 amplitude to 0.0055.
    # - E21: x=-14->-0.0007 (dip tail + baseline). x=-48.1->-0.0032 (baseline).
    #   x=-61.6->-0.0032, x=-87.6->-0.0037. Baseline tanh(|x|/60): -48.1: tanh(0.802)=0.665->-0.0029 ok;
    #   -61.6: tanh(1.027)=0.772->-0.0034 ok; -87.6: tanh(1.46)=0.898->-0.0039 ok.
    #   x=-14: tanh(0.233)=0.229->-0.001 + dip tail exp(-756/28)~0 = -0.001 (obs -0.0007, close).
    # - E23: x=-25.1->-0.0017, x=-47.1->-0.0032, x=-73.3->-0.0034, x=-103.0->-0.004,
    #   x=-97.6->-0.0039, x=-127.4->-0.0044. Baseline tanh(|x|/60) fits well.
    #   x=7.3->-0.0013 (dip tail: exp(-38/28)=0.26->-0.0016, close).
    #   x=82.6->-0.0002, x=45.7->-0.0004, x=55.6->-0.0004 (positive plateau ok).
    xs = probe.get("x", []) if isinstance(probe, dict) else []
    ys = []
    for x in xs:
        try:
            x = float(x)
        except Exception:
            ys.append(None)
            continue
        try:
            bump = 0.28 * math.exp(-((x - 0.4) ** 2) / 3.0)
            bump2 = 0.0055 * math.exp(-((x + 3.5) ** 2) / 2.0)
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
                dip = -0.006 * math.exp(-((x - 13.5) ** 2) / 28.0)
            else:
                dip = 0.0
            ys.append(bump + bump2 + base + dip)
        except Exception:
            ys.append(None)
    return {"y": ys}

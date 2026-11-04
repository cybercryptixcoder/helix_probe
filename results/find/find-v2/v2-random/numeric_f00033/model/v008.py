import math

def predict(probe):
    # Beliefs (revised):
    # - Main positive bump: peak ~0.23 near x=0.6, but MUCH narrower than v7.
    #   [E2 x=1.2->0.228, E6 x=2.0->0.12, E1 x=2.9->0.036, E5 x=-1.6->0.092]
    #   Fit Gaussian: at 1.2 ->0.228, at 2.0 ->0.12, at 2.9 ->0.036.
    #   ln(0.228/0.12)=0.64 over (2.0^2-1.2^2)=2.56 -> 1/(2s^2)=0.25 -> s^2=2.0? 
    #   Check 2.9: exp(-(2.3)^2/2.0)=exp(-2.65)=0.07 -> 0.228*0.07/0.94... use height 0.24.
    #   At -1.6: exp(-(2.2)^2/2.0)=exp(-2.42)=0.089 -> 0.24*0.089=0.021 (obs 0.092). Too low.
    #   So bump is asymmetric or wider on negative side. Try center 0.4, s^2=2.5:
    #   x=1.2: exp(-0.64/2.5)=0.77 ->0.185 (obs 0.228). x=2.0: exp(-2.56/2.5)=0.36->0.086 (obs 0.12).
    #   x=2.9: exp(-6.25/2.5)=0.082->0.020 (obs 0.036). x=-1.6: exp(-4/2.5)=0.20->0.048 (obs 0.092).
    #   Negative side clearly wider. Use asymmetric sigma: s^2=1.6 for x>0.4, s^2=5 for x<0.4.
    #   x=1.2: exp(-0.64/1.6)=0.67->0.16 (obs 0.228). Still low. height 0.28, s^2=2.0 pos:
    #   x=1.2: exp(-0.32)=0.73->0.20; x=2.0: exp(-1.28)=0.28->0.078; x=2.9: exp(-3.1)=0.045->0.013.
    #   Hmm obs 0.036 at 2.9. Wider. s^2=3.0 pos: x=1.2: exp(-0.21)=0.81->0.23; x=2.0: exp(-0.85)=0.43->0.12;
    #   x=2.9: exp(-2.08)=0.125->0.035. Good with height 0.28, center 0.4, s^2=3.0.
    #   Negative: x=-1.6 dist 2.0. obs 0.092. 0.28*exp(-4/s^2)=0.092 -> exp=0.33 -> 4/s^2=1.11 -> s^2=3.6.
    #   Use s^2=3.5 neg. x=-3.5 dist 3.9: 0.28*exp(-15.2/3.5)=0.28*0.013=0.0036 (obs 0.0066). close-ish.
    #   So the "bump2" at -3.5 is likely just the tail of the main bump. Drop bump2.
    # - Negative-side baseline: smooth ramp, ~0 near -5, saturating ~-0.0044 at -128.
    #   [E5 -127.7->-0.0044, E6 -107.4->-0.0041, E3 -102.2->-0.004, E11 -98->-0.0039,
    #    E12 -90.5->-0.0037, E8 -79.5->-0.0035, E11 -71.6->-0.0034, E5 -65.6->-0.0033,
    #    E2 -55.8->-0.0032, E3 -48.6->-0.0032, E11 -42.9->-0.0032, E7 -29.5->-0.0021,
    #    E1 -20.3->-0.0013, E6 -13.3->-0.0006, E3 -7.1->-0.0001]
    #   tanh(|x|/55): -20: tanh(0.36)=0.35->-0.0015 (obs -0.0013 ok); -45: tanh(0.82)=0.67->-0.0030 (obs -0.0032);
    #   -128: tanh(2.3)=0.98->-0.0043 ok. -13: tanh(0.24)=0.23->-0.0010 (obs -0.0006). Slightly high.
    #   Use tanh(|x|/60): -13: tanh(0.22)=0.21->-0.0009; -20: tanh(0.33)=0.32->-0.0014; -45: tanh(0.75)=0.63->-0.0028.
    #   Good enough.
    # - Positive-side baseline: shallow plateau ~-0.0004 from x~22 to ~65, fading to 0 at 128.
    #   [E7 26.4->-0.0004, E11 33.3->-0.0004, E12 27.2->-0.0004, E4 43->-0.0004, E9 52.6->-0.0004,
    #    E2 65.5->-0.0003, E8 65.9->-0.0003, E2 79.4->-0.0003, E9 89.5->-0.0002,
    #    E8 87.7->-0.0002, E9 101.1->-0.0001, E2 104.5->-0.0001, E10 127->0]
    #   Model: -0.0004 for 22<=x<=60, then linear fade to 0 at 128.
    # - Negative dip on positive side: centered ~12, depth ~-0.006, width sigma^2~35.
    #   [E6 12.1->-0.0061, E4 12.5->-0.0058, E6 13.1->-0.0055, E9 10.4->-0.0047,
    #    E7 10.3->-0.0046, E12 8.8->-0.003, E5 17.3->-0.0029, E12 18.9->-0.002,
    #    E7 19.4->-0.0017, E10 20.4->-0.0011, E1 21.3->-0.0005]
    #   center 12, s^2=30, depth -0.0062: x=8.8: exp(-10.2/30)=0.71->-0.0044 (obs -0.003). 
    #   x=17.3: exp(-28/30)=0.39->-0.0024 (obs -0.0029). x=20.4: exp(-70/30)=0.10->-0.0006 (obs -0.0011).
    #   s^2=40: x=8.8: exp(-0.256)=0.77->-0.0048 (obs -0.003). Hmm too high on left.
    #   Maybe center ~12.5, s^2=30: x=8.8 dist 3.7: exp(-13.7/30)=0.63->-0.0039 (obs -0.003).
    #   x=17.3 dist 4.8: exp(-23/30)=0.46->-0.0029 (obs -0.0029). x=20.4 dist 7.9: exp(-62/30)=0.13->-0.0008 (obs -0.0011).
    #   x=10.4 dist 2.1: exp(-4.4/30)=0.86->-0.0053 (obs -0.0047). Reasonable.
    #   Use center 12.5, s^2=30, depth -0.0062.
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
            ys.append(bump + base + dip)
        except Exception:
            ys.append(None)
    return {"y": ys}

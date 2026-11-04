import math

def predict(probe):
    # Structure (revised):
    # - Positive Gaussian bump near x≈0.5, height ~0.23, but narrower than before.
    #   [E2 x=1.2->0.228, E5 x=-1.6->0.0919, E6 x=2.0->0.12, E1 x=2.9->0.0362,
    #    E10 x=-3.5->0.0066, E4 x=-5.9->0.0003, E8 x=-6.0->0.0]
    #   Fit: at x=1.2 ->0.228; x=2.0 ->0.12; x=2.9 ->0.036; x=-1.6 ->0.092;
    #   x=-3.5 ->0.0066. Center ~0.6, sigma^2 ~1.6, height ~0.235.
    # - Negative-side baseline: grows with |x|, roughly linear in |x| beyond ~15.
    #   [E5 x=-127.7->-0.0044, E3 x=-102.2->-0.004, E6 x=-107.4->-0.0041,
    #    E8 x=-105->-0.004, E11 x=-102.2->-0.004, E4 x=-124.4->-0.0044,
    #    E3 x=-48.6->-0.0032, E6 x=-46.1->-0.0032, E11 x=-42.9->-0.0032,
    #    E1 x=-50.4->-0.0032, E1 x=-61.7->-0.0032, E4 x=-61.3->-0.0032,
    #    E5 x=-65.6->-0.0033, E11 x=-65.8->-0.0033, E5 x=-66.9->-0.0033,
    #    E11 x=-71.6->-0.0034, E5 x=-79.1->-0.0035, E8 x=-79.5->-0.0035,
    #    E8 x=-80.2->-0.0035, E11 x=-98->-0.0039,
    #    E1 x=-20.3->-0.0013, E1 x=-24.3->-0.0016, E4 x=-25.9->-0.0018,
    #    E9 x=-27.8->-0.0019, E7 x=-29.5->-0.0021, E7 x=-53.7->-0.0032,
    #    E6 x=-13.3->-0.0006, E10 x=-12.7->-0.0006, E3 x=-16.9->-0.001,
    #    E3 x=-7.1->-0.0001, E7 x=-14.1->-0.0007]
    #   Looks like a smooth ramp: ~0 near x=-5, -0.0013 at -20, -0.0032 at -45,
    #   saturating ~-0.0044 at -128. Model as -0.0044 * (|x|/128)^p with p~0.9?
    #   Check: |x|=20 -> -0.0044*(0.156)^0.9 = -0.0044*0.19=-0.00084 (obs -0.0013)
    #   p=0.7: 0.156^0.7=0.27 -> -0.0012. good. |x|=45: 0.352^0.7=0.48 -> -0.0021
    #   (obs -0.0032). Hmm too low. Try linear-ish: |x|=45/128=0.352 -> -0.0015. no.
    #   Actually obs at -45 is -0.0032, at -128 -0.0044. Ratio 0.73 for ratio 0.35.
    #   p = ln(0.73)/ln(0.35) = 0.30. Then |x|=20: 0.156^0.3=0.57 -> -0.0025. Too high.
    #   Not a simple power. Looks more like a sigmoid/ramp saturating.
    #   Try: -0.0044 * tanh(|x|/45)? |x|=20: tanh(0.44)=0.41 -> -0.0018 (obs -0.0013)
    #   |x|=45: tanh(1)=0.76 -> -0.0034 (obs -0.0032) ok. |x|=128: tanh(2.8)=0.99 -> -0.0044 ok.
    #   |x|=13: tanh(0.29)=0.28 -> -0.0012 (obs -0.0006). A bit high.
    #   Use tanh(|x|/55): |x|=20: tanh(0.36)=0.35->-0.0015; |x|=45: tanh(0.82)=0.67->-0.0030;
    #   |x|=128: tanh(2.3)=0.98->-0.0043. Reasonable.
    # - Positive-side baseline: shallow plateau ~-0.0004, shrinking to 0 at large x.
    #   [E7 x=26.4->-0.0004, E9 x=101.1->-0.0001, E10 x=127->-0.0,
    #    E2 x=123.6->-0.0001, E2 x=104.5->-0.0001, E3 x=119.5->-0.0001,
    #    E1 x=88.2->-0.0002, E8 x=87.7->-0.0002, E9 x=89.5->-0.0002,
    #    E2 x=79.4->-0.0003, E6 x=77.6->-0.0003, E11 x=80.9->-0.0003,
    #    E8 x=65.9->-0.0003, E1 x=66->-0.0003, E2 x=65.5->-0.0003,
    #    E3 x=58.8->-0.0004, E4 x=56.2->-0.0004, E6 x=52.9->-0.0004,
    #    E9 x=52.6->-0.0004, E3 x=47.1->-0.0004, E4 x=43->-0.0004,
    #    E10 x=41->-0.0004, E8 x=40.1->-0.0004, E11 x=33.3->-0.0004,
    #    E2 x=30.3->-0.0004, E8 x=28.9->-0.0004, E10 x=28.9->-0.0004,
    #    E3 x=28.4->-0.0004, E7 x=26.4->-0.0004, E7 x=24.6->-0.0004,
    #    E9 x=23->-0.0004, E7 x=22.4->-0.0004, E1 x=21.3->-0.0005,
    #    E10 x=20.4->-0.0011(!), E7 x=19.4->-0.0017(!), E5 x=17.3->-0.0029(!)]
    #   Wait: at x=20.4 obs -0.0011, x=19.4 -0.0017, x=17.3 -0.0029. That's the dip!
    #   So the dip near x~12 extends to ~20. And the plateau -0.0004 starts ~21+.
    # - Negative dip on positive side: centered ~12, but wider than modeled.
    #   [E6 x=12.1->-0.0061, E4 x=12.5->-0.0058, E6 x=13.1->-0.0055,
    #    E9 x=10.4->-0.0047, E7 x=10.3->-0.0046, E5 x=17.3->-0.0029,
    #    E7 x=19.4->-0.0017, E10 x=20.4->-0.0011, E1 x=21.3->-0.0005]
    #   Center ~12, depth ~-0.0062, sigma^2 ~ 22? at x=17.3: exp(-(5.3)^2/22)=exp(-1.28)=0.28
    #   -> -0.0017 (obs -0.0029). sigma^2=40: exp(-28/40)=0.50->-0.0031 ok.
    #   at x=20.4: exp(-70/40)=0.17->-0.0011 ok. at x=10.4: exp(-2.56/40)=0.94->-0.0058
    #   (obs -0.0047). Hmm. Maybe asymmetric or center ~12.5.
    #   Use center 12, sigma^2=35, depth -0.0062.
    # - Small positive bump near x=-3.5? E10 x=-3.5->0.0066, E4 x=-5.9->0.0003,
    #   E8 x=-6->0.0. Could be tail of main bump (center 0.6, sigma^2 1.6):
    #   at -3.5: exp(-(4.1)^2/1.6)=exp(-10.5)=0 tiny. So 0.0066 is NOT the main bump.
    #   There's a second small positive bump near x≈-3.5, height ~0.0066, narrow.
    #   [E10 x=-3.5->0.0066; E4 x=-5.9->0.0003; E8 x=-6->0.0]
    #   sigma^2 ~ 1.0: at -5.9: exp(-(2.4)^2/1)=exp(-5.8)=0.003 -> 0.00002. obs 0.0003.
    #   sigma^2=2: exp(-5.76/2)=0.056->0.0004 ok. So bump2: 0.0066*exp(-(x+3.5)^2/2).
    xs = probe.get("x", []) if isinstance(probe, dict) else []
    ys = []
    for x in xs:
        try:
            x = float(x)
        except Exception:
            ys.append(None)
            continue
        try:
            # main positive bump near 0.6
            bump = 0.235 * math.exp(-((x - 0.6) ** 2) / 1.6)
            # small positive bump near -3.5
            bump2 = 0.0066 * math.exp(-((x + 3.5) ** 2) / 2.0)
            # baseline
            if x < 0:
                base = -0.0044 * math.tanh(abs(x) / 55.0)
            else:
                if x <= 21.0:
                    base = -0.0004 * (x / 21.0)
                elif x <= 60.0:
                    base = -0.0004
                else:
                    base = -0.0004 * (128.0 - x) / 68.0
            # negative dip near x=12 (positive side only)
            if x > 0:
                dip = -0.0062 * math.exp(-((x - 12.0) ** 2) / 35.0)
            else:
                dip = 0.0
            ys.append(bump + bump2 + base + dip)
        except Exception:
            ys.append(None)
    return {"y": ys}

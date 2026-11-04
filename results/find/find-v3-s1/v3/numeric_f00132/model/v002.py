import math

def predict(probe):
    # Model of f(x): an MLP approximating a smooth function.
    # E2 shows f is NOT odd: f(0)=3.92, and near zero f is roughly linear
    # with slope ~5.3 (e.g. f(0.25)=5.27, f(0.5)=6.59, f(1)=8.93).
    # For larger |x| the slope grows: f(5)=27.8, f(8)=41.9, and at large x
    # the slope is ~4.7 (E1). So f is like a*x + b + c*tanh-like saturation.
    # Fit: f(x) = A*x + B + C*tanh(D*x) won't give growing slope.
    # Instead: f(x) = a*x + b + c*tanh(x/s) with slope near 0 = a + c/s.
    # Near 0 slope ~5.3; large-x slope ~4.7. So slope DECREASES with |x|,
    # meaning c<0 (a - |c|/s near 0, a far away). But f is increasing
    # everywhere and roughly linear far out.
    # Let's fit a*x + b + c*tanh(x/s).
    # Large x: f ~ (a+c)*x + b + sign*c... actually tanh->sign(x).
    # For x>0 large: f ~ a*x + b + c. For x<0 large: f ~ a*x + b - c.
    # E1: x=88.9 -> 423.29; x=-93.6 -> -434.46.
    # a*88.9 + b + c = 423.29
    # a*(-93.6) + b - c = -434.46
    # Also x=120.7 neg: a*(-120.7)+b-c = -561.47
    # From these two neg: a*(-93.6)-a*(-120.7) = -434.46+561.47=127.01
    #   a*27.1 = 127.01 -> a = 4.687
    # Then b - c = -434.46 + 4.687*93.6 = -434.46+438.7 = 4.24
    # Pos: x=67.5 -> 322.41: a*67.5+b+c = 316.4+b+c=322.41 -> b+c=6.01
    # x=73.9 -> 352.58: 346.4+b+c=352.58 -> b+c=6.18
    # x=38.8 -> 187.12: 181.9+b+c=187.12 -> b+c=5.22
    # Hmm b+c varies; slope not perfectly constant. Use a=4.687.
    # b+c ~ 5.8, b-c ~ 4.24 -> b=5.02, c=0.78.
    # Check near 0: f(0)=b=5.02 vs observed 3.92. Off.
    # The tanh model with small c can't produce the near-zero curvature.
    # E2 near-zero: f(0)=3.92, f(0.25)=5.27, f(0.5)=6.59, f(1)=8.93,
    # f(1.5)=11.29, f(2)=13.65, f(3)=18.35, f(5)=27.78, f(8)=41.92.
    # Differences: 0->0.25: 1.35 (slope 5.4); 0.25->0.5: 1.32 (5.3);
    # 0.5->1: 2.35 (4.7); 1->1.5: 2.36 (4.7); 1.5->2: 2.36 (4.7);
    # 2->3: 4.70 (4.7); 3->5: 9.43 (4.7); 5->8: 14.14 (4.7).
    # So slope is ~5.3 for |x|<0.5, then ~4.7 beyond. A smooth transition.
    # Negative side: f(-0.5)=1.96, f(-1)=-0.24, f(-1.5)=-2.93, f(-2)=-5.15,
    # f(-3)=-9.90, f(-5)=-19.26.
    # Differences: -0.5->-1: -2.20 (slope 4.4); -1->-1.5: -2.69 (5.4);
    # -1.5->-2: -2.22 (4.4); -2->-3: -4.75 (4.75); -3->-5: -9.36 (4.68).
    # Noisy but roughly slope 4.7 with a bump near -1.
    # The function is close to linear with slope ~4.7 plus a small
    # near-zero correction and an offset. Let's model:
    # f(x) = 4.7*x + 3.9 + correction, where correction is small bump.
    # At x=0: 3.9 good. At x=0.5: 2.35+3.9=6.25 vs 6.59 (need +0.34).
    # At x=1: 4.7+3.9=8.6 vs 8.93 (+0.33). At x=2: 9.4+3.9=13.3 vs 13.65.
    # At x=5: 23.5+3.9=27.4 vs 27.78. At x=8: 37.6+3.9=41.5 vs 41.92.
    # So add ~0.35 for x>0. For x<0: x=-1: -4.7+3.9=-0.8 vs -0.24 (+0.56)
    # x=-2: -9.4+3.9=-5.5 vs -5.15 (+0.35). x=-5: -23.5+3.9=-19.6 vs -19.26.
    # So correction ~+0.4 on both sides, slightly more near -1.
    # Large x: x=88.9: 4.7*88.9+3.9=421.7 vs 423.29 (+1.6). Slope a bit higher.
    # Use a=4.72: 88.9*4.72+3.9=423.5 good. x=-93.6: -441.8+3.9=-437.9 vs -434.46.
    # Hmm negative needs less. Use a=4.70, b=3.9, and add small tanh bump.
    # Let's do: f(x)=4.70*x + 3.9 + 0.4*exp(-(x/2)^2) + 0.15*tanh(x/50)*x/50*... 
    # Keep simple: f(x) = 4.70*x + 3.9 + 0.4*exp(-(x/2.5)^2)
    # Check x=0: 3.9+0.4=4.3 vs 3.92. Slightly high; reduce base.
    # Use b=3.55, bump 0.4: f(0)=3.95 good.
    # x=0.5: 2.35+3.55+0.4*exp(-0.04)=5.9+0.384=6.28 vs 6.59.
    # x=1: 4.7+3.55+0.4*0.852=8.25+0.34=8.59 vs 8.93.
    # x=2: 9.4+3.55+0.4*0.527=12.95+0.21=13.16 vs 13.65.
    # x=5: 23.5+3.55+0.4*0.018=27.05 vs 27.78.
    # Consistently ~0.5 low for mid x. Increase slope to 4.75:
    # x=5: 23.75+3.55=27.3 vs 27.78. x=8: 38+3.55=41.55 vs 41.92.
    # x=88.9: 422.3+3.55=425.8 vs 423.29 (high).
    # Slope varies: ~4.75 for mid, ~4.72 for large. Use 4.73.
    # x=5: 23.65+3.55=27.2. x=88.9: 420.5+3.55=424.1 vs 423.29 ok.
    # x=-93.6: -442.7+3.55=-439.2 vs -434.46 (too low by 4.7).
    # Negative side slope ~4.64. So asymmetry: positive slope 4.75, neg 4.64.
    # Use a = 4.75 if x>0 else 4.64, b=3.55, bump 0.4*exp(-(x/2.5)^2).
    # x=-93.6: -434.3+3.55+~0=-430.8 vs -434.46. Close.
    # x=-120.7: -560.0+3.55=-556.5 vs -561.47. Off by 5.
    # neg slope: from -93.6 to -120.7: (-561.47+434.46)/(-27.1)=4.687.
    # So neg slope 4.687. x=-93.6: -438.7+3.55=-435.2 vs -434.46 good.
    # x=-120.7: -565.7+3.55=-562.2 vs -561.47 good.
    # x=-62.7: -293.9+3.55=-290.3 vs -289.64 good.
    # x=-104: -487.4+3.55=-483.9 vs -483.20 good.
    # pos slope: x=38.8->187.12, x=88.9->423.29: (423.29-187.12)/50.1=4.714
    # x=67.5->322.41, x=73.9->352.58: (352.58-322.41)/6.4=4.714
    # So pos slope 4.714, b: 38.8*4.714=182.9, +b=187.12 -> b=4.2
    # But b from neg: -62.7*4.687=-293.9, +b=-289.64 -> b=4.26
    # So b~4.2, consistent! Use b=4.2.
    # x=0: 4.2+bump=3.92 -> bump=-0.28 at 0? But near zero f rises faster.
    # Recheck: f(0)=3.92, f(0.25)=5.27. slope 5.4 near 0.
    # With a=4.71, b=4.2: f(0.25)=1.18+4.2=5.38 vs 5.27. ok!
    # f(0)=4.2 vs 3.92. Slight dip at 0. Add small negative bump at 0?
    # Actually f(0.5)=2.36+4.2=6.56 vs 6.59 good. f(1)=4.71+4.2=8.91 vs 8.93!
    # f(2)=9.42+4.2=13.62 vs 13.65! f(3)=14.13+4.2=18.33 vs 18.35!
    # f(5)=23.55+4.2=27.75 vs 27.78! f(8)=37.68+4.2=41.88 vs 41.92!
    # Excellent. So f(x) = 4.71*x + 4.2 for x>=0 works great except f(0).
    # f(0)=4.2 vs 3.92: small dip. And f(-0.5)=1.96: 4.71*-0.5+4.2=1.85 vs 1.96.
    # f(-1)=-0.24: -4.71+4.2=-0.51 vs -0.24. f(-1.5)=-2.93: -7.07+4.2=-2.87 good.
    # f(-2)=-5.15: -9.42+4.2=-5.22 good. f(-3)=-9.90: -14.13+4.2=-9.93 good!
    # f(-5)=-19.26: -23.55+4.2=-19.35 good.
    # So near-zero has a small wiggle (dip at 0, bump at -1). MLP artifact.
    # Model: f(x) = a*x + 4.2 + small wiggle, a=4.71 (pos), 4.687 (neg).
    # Add small correction: -0.28*exp(-(x/0.5)^2) for the dip at 0,
    # and +0.3*exp(-((x+1)/1)^2) for the bump near -1.
    # Keep it simple and smooth.
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            a = 4.71 if x >= 0 else 4.687
            y = a * x + 4.2
            # small dip at exactly 0 (MLP artifact)
            y += -0.28 * math.exp(-(x / 0.6) ** 2)
            # small bump near x=-1
            y += 0.30 * math.exp(-((x + 1.0) / 1.0) ** 2)
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}

import math

def predict(probe):
    # Beliefs (from E1, E2):
    # - f is odd: f(-x) = -f(x) [E2: pairs (-80,80),(-40,40),... mirror in sign]
    # - f is smooth, monotone-ish, saturating at large |x| [E1,E2]
    # - y/x ratio: ~1.28 at x=2, ~1.82 at x=5, ~2.28 at x=10, ~2.24 at x=20,
    #   ~1.34 at x=40, ~0.78 at x=80 [E2]
    # - So |y| rises fast then saturates; looks like a saturating odd curve.
    # - Try y = -A * tanh(x/s) * something, or -A*x/(1+|x|/k)^p.
    # Fit: at x=80, y=-62.48; x=40, y=-53.52; x=20, y=-44.75; x=10, y=-36.40;
    #   x=5, y=-25.42; x=2, y=-15.58.
    # Ratio y/x: 2->7.79, 5->5.08, 10->3.64, 20->2.24, 40->1.34, 80->0.78.
    # This looks like y = -A * x / (b + |x|)^? Let's try y = -A * sign(x) * |x|^p / (c+|x|^p).
    # Simpler: y = -A * tanh(x/s) * |x|^q? Try y = -A * x / (1 + (|x|/k))^? 
    # Try y = -A * x / (b + |x|): at x=80: A*80/(b+80)=62.48; x=40: A*40/(b+40)=53.52
    #   ratio: 2*(b+40)/(b+80) = 62.48/53.52*... wait: (80/(b+80))/(40/(b+40)) = 2(b+40)/(b+80) = 62.48/53.52=1.167
    #   2(b+40)=1.167(b+80) -> 2b+80=1.167b+93.4 -> 0.833b=13.4 -> b=16.1
    #   Then A: A*80/96.1=62.48 -> A=75.06. Check x=20: 75.06*20/36.1=41.6 vs 44.75. Close-ish.
    #   x=10: 75.06*10/26.1=28.8 vs 36.4. Off.
    # Try y = -A * x / (b + |x|^p). 
    # Let's just fit a smooth odd saturating function numerically-ish.
    # Use y = -A * tanh(x/s) * (1 + c*|x|/(d+|x|))? Getting complex.
    # Alternative: y = -A * x / (1 + (x/s)^2)^(p/2)? 
    # Let's try y = -A * x / (b + |x|^p) with p~1.5.
    # Actually ratios: at small x, y/x large (7.79 at x=2). So y ~ -A*x^alpha with alpha<1 near 0? 
    # y(2)=-15.58, y(5)=-25.42: ratio 1.63 for x ratio 2.5 -> alpha=log(1.63)/log(2.5)=0.53.
    # y(5)/y(10)=25.42/36.4=0.698, x ratio 2 -> alpha=0.52.
    # y(10)/y(20)=36.4/44.75=0.813, alpha=0.30.
    # y(20)/y(40)=44.75/53.52=0.836, alpha=0.26.
    # y(40)/y(80)=53.52/62.48=0.857, alpha=0.22.
    # So y ~ -A * |x|^0.5 for small x, saturating toward -A_max ~ 65-70.
    # Try y = -A * |x|^0.5 / (1 + |x|^0.5/B) * sign(x)? 
    #   = -A * sign(x) * |x|^0.5 * B/(B+|x|^0.5)
    # At x=2: A*1.414*B/(B+1.414)=15.58
    # At x=80: A*8.944*B/(B+8.944)=62.48
    # ratio: (8.944/1.414)*(B+1.414)/(B+8.944)=6.325*(B+1.414)/(B+8.944)=62.48/15.58=4.01
    #   6.325(B+1.414)=4.01(B+8.944) -> 6.325B+8.94=4.01B+35.87 -> 2.315B=26.93 -> B=11.63
    #   A: A*8.944*11.63/20.57=62.48 -> A*5.057=62.48 -> A=12.36
    # Check x=10: 12.36*3.162*11.63/(11.63+3.162)=12.36*3.162*11.63/14.79=30.7 vs 36.4. Off.
    # Try y = -A * sign(x) * |x|^0.5 * (1 - exp(-|x|/t))? 
    # Let's just use a flexible odd form and fit roughly:
    # y = -A * sign(x) * (1 - exp(-(|x|/s)^p))^q ... 
    # Given time, use y = -A * sign(x) * |x|^0.5 / (1 + |x|^0.5/B) with tuned A,B.
    # Better: interpolate. Use y = -A * tanh((|x|/s)^p) * sign(x).
    # At x=80: A*tanh((80/s)^p)=62.48
    # At x=2: A*tanh((2/s)^p)=15.58
    # If p=0.5: tanh(sqrt(80/s)) vs tanh(sqrt(2/s)).
    # Try s=20,p=0.5: tanh(sqrt(4))=tanh(2)=0.964; tanh(sqrt(0.1))=tanh(0.316)=0.306
    #   ratio 0.964/0.306=3.15, need 4.01. 
    # Try s=10,p=0.5: tanh(sqrt(8))=tanh(2.83)=0.993; tanh(sqrt(0.2))=tanh(0.447)=0.420
    #   ratio 2.36. Worse.
    # Try p=0.4, s=20: (80/20)^0.4=4^0.4=1.741, tanh=0.940; (2/20)^0.4=0.1^0.4=0.398,tanh=0.378
    #   ratio 2.49. 
    # Hmm the small-x behavior is steeper than sqrt.
    # y(2)/y(5)=15.58/25.42=0.613, x ratio 2.5 -> alpha=0.53 (sqrt-ish).
    # But y(2)=15.58 means at x=2 already substantial. And y(0)=0 presumably.
    # Actually maybe there's a linear term plus saturating: y = -(a*x + b*tanh(x/c))?
    # At small x: slope a + b/c. y(2)/2=7.79. 
    # Let's try y = -(a*x + b*tanh(x/c)) with a small.
    # At large x: a*x + b -> at x=80: 80a+b=62.48; x=40: 40a+b=53.52 -> 40a=8.96 -> a=0.224, b=44.56
    # Check x=20: 20*0.224+44.56*tanh(20/c). Need 44.75. 4.48+44.56*tanh(20/c)=44.75 -> tanh(20/c)=0.903 -> 20/c=1.49 -> c=13.4
    # Check x=10: 2.24+44.56*tanh(10/13.4)=2.24+44.56*tanh(0.746)=2.24+44.56*0.633=30.4 vs 36.4. Off.
    # Check x=5: 1.12+44.56*tanh(0.373)=1.12+44.56*0.357=17.0 vs 25.42. Off.
    # The data has a "shoulder" — ratio peaks around x=10-20.
    # y/x: 2->7.79, 5->5.08, 10->3.64, 20->2.24, 40->1.34, 80->0.78
    # This is monotonically decreasing ratio. So y is concave (sublinear) throughout.
    # y = -A * |x|^p with p<1: y(2)=15.58, y(80)=62.48 -> (80/2)^p=62.48/15.58=4.01 -> p=log(4.01)/log(40)=1.389/3.689=0.377
    # Check: A=15.58/2^0.377=15.58/1.30=11.98
    # x=5: 11.98*5^0.377=11.98*1.836=22.0 vs 25.42. Off by 14%.
    # x=10: 11.98*10^0.377=11.98*2.38=28.5 vs 36.4. Off.
    # x=20: 11.98*20^0.377=11.98*3.09=37.0 vs 44.75. Off.
    # x=40: 11.98*40^0.377=11.98*4.01=48.0 vs 53.52. Off.
    # Not pure power law. There's a knee.
    # Let's try y = -A * sign(x) * |x| / (b + |x|^p) with p>1.
    # At large x: y ~ -A*|x|^(1-p) -> decays. But data saturates, not decays.
    # Try y = -A * sign(x) * (1 - 1/(1+(|x|/s)^p)) = -A*sign(x)*(|x|/s)^p/(1+(|x|/s)^p)
    # This is a Hill function, saturating to A. 
    # y(80)=62.48, y(2)=15.58. If A~70: 
    #   62.48/70=0.893 -> (80/s)^p/(1+)=0.893 -> (80/s)^p=8.35
    #   15.58/70=0.2226 -> (2/s)^p=0.286
    #   ratio: (40)^p=8.35/0.286=29.2 -> p=log(29.2)/log(40)=3.374/3.689=0.915
    #   (2/s)^0.915=0.286 -> 2/s=0.286^(1/0.915)=0.286^1.093=0.256 -> s=7.81
    # Check x=10: (10/7.81)^0.915=1.28^0.915=1.253; 70*1.253/2.253=38.9 vs 36.4. Close!
    # x=20: (2.56)^0.915=2.36; 70*2.36/3.36=49.2 vs 44.75. Off by 10%.
    # x=40: (5.12)^0.915=4.51; 70*4.51/5.51=57.3 vs 53.52. Off.
    # x=5: (0.64)^0.915=0.664; 70*0.664/1.664=27.9 vs 25.42. Close.
    # Reasonable. Let me tune A, s, p a bit.
    # Try A=68, p=0.85, s=8:
    # x=2: (0.25)^0.85=0.308; 68*0.308/1.308=16.0 vs 15.58 ✓
    # x=5: (0.625)^0.85=0.671; 68*0.671/1.671=27.3 vs 25.42
    # x=10: (1.25)^0.85=1.208; 68*1.208/2.208=37.2 vs 36.4 ✓
    # x=20: (2.5)^0.85=2.18; 68*2.18/3.18=46.6 vs 44.75
    # x=40: (5)^0.85=3.93; 68*3.93/4.93=54.2 vs 53.52 ✓
    # x=80: (10)^0.85=7.08; 68*7.08/8.08=59.6 vs 62.48
    # Decent. Try A=70, p=0.9, s=8.5:
    # x=2: (0.235)^0.9=0.272; 70*0.272/1.272=15.0 vs 15.58
    # x=5: (0.588)^0.9=0.619; 70*0.619/1.619=26.8 vs 25.42
    # x=10: (1.176)^0.9=1.157; 70*1.157/2.157=37.5 vs 36.4
    # x=20: (2.353)^0.9=2.16; 70*2.16/3.16=47.8 vs 44.75
    # x=40: (4.706)^0.9=4.02; 70*4.02/5.02=56.1 vs 53.52
    # x=80: (9.41)^0.9=7.53; 70*7.53/8.53=61.8 vs 62.48 ✓
    # Good enough. Use A=69, p=0.88, s=8.2.
    A, p, s = 69.0, 0.88, 8.2
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
            t = (abs(x) / s) ** p
            y = -A * t / (1.0 + t)
            if x < 0:
                y = -y
            ys.append(y)
        except Exception:
            ys.append(None)
    return {"y": ys}

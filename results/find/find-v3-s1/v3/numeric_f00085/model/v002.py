import math

def predict(probe):
    # Model hypotheses:
    # f(x) is a piecewise function:
    #   For |x| <= ~5 (a dead zone), f(x) = -22.8021 (constant) [E2]
    #   Outside the dead zone, f(x) is quadratic with positive curvature [E1, E2]
    # The dead zone is symmetric around 0: at x=-5 and x=5 we see -22.8021 [E2]
    # At x=10, y=272.93; at x=-10, y=269.53 (roughly symmetric) [E2]
    # Quadratic: y = a*x^2 + c, with a ~ 3.18, c ~ -22.8 (fit from E2 large values)
    # Check: x=120 -> 3.18*14400 - 22.8 = 45769 (obs 45868) close
    # x=100 -> 3.18*10000 - 22.8 = 31777 (obs 34058) - a bit off
    # Let's fit better: use x=40 (5460), x=120 (45868)
    # a = (45868 - 5460)/(14400-1600) = 40408/12800 = 3.157
    # c = 5460 - 3.157*1600 = 5460 - 5051 = 409? That doesn't match -22.8
    # Try quadratic with linear term? x=40: 5460, x=-40: 5748 (slight asymmetry)
    # x=120: 45868, x=100: 34058. Diff 11810 over 4400 -> ~2.68 per unit at ~110
    # x=40 to 60: 12387-5460=6927 over 2000 -> 3.46 per unit at ~50
    # Curvature not constant; maybe cubic or higher. But MLP approximates.
    # Let's fit a*x^2 + b*x + c using E2 outside dead zone.
    # Use points: (-40,5748.25), (40,5460.32), (120,45868.65)
    # From -40 and 40: 1600a - 40b + c = 5748.25; 1600a+40b+c=5460.32
    # Subtract: 80b = -287.93 -> b = -3.599
    # Add: 3200a + 2c = 11208.57 -> 1600a + c = 5604.28
    # x=120: 14400a + 120b + c = 45868.65
    # 14400a + 120*(-3.599) + c = 45868.65
    # 14400a + c = 45868.65 + 431.9 = 46300.55
    # Subtract (1600a+c=5604.28): 12800a = 40696.27 -> a = 3.1794
    # c = 5604.28 - 1600*3.1794 = 5604.28 - 5087.0 = 517.3
    # Hmm c=517 doesn't match dead zone -22.8. So quadratic isn't right globally.
    # Check x=10: 3.1794*100 - 3.599*10 + 517.3 = 317.94 - 35.99 + 517.3 = 799 (obs 272.9) - off
    # So the function is not a simple quadratic. It looks like it grows faster than quadratic.
    # Check ratio: x=120 -> 45868, x=60 -> 12387. Ratio 3.70 for x ratio 2. So ~x^1.89
    # x=40 -> 5460, x=20 -> 1357. Ratio 4.02 for x ratio 2. ~x^2
    # x=120/40=3, y ratio 45868/5460=8.4 -> x^1.94
    # Roughly quadratic but with some deviation. MLP approximation.
    # Let's use power law: y = A*|x|^p + c for |x|>5
    # x=20: 1357, x=40: 5460 -> ratio 4.02 -> p = log2(4.02) = 2.007
    # x=40: 5460, x=80: 22248.69 -> ratio 4.075 -> p=2.027
    # x=60: 12387, x=120: 45868 -> ratio 3.70 -> p=1.89
    # Not consistent. Let's just fit quadratic on larger points and accept error.
    # Better: fit a*x^2 + b*x + c using least squares on E2 outside dead zone.
    # Points: (-40,5748.25),(-30,3259.36),(-20,1508.06),(-10,269.53),
    #         (10,272.93),(20,1357.30),(30,3042.98),(40,5460.32),
    #         (50,8572.41),(60,12387.50),(80,22248.69),(100,34058.67),(120,45868.65)
    # Let me estimate: quadratic fit. Use x=20,40,80:
    # 400a+20b+c=1357.30; 1600a+40b+c=5460.32; 6400a+80b+c=22248.69
    # (2)-(1): 1200a+20b=4103.02
    # (3)-(2): 4800a+40b=16788.37
    # Multiply first by 2: 2400a+40b=8206.04
    # Subtract: 2400a = 8582.33 -> a=3.576
    # 20b = 4103.02 - 1200*3.576 = 4103.02 - 4291.2 = -188.18 -> b=-9.409
    # c = 1357.30 - 400*3.576 - 20*(-9.409) = 1357.30 - 1430.4 + 188.18 = 115.08
    # Check x=120: 3.576*14400 - 9.409*120 + 115.08 = 51494 - 1129 + 115 = 50480 (obs 45868) - 10% off
    # Check x=10: 3.576*100 - 94.09 + 115.08 = 357.6 + 21 = 378.6 (obs 272.9) - off
    # The function seems to have a "soft" transition. 
    # Given it's an MLP, maybe it's something like a smooth ReLU-ish or x^2 with softplus.
    # Let's try: y = a*(sqrt(x^2 + eps) - sqrt(eps))^2 + c? Or y = a*x^2/(1+exp(-k(|x|-t)))?
    # Actually looking at data: near 0 it's flat at -22.8, then rises.
    # x=5: -22.8, x=10: 272.9. So transition between 5 and 10.
    # Let's model: for |x|<=5: -22.8021
    # for |x|>5: quadratic fit. Use points x=10,20,40,80,120 to fit.
    # Least squares: let me just pick reasonable coefficients.
    # From x=10 (272.93) and x=120 (45868.65):
    # If y = a*x^2 + c: 100a+c=272.93, 14400a+c=45868.65 -> 14300a=45595.72 -> a=3.1885, c=-45.9
    # Check x=40: 3.1885*1600-45.9=5055.7 (obs 5460) - 7% off
    # Check x=80: 3.1885*6400-45.9=20360 (obs 22249) - 8% off
    # Check x=20: 3.1885*400-45.9=1229.5 (obs 1357) - 9% off
    # Consistently under. Maybe cubic term.
    # Try y = a*x^2 + b*x^3? Fit x=20,120:
    # 400a+8000b=1357.30; 14400a+1728000b=45868.65
    # From first: a = (1357.30-8000b)/400 = 3.393 - 20b
    # 14400*(3.393-20b)+1728000b = 45868.65
    # 48859.2 - 288000b + 1728000b = 45868.65
    # 1440000b = -2990.55 -> b = -0.002077
    # a = 3.393 + 0.04154 = 3.4345
    # Check x=40: 3.4345*1600 - 0.002077*64000 = 5495 - 132.9 = 5362 (obs 5460) - 2% off
    # Check x=80: 3.4345*6400 - 0.002077*512000 = 21981 - 1063 = 20918 (obs 22249) - 6% off
    # Hmm. Let's try y = a*x^2 + b*x^4? 
    # Actually, let's just use a smooth interpolation. Given MLP, maybe it's x^2 * sigmoid.
    # Simplest good model: piecewise with quadratic fit on |x|>5.
    # Let me fit quadratic to all outside points via least squares mentally.
    # Actually let's use: y = a*x^2 + b*x + c with a=3.2, b=-1.5, c=-50 for |x|>5
    # Check x=10: 320-15-50=255 (obs 272.9) ok
    # x=20: 1280-30-50=1200 (obs 1357) - 12%
    # x=40: 5120-60-50=5010 (obs 5460) - 8%
    # x=80: 20480-120-50=20310 (obs 22249) - 9%
    # x=120: 46080-180-50=45850 (obs 45868) - great!
    # Hmm x=120 matches but others under. 
    # Let me try a=3.3, b=-2, c=-30:
    # x=10: 330-20-30=280 (obs 272.9) 
    # x=20: 1320-40-30=1250 (obs 1357) - 8%
    # x=40: 5280-80-30=5170 (obs 5460) - 5%
    # x=80: 21120-160-30=20930 (obs 22249) - 6%
    # x=120: 47520-240-30=47250 (obs 45868) +3%
    # Reasonable. Let's go with a=3.3, b=-2, c=-30 for |x|>5.
    # For |x|<=5: -22.8021
    # Check x=-40: 3.3*1600+80-30=5330 (obs 5748) - 7%
    # x=-120: 47520+240-30=47730 (obs 46913) +2%
    # Good enough.
    # Also check E1: x=-93.6: 3.3*8761+187.2-30=28911+157=29068 (obs 30915) - 6%
    # x=88.9: 3.3*7903-177.8-30=26080-208=25872 (obs 27504) - 6%
    # x=67.5: 3.3*4556-135-30=15035-165=14870 (obs 15709) - 5%
    # x=-62.7: 3.3*3931+125.4-30=12972+95=13067 (obs 13990) - 7%
    # x=-1.2: dead zone -> -22.8 (obs -22.8) 
    # x=-12.9: 3.3*166.4+25.8-30=549+(-4)=545 (obs 629) - 13%
    # x=38.8: 3.3*1505-77.6-30=4967-108=4859 (obs 5135) - 5%
    # x=73.9: 3.3*5461-147.8-30=18021-178=17843 (obs 18855) - 5%
    # x=-104: 3.3*10816+208-30=35693+178=35871 (obs 37054) - 3%
    # x=-120.7: 3.3*14568+241.4-30=48074+211=48285 (obs 46913) +3%
    # Consistent ~5% under for positive, mixed for negative. The true function seems slightly steeper.
    # Let's bump a to 3.45, keep b=-2, c=-30:
    # x=40: 5520-80-30=5410 (obs 5460) 
    # x=80: 22080-160-30=21890 (obs 22249) - 1.6%
    # x=120: 49680-240-30=49410 (obs 45868) +7.7% - too high
    # Hmm. The function isn't quite quadratic. Let's use a=3.35:
    # x=40: 5360-80-30=5250 (obs 5460) - 4%
    # x=80: 21440-160-30=21250 (obs 22249) - 4.5%
    # x=120: 48240-240-30=47970 (obs 45868) +4.6%
    # Balanced. Use a=3.35, b=-2, c=-30.
    # Actually let's also consider the dead zone boundary. At x=5: -22.8, x=10: 272.9.
    # Maybe the dead zone is |x|<=5 exactly. At x=-5: -22.8, x=-10: 269.5.
    # So boundary at 5. Good.
    # Final model: piecewise.
    a = 3.35
    b = -2.0
    c = -30.0
    dead = -22.8021
    edge = 5.0
    xs = probe.get("x", [])
    out = []
    for x in xs:
        try:
            if abs(x) <= edge:
                y = dead
            else:
                y = a * x * x + b * x + c
        except Exception:
            y = None
        out.append(y)
    return {"y": out}

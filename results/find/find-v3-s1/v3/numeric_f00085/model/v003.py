import math

def predict(probe):
    # Model hypotheses:
    # f(x) = -22.8021 for |x| <= 7 (dead zone) [E4: flat through x=-7, jumps at x=-8]
    # Outside dead zone, f(x) is smooth, roughly quadratic, slightly asymmetric [E1,E2,E3]
    # Fit quadratic y = a*x^2 + b*x + c on outside points (least squares-ish).
    # Points (|x|>7): (-40,5748.25),(-30,3259.36),(-20,1508.06),(-10,269.53),
    #   (10,272.93),(20,1357.30),(30,3042.98),(40,5460.32),(50,8572.41),
    #   (60,12387.50),(80,22248.69),(100,34058.67),(120,45868.65),
    #   (-8,21.82),(86,25791.69),(-17.2,1161.27),(67.1,15521.38),
    #   (-127.5,50927.45),(-14,764.94),(56.7,11053.66),(-69.4,17112.22),
    #   (114,42325.65),(102.8,35712.07),(-120.2,46617.94),
    #   (-93.6,30914.79),(88.9,27504.13),(67.5,15708.51),(-62.7,13990.07),
    #   (-12.9,628.70),(38.8,5134.75),(73.9,18854.79),(-104,37054.37),
    #   (-120.7,46913.11)
    # Fit: use a*x^2 + b*x + c. Try a=3.30, b=-1.0, c=-40.
    # Check x=120: 47520-120-40=47360 (obs 45868) +3%
    # x=100: 33000-100-40=32860 (obs 34058) -3.5%
    # x=80: 21120-80-40=21000 (obs 22249) -5.6%
    # x=40: 5280-40-40=5200 (obs 5460) -4.8%
    # x=20: 1320-20-40=1260 (obs 1357) -7%
    # x=10: 330-10-40=280 (obs 273) +2.6%
    # x=-40: 5280+40-40=5280 (obs 5748) -8%
    # x=-120: 47520+120-40=47600 (obs 46913) +1.5%
    # Reasonable. Slight under on positive mid-range.
    # Try a=3.35, b=-1.0, c=-40:
    # x=40: 5360-40-40=5280 (obs 5460) -3.3%
    # x=80: 21440-80-40=21320 (obs 22249) -4.2%
    # x=120: 48240-120-40=48080 (obs 45868) +4.8%
    # x=10: 335-10-40=285 (obs 273) +4.4%
    # x=-40: 5360+40-40=5360 (obs 5748) -6.7%
    # x=-120: 48240+120-40=48320 (obs 46913) +3%
    # Balanced. Use a=3.32, b=-1.0, c=-40.
    # Check x=8: 3.32*64-8-40=212.5-48=164.5 (obs at -8 is 21.8) - off near boundary.
    # Near boundary the function is softer (MLP smooth). Add smooth blend.
    # At x=8: obs ~21.8 (only -8 measured). At x=10: 272.9.
    # So transition from -22.8 at 7 to ~273 at 10. Very steep.
    # Model: dead zone |x|<=7, then quadratic. At x=8 quadratic gives 164 but obs ~22.
    # So there's a soft ramp between 7 and ~10. Use smoothstep blend.
    # Let's model: for |x|<=7: -22.8021
    # for 7<|x|<10: blend from dead to quadratic via smoothstep
    # for |x|>=10: quadratic
    a = 3.32
    b = -1.0
    c = -40.0
    dead = -22.8021
    edge = 7.0
    ramp = 10.0
    xs = probe.get("x", [])
    out = []
    for x in xs:
        try:
            ax = abs(x)
            if ax <= edge:
                y = dead
            elif ax >= ramp:
                y = a * x * x + b * x + c
            else:
                t = (ax - edge) / (ramp - edge)
                s = t * t * (3 - 2 * t)
                quad = a * x * x + b * x + c
                y = dead + s * (quad - dead)
        except Exception:
            y = None
        out.append(y)
    return {"y": out}

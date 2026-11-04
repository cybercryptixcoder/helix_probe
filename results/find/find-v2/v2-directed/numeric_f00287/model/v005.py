import math

def predict(probe):
    # Left linear: y = -0.7*floor(x) for x < -5 [E1,E2,E4]
    #   E4: -11.5,-11.2,-11.1 -> 8.4 = -0.7*floor(x) (floor=-12) [E4]
    #   E2: -15..-12 -> 10.5,9.8,9.1,8.4 = -0.7*floor(x) [E2]
    #   E4: -6.5,-6.2,-6.1 -> 4.9 (floor=-7); -5.9,-5.5 -> 4.2 (floor=-6) [E4]
    #   E1: -5 -> -402.32 (constant), so boundary x < -5 [E1]
    # Middle constant: y ~ -402.3 (noisy) for -5 <= x < 18.5 [E1,E2,E3,E5]
    #   E5: -4.9..15.5 all ~-402.3; 18.51 -> -402.2 (still constant!) [E5]
    #   E5: 18.55 -> -302.4 (linear). So boundary between 18.51 and 18.55.
    #   E4: 18.6 -> -302.4. E3: 18.5 -> -402.35 (constant). So boundary ~18.52?
    #   Hmm E5 18.51 constant, 18.55 linear. Need exact threshold.
    #   Right linear: y = -16.8*floor(x) [E1,E3,E4,E5]
    #   E5: 18.55..18.99 -> -302.4 = -16.8*18 (floor=18) [E5]
    #   E5: 19.0..19.99 -> -319.2 = -16.8*19 [E5]
    #   E5: 20.0,20.01 -> -336 = -16.8*20 [E5]
    #   E1: 20->-336, 40->-672, 60->-1008, 80->-1344, 100->-1680, 120->-2016 [E1]
    #   So right linear uses floor(x), and starts somewhere in (18.51, 18.55).
    #   Threshold? Maybe x > 18.5? But 18.51 constant. Maybe x >= 18.52? 
    #   Perhaps the rule is floor-based: linear when floor(x) >= 18 AND x > 18.5? 
    #   18.51 floor=18, constant. 18.55 floor=18, linear. So not floor alone.
    #   Maybe threshold is x >= 18.52 or x > 18.51. I'll guess x > 18.51 (?).
    #   Actually maybe the split is at 18.5 + something. E3 18.5 constant, E5 18.51 constant,
    #   18.55 linear. Best guess: x >= 18.52 (?). I'll use x > 18.51.
    out = []
    for x in probe.get("x", []):
        try:
            if x < -5:
                out.append(-0.7 * math.floor(x))
            elif x <= 18.51:
                out.append(-402.3)
            else:
                out.append(-16.8 * math.floor(x))
        except Exception:
            out.append(None)
    return {"y": out}

import math

def predict(probe):
    # Left linear: y = -0.7*floor(x) for x < -10 [E2,E4]
    #   E2: -15..-6 -> 10.5,9.8,...,4.2 = -0.7*floor(x) [E2]
    #   E4: -11.5,-11.2,-11.1 -> 8.4 (floor=-12); -6.5,-6.2,-6.1 -> 4.9 (floor=-7) [E4]
    # Left plateau: y = 7.7 for -10.1 <= x < -10.0? [E3,E4,E6]
    #   E3: -10.9..-10.1 -> 7.7 [E3]
    #   E4: -10.05,-10.02,-10.01 -> 7.7; -9.99,-9.5 -> 7.0 [E4]
    #   E6: -10.55..-10.15 -> 7.7 [E6]
    #   So plateau at 7.7 spans roughly x in [-10.1, -10.0). Below -10.1 linear.
    #   Wait: E2 -10.5 -> 7.7 (floor=-11 -> 7.7). -10.5 is linear value too!
    #   floor(-10.5)=-11, -0.7*-11=7.7. So -10.5 matches both. 
    #   E4 -10.05 -> 7.7: floor=-11 -> 7.7. Also matches linear!
    #   E4 -9.99 -> 7.0: floor=-10 -> 7.0. Matches linear!
    #   So actually left linear -0.7*floor(x) extends through -10 region up to -10.0.
    #   E4 -9.5 -> 7.0: floor=-10 -> 7.0. Matches linear.
    #   So left linear -0.7*floor(x) holds for x < -10.0? Check -10.0 itself.
    #   E3 -10.1 -> 7.7 (floor=-11 ->7.7 ok). No probe exactly -10.0.
    #   Hmm but then where does constant start? E2 -6 -> 4.2 (floor=-6). 
    #   E4 -5.9,-5.5 -> 4.2 (floor=-6). E1 -5 -> -402.32 constant.
    #   So left linear holds until x < -5? But E2 -6 -> 4.2, -5.9 -> 4.2 (floor -6).
    #   E1 -5 -> constant. So boundary between -5.9 and -5.
    #   Wait but E4 -6.1 -> 4.9 (floor=-7), -5.9 -> 4.2 (floor=-6). Consistent linear.
    #   So left linear -0.7*floor(x) for x < -5? Check -5.5 -> floor -6 -> 4.2 ok.
    #   But E1 -5 -> -402.32. So boundary at x = -5: x < -5 linear, x >= -5 constant.
    #   Hmm but earlier v5 used x < -5. Let me recheck E2: -6 -> 4.2 (floor -6, linear ok).
    #   So left linear region is x < -5, NOT x < -10. The 7.7 plateau is just floor values.
    #   Actually -0.7*floor(x) naturally gives 7.7 at floor=-11 (x in [-11,-10)), 
    #   and 7.0 at floor=-10 (x in [-10,-9)). So no separate plateau needed!
    #   The "plateau at 7.7" is just the floor step. Good, simpler.
    # Middle constant: y ~ -402.3 (noisy) for -5 <= x < 18.52 [E1,E2,E3,E5,E6]
    #   E6: 18.515 -> -402.3 (constant); 18.52 -> -302.4 (linear) [E6]
    #   So boundary: x < 18.52 constant, x >= 18.52 linear.
    #   E5: 18.51 constant, 18.55 linear [E5]. E3: 18.5 constant [E3].
    # Right linear: y = -16.8*floor(x) for x >= 18.52 [E1,E3,E4,E5,E6]
    #   E5: 18.55..18.99 -> -302.4 = -16.8*18; 19.0..19.99 -> -319.2 = -16.8*19 [E5]
    #   E1: 20->-336, 40->-672, ... 120->-2016 [E1]
    out = []
    for x in probe.get("x", []):
        try:
            if x < -5:
                out.append(-0.7 * math.floor(x))
            elif x < 18.52:
                out.append(-402.3)
            else:
                out.append(-16.8 * math.floor(x))
        except Exception:
            out.append(None)
    return {"y": out}

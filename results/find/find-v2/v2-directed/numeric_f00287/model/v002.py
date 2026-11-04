import math

def predict(probe):
    # Piecewise structure inferred from E1, E2:
    # - For x <= -10.5: y = -0.7*x (linear). E2: -15->10.5, -14->9.8, -13->9.1, -12->8.4, -11->7.7, -10.5->7.7
    #   Check: -0.7*(-10.5)=7.35, observed 7.7. Hmm, -10.5 gives 7.7 = -0.7*(-11). So boundary is at -11?
    #   -11->7.7 = -0.7*(-11) yes. -10.5->7.7 too. So -10.5 also on linear? -0.7*-10.5=7.35 not 7.7.
    #   Actually -10.5 -> 7.7 matches -0.7*(-11). Maybe boundary at -10.5 with value 7.7 (constant on linear side).
    #   Let's say for x <= -10.5: y = -0.7*x, but -10.5 gives 7.35 not 7.7. So maybe boundary at -11.
    #   E1: -10 -> 7.0 = -0.7*(-10) yes. So -10 is linear! E2: -10.5 -> 7.7 = -0.7*(-11). 
    #   Wait -0.7*(-10.5) = 7.35. Observed 7.7. So -10.5 is NOT on y=-0.7x. But -10 is (7.0).
    #   Contradiction? E1 -10->7.0, E2 -10.5->7.7. If linear y=-0.7x, -10.5->7.35. Observed 7.7.
    #   So maybe slope is -0.7 but boundary... or -10.5 rounds? Let's check -11->7.7 = -0.7*(-11)=7.7 yes.
    #   So -10.5 and -11 both give 7.7. That's odd. Maybe -10.5 is on constant side with value 7.7? No, constant is -402.
    #   Perhaps the linear region extends to x=-10.5 with y=-0.7*x but -10.5 gives 7.35... observed 7.7.
    #   Alternative: slope is -0.7 for x<=-11, and -10.5 is a transition. But -10->7.0 fits -0.7x.
    #   Hmm, -10.5 -> 7.7 = -0.7 * -11. Maybe there's rounding: -10.5 could be -0.7*(-11)? No.
    #   Let's just fit: points -15..-11: y = -0.7x exactly (10.5,9.8,9.1,8.4,7.7). -10.5->7.7 also.
    #   -10->7.0. So -10.5->7.7 breaks -0.7x (would be 7.35). Possibly -10.5 is special/transition.
    #   I'll treat x <= -11 as y=-0.7x, and -10.5 as transition value 7.7 (guess).
    # - For -10.5 < x < 6: constant ~ -402.3 (noisy). E1: -5..10 constant. E2: -9..-6 constant, 6..16 constant.
    #   Wait E2: 6,7,8,9,11,12,13,14,15,16 all ~-402.3! So right linear region starts beyond 16.
    #   E1: 20->-336 = -16.8*20. So right boundary between 16 and 20.
    # - For x >= 20: y = -16.8*x (E1: 20->-336, 40->-672, etc.)
    # - Left linear: x <= -11 (or -10.5): y = -0.7*x
    # - Right linear: x >= 20: y = -16.8*x
    # - Constant middle: -10.5 < x < 20: y ~ -402.3
    # Boundary on right between 16 and 20 (unknown, guess 18?). E2 shows 16 still constant.
    out = []
    for x in probe.get("x", []):
        try:
            if x <= -10.5:
                out.append(-0.7 * x)
            elif x < 20:
                out.append(-402.3)
            else:
                out.append(-16.8 * x)
        except Exception:
            out.append(None)
    return {"y": out}

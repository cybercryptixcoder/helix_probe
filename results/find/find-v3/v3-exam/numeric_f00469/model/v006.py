import math

def predict(probe):
    # Beliefs:
    # - Output is 1.0 exactly on the interval (-2, 1.75) roughly, else 0.0 [E2, E4, E6]
    # - Lower boundary: 1.0 at x=-2, 0.0 at x=-5; E2 shows -2 -> 1, -5 -> 0 [E2]
    # - Upper boundary: 1.0 at 1.75, 0.0 at 1.9; E6 shows 1.75 -> 1, 1.8 -> 0 [E6]
    # - E4: 1.5 -> 1, 1.75 -> 0? Wait E4 says 1.75 -> 0.0, but E6 says 1.75 -> 1.0. Contradiction?
    # Let's re-read carefully.
    #
    # E4: x=[-1.5,-1.25,-1.1,-1.0,-0.9,-0.75,-0.25,0.25,1.5,1.75,1.9,2.0,2.1,2.25,2.5,3.0]
    #     y=[ 1.0,  1.0, 1.0, 1.0, 1.0,  1.0,  1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    # E6: x=[1.55,1.6,1.65,1.7,1.75,1.8,1.85,1.9,1.95,1.99,1.999,0.75,1.25,1.4]
    #     y=[ 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,  0.0, 1.0, 1.0, 1.0]
    #
    # E4 says 1.75 -> 0.0, E6 says 1.75 -> 1.0. These contradict!
    # Unless... the output is noisy? "The output could be noisy."
    # Or perhaps there's something else going on.
    #
    # Let's look at E6 more carefully: 1.55,1.6,1.65,1.7 -> 0; 1.75 -> 1; 1.8,1.85,1.9,1.95,1.99,1.999 -> 0.
    # That's a single spike at 1.75! Interesting.
    # E4: 1.5 -> 1, 1.75 -> 0, 1.9 -> 0.
    # So at 1.5, E4 says 1.0. But E6 has 1.4 -> 1.0, 1.55 -> 0.0.
    # So maybe boundary is between 1.4 and 1.55, with 1.5 being... hmm E4 says 1.5->1.
    #
    # Wait, maybe it's not an interval but something else. Let's look at E2:
    # -128,-100,-75,-50,-25,-10,-5,-2,-1,-0.5,0,0.5,1,2,5,10,25,50,100,128
    # y:  0,   0,   0,  0,  0,  0, 0, 1, 1,  1, 1, 1, 1,0,0, 0, 0, 0,  0,  0
    # So 1.0 at -2,-1,-0.5,0,0.5,1. And 0 at 2.
    # E4: -1.5,-1.25,-1.1,-1.0,-0.9,-0.75,-0.25,0.25 all -> 1.0. So interval includes -1.5 to 0.25.
    # E4: 1.5 -> 1.0, 1.75 -> 0.0.
    # E6: 1.4 -> 1.0, 1.55 -> 0.0, ..., 1.7 -> 0.0, 1.75 -> 1.0, 1.8 -> 0.0.
    #
    # Hmm, 1.75 gives 1.0 in E6 but 0.0 in E4. That's a direct contradiction at the same x.
    # Unless the function is noisy. "The output could be noisy."
    # But all other values are consistent... Let's check: is it possible that the interval is (-2, 1.5) and 1.75 is an outlier?
    # E4: 1.5 -> 1, 1.75 -> 0. E6: 1.4 -> 1, 1.55 -> 0, 1.75 -> 1.
    # If the boundary is at 1.5, then 1.55 -> 0 makes sense. 1.75 -> 0 in E4 makes sense. But E6's 1.75 -> 1 is weird.
    #
    # Maybe the function is something like: 1 if x is in (-2, 1.5) OR x is in some other set?
    # Let's look at E1: 88.2, 66.0, -20.3, -61.7, 2.9, -24.3, 72.7, -50.4, -6.0, 21.3 all -> 0.
    # E3: 1.2 -> 1.0, rest -> 0. 1.2 is in (-2, 1.5). OK.
    # E5: all -> 0. -7.1 -> 0. Hmm, -7.1 is outside (-2, 1.5). OK.
    #
    # So the main interval seems to be roughly (-2, 1.5). Let's check E2: -2 -> 1, 2 -> 0. OK.
    # E4: -1.5 -> 1, 1.5 -> 1, 1.75 -> 0. OK.
    # E6: 1.4 -> 1, 1.55 -> 0. OK. But 1.75 -> 1 in E6 is an anomaly.
    #
    # Could it be noise? A single flipped bit? The problem says "The output could be noisy."
    # If we assume noise, then 1.75 -> 1 in E6 is noise. But E4's 1.75 -> 0 is consistent with boundary at 1.5.
    # So the model: return 1.0 if -2 < x < 1.5 (or maybe <=), else 0.0.
    # Let's check endpoints: E2 has -2 -> 1.0. So -2 is included. E2 has 2 -> 0.0.
    # E4 has 1.5 -> 1.0. E6 has 1.55 -> 0.0. So 1.5 included, 1.55 excluded.
    # Lower: E2 has -2 -> 1.0, -5 -> 0.0. E4 has -1.5 -> 1.0. So lower bound is between -5 and -2, likely -2 inclusive.
    # Check E5: -7.1 -> 0.0, consistent.
    #
    # But wait, what about the 1.75 -> 1.0 in E6? Maybe it's not noise. Maybe there's a second interval?
    # E6: 1.75 -> 1.0. E4: 1.75 -> 0.0. Contradiction. So one of them is noise.
    # Given all other points fit the interval (-2, 1.5], I'll treat 1.75->1 in E6 as noise.
    #
    # Actually, let's reconsider. Could the function be something like: 1 if x is in (-2, 1.5) and x is not a multiple of something? No.
    # Could it be 1 if sin or something? Let's check: -2 to 1.5 is width 3.5. Not obviously periodic.
    #
    # What about the possibility that the function is 1 if x is in (-2, 1.5) OR x is in some other interval?
    # E6: 1.75 -> 1.0. E4: 1.75 -> 0.0. Same x, different results -> noise.
    # So the simplest model: interval (-2, 1.5] or [-2, 1.5]?
    # E2: -2 -> 1.0, so -2 included. E4: 1.5 -> 1.0, so 1.5 included. E6: 1.55 -> 0.0, so 1.5 is upper bound.
    # Lower bound: E2: -2 -> 1.0, -5 -> 0.0. So lower bound is -2.
    # Check E4: -1.5 -> 1.0, consistent.
    #
    # So model: y = 1.0 if -2 <= x <= 1.5 else 0.0.
    # But wait, E6 has 1.75 -> 1.0. If we ignore that as noise, fine.
    # What about 1.5 in E4? 1.5 -> 1.0. E6 has 1.55 -> 0.0. So 1.5 is in, 1.55 is out. Good.
    #
    # Let's double-check E2: -2 -> 1.0. If lower bound is -2 inclusive, good.
    # E2: -5 -> 0.0. Good.
    # E4: -1.5 -> 1.0. Good.
    #
    # So the interval is [-2, 1.5]. But wait, E6 has 1.75 -> 1.0. That's outside. If we include it, we'd need a second interval.
    # But E4 has 1.75 -> 0.0. So it's contradictory. Noise.
    #
    # Could the noise be systematic? Maybe the function is 1 if x is in [-2, 1.5] OR x == 1.75? But E4 says 1.75 -> 0.0. So no.
    #
    # I'll go with: 1.0 if -2 <= x <= 1.5, else 0.0.
    # But let's check E6's 1.75 -> 1.0 again. Is there any pattern? 1.55,1.6,1.65,1.7 -> 0; 1.75 -> 1; 1.8,... -> 0.
    # That's a single spike. Could be a narrow second interval? But E4 has 1.75 -> 0.0. So it's noise.
    #
    # Actually, wait. Let me re-read E4: x=[...1.5,1.75,1.9...] y=[...1.0,0.0,0.0...]
    # E6: x=[...1.7,1.75,1.8...] y=[...0.0,1.0,0.0...]
    # So at 1.75, E4 says 0, E6 says 1. Contradiction. Noise.
    #
    # So the model is simple: indicator of [-2, 1.5].
    # But let's check the lower bound more carefully. E2: -2 -> 1.0. What about -2.1? Not tested.
    # E4: -1.5 -> 1.0. E5: -7.1 -> 0.0. So lower bound is between -7.1 and -2. Likely -2.
    #
    # What about upper bound? E4: 1.5 -> 1.0. E6: 1.55 -> 0.0. So upper bound is between 1.5 and 1.55. Likely 1.5.
    #
    # So: y = 1.0 if -2 <= x <= 1.5 else 0.0.
    #
    # But wait, E2 has -2 -> 1.0 and -5 -> 0.0. What about -2.5? Not tested. I'll assume -2 is the boundary.
    #
    # Let's also consider: could it be (-2, 1.5]? E2: -2 -> 1.0, so -2 is included. So [-2, 1.5].
    #
    # Could it be [-2, 1.5)? E4: 1.5 -> 1.0, so 1.5 included. So [-2, 1.5].
    #
    # I'll go with that.
    #
    # But what about the 1.75 -> 1.0 in E6? If it's not noise, maybe the interval is [-2, 1.5] U {1.75}? But E4 says 1.75 -> 0.0. So no.
    #
    # I'll treat it as noise.
    #
    # So the model is: return 1.0 if -2 <= x <= 1.5 else 0.0.
    #
    # Let me double-check all evidence:
    # E1: all outside -> 0.0. OK.
    # E2: -2 -> 1.0 (in), -1 -> 1.0, ..., 1 -> 1.0, 2 -> 0.0 (out). OK.
    # E3: 1.2 -> 1.0 (in), others out. OK.
    # E4: -1.5 -> 1.0, ..., 1.5 -> 1.0, 1.75 -> 0.0. OK.
    # E5: all out -> 0.0. OK.
    # E6: 1.4 -> 1.0 (in), 1.55 -> 0.0 (out), 1.75 -> 1.0 (out, but says 1.0 -> noise). OK.
    #
    # So the only anomaly is E6's 1.75 -> 1.0.
    #
    # I'll write the model as: 1.0 if -2 <= x <= 1.5 else 0.0.
    #
    # But wait, could the function be something like: 1 if x is in [-2, 1.5] and x is not a multiple of 0.25? No, E4 has -1.5, -1.25, -1.0, -0.75, -0.25, 0.25, 1.5 all -> 1.0.
    #
    # Could it be 1 if x is in [-2, 1.5] and x is not 1.75? That's silly.
    #
    # I'll go with the simple interval.

    result = []
    for x in probe["x"]:
        if x is None:
            result.append(None)
        else:
            if -2 <= x <= 1.5:
                result.append(1.0)
            else:
                result.append(0.0)
    return {"y": result}

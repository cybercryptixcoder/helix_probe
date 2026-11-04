def predict(probe):
    # A: x >= 20: y = -16.8*floor(x) [E1,E2,E3,E5]
    # B: -5 <= x < 20: y = -402.3 (noisy constant) [E2,E3,E6]
    # C: x < -5: y = -0.7*floor(x) [E1,E2,E4,E5,E6]
    # E6: 19.5 -> -319.2 = -16.8*19 (floor(19.5)=19) => positive branch starts at x>=19.5? 
    #   Actually -16.8*floor(19.5)=-16.8*19=-319.2 ✓. And 15.0->-402.3 (region B).
    #   So boundary B/C is between 15 and 19.5. E2: 20->-336 (region A). 
    #   Test: is 19.5 in A? yes. Is 15 in B? yes. Boundary in (15,19.5].
    #   Hmm but E2 has 10->-402.2 and 20->-336. Need finer. Guess boundary at x>=19.5? 
    #   Actually maybe region B is -5<=x<19.5 and A is x>=19.5. But 19.5 gives -319.2 which is A.
    #   Let's say A: x >= 19.5? But 20 works. Need to check if 19.0 is A or B. Unknown.
    #   Wait: maybe the switch is at x >= 19.5? Or maybe region B ends at 19? 
    #   E6 tested 19.5 and got A. So boundary <= 19.5. E6 tested 15 -> B. So boundary in (15,19.5].
    #   Guess: A: x >= 19.5? But then 19.4 would be B. Hmm, or maybe it's x > 19? 
    #   Actually reconsider: maybe region B is -5 <= x <= 19 and A is x >= 19.5? 
    #   Let's use x >= 19.5 for A (mark uncertain).
    #   Actually wait — could the boundary be at 19? -16.8*floor(19)= -319.2 too. 
    #   But 19.5 floor=19 also -319.2. So can't distinguish 19 vs 19.5 from this.
    #   E2 20->-336=-16.8*20. So A includes 20.
    #   Let me guess boundary: A: x >= 19.5 (or x>19). Use x >= 19.5? 
    #   Hmm, but what about x between 19 and 19.5? Unknown. Use x > 19 (i.e. x>=19.5 effectively for tested). 
    #   Actually simplest: A: x >= 19.5. Mark "?".
    import math
    xs = probe["x"]
    ys = []
    for x in xs:
        if x < -5:
            ys.append(-0.7 * math.floor(x))
        elif x < 19.5:
            ys.append(-402.3)
        else:
            ys.append(-16.8 * math.floor(x))
    return {"y": ys}

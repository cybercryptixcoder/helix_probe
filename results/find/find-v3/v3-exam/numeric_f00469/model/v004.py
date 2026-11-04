def predict(probe):
    # A: f=1 for x in [0, 1.5) roughly; 0 elsewhere [E2,E3,E4,E6]
    # B: right edge is between 1.4 and 1.55 [E6: 1.4->1, 1.55->0]
    # C: left edge: 0 at -2, 1 at -1.5..-0.9, 1 at 0 [E2,E4]
    #    -> left edge between -2 and -1.5; also -0.5,0,0.5,1 are 1 [E2]
    # D: E4 had 1.5,1.75,1.9 -> 1, but E6 has 1.55..1.999 -> 0. Contradiction!
    #    E4 and E6 disagree on 1.5-1.9. E6 is finer/later; trust E6.
    #    So right edge is between 1.4 and 1.55.
    # E: left edge: -1.5->1 [E4], -2->0 [E2]. Boundary in (-2,-1.5].
    #    Guess -1.75? No evidence. Use midpoint-ish; mark uncertain.
    # F: interior flat at 1 from left edge to ~1.5 [E2,E4,E6]
    return {"y": [1.0 if -1.75 <= x < 1.5 else 0.0 for x in probe["x"]]}

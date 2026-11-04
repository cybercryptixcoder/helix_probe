def predict(probe):
    # A: f=1 on an interval around 0, 0 outside [E2,E4,E5,E7]
    # B: right edge: 1.5->1, 1.52->0 [E8]; sharp step in (1.5,1.52]
    # C: left edge: -1.5->1 [E4], -2->0 [E2]; in (-2,-1.5]
    # D: interior flat at 1 [E2,E4,E6,E8]
    return {"y": [1.0 if -1.75 <= x <= 1.51 else 0.0 for x in probe["x"]]}

def predict(probe):
    # f(x) = floor(x) - 39 for all tested x [E1]
    # Check: 88.2->49 (88-39=49) yes; 66->27 yes; -20.3->-60 (-21-39=-60) yes
    # -61.7->-101 (-62-39=-101) yes; 2.9->-37 (2-39=-37) yes; -24.3->-64 (-25-39=-64) yes
    # 72.7->33 (72-39=33) yes; -50.4->-90 (-51-39=-90) yes; -6->-45 (-6-39=-45) yes
    # 21.3->-18 (21-39=-18) yes
    import math
    out = []
    for x in probe.get("x", []):
        try:
            out.append(math.floor(x) - 39)
        except Exception:
            out.append(None)
    return {"y": out}

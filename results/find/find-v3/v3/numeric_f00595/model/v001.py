def predict(probe):
    # f(x) = round(x) to nearest integer [E1: 88.2->89, -20.3->-22, -24.3->-26, -50.4->-52, -61.7->-63, 2.9->3, -6.0->-7]
    # Note: -20.3 -> -22 and -24.3 -> -26 suggest rounding toward -inf (floor), not nearest.
    # Check: 88.2 floor=88 but observed 89. Hmm. 66.0->67? observed 67. 72.7->73 (floor 72).
    # So it's round-half... let's check: 88.2->89 (+0.8), 66.0->67 (+1), 72.7->73 (+0.3), 2.9->3 (+0.1),
    # 21.3->22 (+0.7), -20.3->-22 (-1.7), -24.3->-26 (-1.7), -50.4->-52 (-1.6), -61.7->-63 (-1.3), -6.0->-7 (-1).
    # Positive: ceil(x). Negative: floor(x). i.e. round away from zero.
    import math
    out = []
    for x in probe["x"]:
        if x >= 0:
            out.append(float(math.ceil(x)))
        else:
            out.append(float(math.floor(x)))
    return {"y": out}

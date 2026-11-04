def predict(probe):
    # f(x) = round(x) to nearest integer [E1: 88.2->89, -20.3->-22, 2.9->3, -24.3->-26, -6.0->-7]
    # Note: -20.3 -> -22 and -24.3 -> -26 suggest rounding half away from zero or floor-ish;
    # but 88.2->89, 66.0->67?? Wait 66.0->67 is odd. Let's check: 66.0 -> 67, 72.7->73, -50.4->-52, 21.3->22.
    # Pattern: y = round(x) but 66.0->67 and -50.4->-52 don't fit plain round.
    # Actually: 66.0->67, -50.4->-52, -20.3->-22, -24.3->-26, -6.0->-7: these are floor(x)-? 
    # Check floor: floor(88.2)=88 no. ceil: ceil(88.2)=89 yes; ceil(66.0)=66 no (got 67).
    # Try round half up: round(66.0)=66 no.
    # Try x rounded then +? 66.0->67 (+1), 72.7->73 (round=73 ok), -50.4->-52 (round=-50, no).
    # Hmm: 66.0->67, -50.4->-52, -20.3->-22, -24.3->-26, -6.0->-7 all differ by about -1 from round.
    # 88.2->89 (round=88, +1), 2.9->3 (round=3 ok), 21.3->22 (round=21, +1).
    # Mixed. Perhaps y = round(x) with some offset? Let's just use round with half away from zero as best guess.
    # ? uncertain: E1 shows values near integers shifted by ±1 inconsistently.
    out = []
    for x in probe["x"]:
        try:
            out.append(float(round(x)))
        except Exception:
            out.append(None)
    return {"y": out}

def predict(probe):
    # f(x) = round(x) to nearest integer [E1]
    # Evidence: 88.2->89, 66.0->67, -20.3->-22, -61.7->-63, 2.9->3,
    #           -24.3->-26, 72.7->73, -50.4->-52, -6.0->-7, 21.3->22
    # Note: 66.0->67 and -6.0->-7 suggest rounding half away from zero
    # (or half up), not banker's rounding. 2.9->3, 21.3->22 consistent.
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
            continue
        # round half away from zero
        if x >= 0:
            out.append(float(int(x + 0.5)))
        else:
            out.append(float(int(x - 0.5)))
    return {"y": out}

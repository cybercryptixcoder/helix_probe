def predict(probe):
    # f(x) = x for |x| <= 2 [E1]
    # f(x) = round(x) for 2 < |x| <= 4 [E2: -4->-4, -3.5->-3, -3->-3, -2.5->-2, -2.1->-2, 2.1->3, 2.5->3, 3->3, 3.5->4, 4->4]
    # f(x) = 0 for |x| > 4 [E1: -5,-10,... -> 0]
    # "?" exact boundary between 4 and 5 unknown; assume |x| <= 4 for the rounding region.
    out = []
    for x in probe.get("x", []):
        try:
            if -2 <= x <= 2:
                out.append(float(x))
            elif -4 <= x <= 4:
                # round half away from zero to match observed values
                import math
                out.append(float(math.floor(x + 0.5)) if x >= 0 else float(math.ceil(x - 0.5)))
            else:
                out.append(0.0)
        except Exception:
            out.append(None)
    return {"y": out}

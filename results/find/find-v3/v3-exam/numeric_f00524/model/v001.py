def predict(probe):
    # Hypothesis: f(x) = round(x) if x is in some interval, else 0.
    # E1: x=2.9 -> 3.0; all other values -> 0.0.
    # The nonzero output at 2.9 suggests rounding near small integers,
    # but only 2.9 produced a nonzero. Simplest guess: f(x)=round(x) when
    # |x| < some small threshold, else 0. But 2.9 rounds to 3, and -6.0 -> -0.0,
    # 21.3 -> 0.0. So the active region is narrow around small x.
    # ? Best guess: f(x) = round(x) if -3 <= x <= 3 else 0.
    out = []
    for x in probe["x"]:
        if -3.0 <= x <= 3.0:
            out.append(float(round(x)))
        else:
            out.append(0.0)
    return {"y": out}

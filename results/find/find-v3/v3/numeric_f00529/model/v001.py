def predict(probe):
    # Outputs cluster at -6.9 and -7.9 [E1]
    # 2.9 -> -6.9015, slightly off from -6.9, suggesting a smooth function near a threshold [E1]
    # Sign pattern: positive x -> -6.9, negative x -> -7.9, except 2.9 special [E1]
    # Hypothesis: f(x) = -7.9 + 1.0 * (x > 0), with a smooth transition near 0
    # The 2.9 value -6.9015 suggests transition: maybe -7.9 + 1.0*step(x) plus small correction
    # Try: f(x) = -7.9 + (1.0 if x>0 else 0) but 2.9 gives -6.9015 not -6.9
    # Perhaps f(x) = -7.9 + 1/(1+exp(-k*x))? At x=2.9, sigmoid ~ -6.9015 means sigmoid=0.9985
    # sigmoid(2.9*k)=0.9985 -> 2.9k=6.5 -> k~2.24. Check x=21.3: sigmoid(47.7)=1 -> -6.9 ok
    # x=-6: sigmoid(-13.4)~0 -> -7.9 ok. x=-20.3: ok. x=-24.3: ok. x=-50: ok.
    # x=66,88: ok. x=-61.7: ok. x=72.7: ok.
    import math
    out = []
    for x in probe["x"]:
        try:
            s = 1.0/(1.0+math.exp(-2.24*x))
            out.append(-7.9 + 1.0*s)
        except OverflowError:
            out.append(-6.9 if x>0 else -7.9)
    return {"y": out}

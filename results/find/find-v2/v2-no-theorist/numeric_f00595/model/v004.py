def predict(probe):
    # f(x) = ceil(x) for x > 0, except on the interval (38, 42) where it returns a small negative value [E1-E14]
    # f(x) = floor(x) - 1 for x < 0 [E1-E14]
    # f(0) = -1 [E2,E4,E6,E10]
    # On (38, 42): f returns a small negative value (~ -0.3 to -0.6), seemingly random/noisy [E14]
    #   At x=40 exactly: -0.5542 [E12]; elsewhere in (38,42) similar small negatives [E14]
    #   Boundary: 38 and 42 are NOT in the interval (they follow ceil: 38->39? no...)
    #   Wait: E14 shows 38.0 -> -0.5361, 42.0 -> -0.365. So 38 and 42 ARE in the interval.
    #   But 37.0 -> -0.3305 and 43.0 -> 44.0. So interval is [38, 42] inclusive? 
    #   E14: 37->-0.3305 (in!), 43->44 (out). So lower bound <=37, upper bound between 42 and 43.
    #   Actually 35->-0.35, 36->-0.6257, 37->-0.3305 all negative. 43->44 out.
    #   So interval extends below 35. Need to find lower boundary. Unknown - mark with ?
    #   Upper boundary: 42 in, 43 out. So upper bound in (42, 43].
    #   Since we lack lower bound data, guess interval is (some lower, 42.5]? 
    #   But E12 had 40 -> -0.5542 and 50 -> 51 (out). E14 shows 35-42 all in.
    #   Best guess: interval is [?, 42.5]. Lower bound unknown; assume it's a wide region.
    #   Actually reconsider: maybe the "anomaly" is a whole band. Let's say x in [a, 42.5] for some a.
    #   Without data below 35, guess a = 30? E12: 30 -> 31 (out!). So a > 30.
    #   E14: 35 in. So a in (30, 35]. Guess a = 34? Mark uncertain.
    #   Use: 34 <= x <= 42.5 -> small negative (noisy, return -0.5 as placeholder)
    import math
    out = []
    for x in probe["x"]:
        if 34 <= x <= 42.5:  # ? lower bound uncertain (between 30 and 35)
            out.append(-0.5)  # ? noisy small negative; exact value unpredictable
        elif x > 0:
            out.append(math.ceil(x))
        elif x < 0:
            out.append(math.floor(x) - 1)
        else:
            out.append(-1)
    return {"y": out}

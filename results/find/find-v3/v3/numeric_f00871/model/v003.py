def predict(probe):
    # f(x) = 5.2 - 2.5*x on [-1, 1], else 0 [E2]
    # E3: x=1.2 -> 2.2. Extends linear rule beyond 1: 5.2-2.5*1.2=2.2 ✓
    # So the linear region is wider than [-1,1]; boundary unknown.
    # E2: x=3.14159 -> 0, x=-2.71828 -> 0. So boundary is between 1.2 and 2.71828.
    # Guess: linear on [-2, 2]? But -2.71828 -> 0 fits. Try |x| < 2.5?
    # Actually try: linear where 5.2-2.5x would be... check sign? 
    # At x=2.08, value=0. Maybe region is where value > 0? 
    # x=1.2->2.2>0 ✓, x=3.14-> 5.2-7.85<0 -> 0 ✓, x=-2.718-> 5.2+6.8>0 but observed 0. So no.
    # Symmetric cutoff: |x| <= 2 gives x=1.2 in, x=2.718 out, x=-2.718 out. Consistent.
    # Guess boundary at |x| <= 2 (?)
    out = []
    for x in probe["x"]:
        if -2.0 <= x <= 2.0:
            out.append(5.2 - 2.5 * x)
        else:
            out.append(0.0)
    return {"y": out}

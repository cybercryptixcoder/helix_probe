import math

def predict(probe):
    # A: f is deterministic in x (tiny noise ~1e-4) [E1,E2]
    # B: For |x| >= ~5, y is a smooth function of x, asymmetric in sign [E1,E3,E4]
    #    - large positive x: y ≈ -16.6*x  (e.g. 88.9->-1478.4, 114->-1915.2) [E1,E3]
    #    - large negative x: y ≈ -0.70*x  (e.g. -93.6->65.8, -120.7->84.7) [E1,E3]
    #    - x=-12 -> 8.4, x=-8 -> 5.6, x=12 -> -402.258 (!!) [E4]
    # C: For |x| <= ~5, y is essentially constant ≈ -402.4 (a plateau, not a pole!) [E4]
    #    x in {-5,-3,-2,-1.5,-1,-0.5,0.5,1,1.5,2,3,5} all give ~-402.3 to -402.6 [E4]
    #    So the "spike" is actually a flat plateau of value ~-402.4 on |x|<=5.
    # D: Transition: x=-8 -> 5.6 (linear regime), x=-5 -> -402.2 (plateau). So boundary ~5-8.
    #    x=12 -> -402.258 is odd: positive side still plateau at 12? But x=38.8 -> -638.4 linear.
    #    So positive-side boundary is between 12 and 38.8. Negative-side boundary between 5 and 8.
    #    Asymmetric boundaries. Let's model: plateau on [-5, 12]? Check x=-12 -> 8.4 (outside), x=-8->5.6 (outside).
    #    x=12 -> -402.258 (inside plateau). x=5 -> -402.232 (inside). x=8 -> -402.3722 (inside!).
    #    Wait x=8 -> -402.3722 is plateau. x=-8 -> 5.6 is linear. So positive boundary >8, negative boundary <8.
    #    x=12 -> -402.258 plateau. So positive boundary between 12 and 38.8.
    #    Negative: x=-5 plateau, x=-8 linear. Boundary between -8 and -5.
    # E: Linear regime fit:
    #    negative x (x<=-8): y ≈ -0.703*x  (-12->8.4: 8.4/-12=-0.70; -8->5.6: -0.70) [E1,E4]
    #    positive x (x>=~38): y ≈ -16.6*x  (38.8->-638.4: -16.45; 88.9->-16.63) [E1,E3]
    #    Use y = -x*(c + d*tanh(x)) with c+d=16.6, c-d=0.703 -> c=8.65, d=7.95 [E1,E3]
    #    Check x=38.8: tanh~1, factor 16.6, y=-644 (obs -638.4, ok); x=-12: factor 0.70, y=8.4 good.
    # F: Plateau value ~ -402.4 (mean of E4 plateau points) [E4]
    # G: Boundaries (?) : plateau for -5 < x < ~20 (guess upper between 12 and 38.8)
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None); continue
        try:
            if -5.0 < x < 20.0:  # ? plateau region, boundaries uncertain
                y = -402.4
            else:
                y = -x*(8.65 + 7.95*math.tanh(x))
        except Exception:
            y = None
        out.append(y)
    return {"y": out}

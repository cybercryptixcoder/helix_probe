import math

def predict(probe):
    # A: deterministic in x [E1,E2]
    # B: plateau value ~-402.4 for |x| small [E4]
    # C: negative boundary: plateau for x>-5, linear for x<=-8; boundary in (-8,-5) [E4]
    #    negative linear: y ≈ -0.703*x  (x=-8->5.6, x=-12->8.4) [E1,E4]
    # D: positive boundary: plateau through x=18, linear from x=19 [E6]
    #    x=19->-319.2, 20->-336, 22->-369.6, 24->-403.2, 26->-436.8, 28->-470.4, 30->-504, 32->-537.6, 34->-571.2
    #    slope: (-571.2+319.2)/(34-19)= -252/15 = -16.8; intercept: -319.2+16.8*19 = 0
    #    so y = -16.8*x for x>=19 [E6]
    #    check x=38.8: -16.8*38.8=-651.8 vs obs -638.4 (close-ish); x=88.9: -1493.5 vs -1478.4
    #    slope slightly less: use -16.6? -16.6*19=-315.4 vs -319.2. -16.8 fits E6 exactly.
    #    Use -16.8 for x>=19 (E6 exact), accept slight error at large x.
    # E: positive boundary between 18 and 19 [E6]
    # F: negative boundary between -8 and -5; use -6.5 (?) [E4]
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None); continue
        try:
            if x >= 19.0:
                y = -16.8 * x
            elif x <= -6.5:
                y = -0.703 * x
            else:
                y = -402.4
        except Exception:
            y = None
        out.append(y)
    return {"y": out}

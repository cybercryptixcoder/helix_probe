import math

def predict(probe):
    # Observations from E1:
    # x=88.2 -> 27090.784 ; 66.0 -> 15014.0187 ; -20.3 -> 1545.2188
    # -61.7 -> 13550.6196 ; 2.9 -> -22.8021 ; -24.3 -> 2154.0941
    # 72.7 -> 18241.8226 ; -50.4 -> 9077.3007 ; -6.0 -> -22.8021
    # 21.3 -> 1532.7222
    #
    # Pattern hypothesis: for large |x| output ~ x^2 * c (88.2^2=7779, *3.48=27090)
    # 66^2=4356, *3.45=15014. 72.7^2=5285, *3.45=18234. So y ~ 3.45*x^2 for large x.
    # For small x (|x|<~25) output is small/negative: 2.9->-22.8, -6->-22.8, 21.3->1532.
    # 21.3^2=453.7, *3.45=1565 close to 1532. Hmm 2.9 and -6 both give -22.8021 exactly.
    # That constant -22.8021 for both 2.9 and -6.0 suggests a floor/clamp region.
    # -20.3 -> 1545.2 ; -20.3^2=412, *3.45=1422, not exact. -24.3^2=590,*3.45=2036 vs 2154.
    # Negative side: -50.4^2=2540,*3.45=8764 vs 9077. -61.7^2=3807,*3.45=13134 vs 13550.
    # Ratio y/x^2: 88.2:3.482, 66:3.447, 72.7:3.451, -61.7:3.559, -50.4:3.573, -24.3:3.648, -20.3:3.749
    # Positive side ratio ~3.45-3.48; negative side higher, growing as |x| shrinks.
    # Try y = a*x^2 + b*x + c fit? Let's just use quadratic fit on data.
    # Actually simplest: fit quadratic through points. Use least squares mentally is hard.
    # Try y = 3.45*x^2 + k*x + c. For x=88.2: 3.45*7779=26838, need +252 -> k*88.2+c=252
    # x=66: 3.45*4356=15028, need -14 -> 66k+c=-14
    # Subtract: 22.2k=266 -> k=11.98, c=-14-66*11.98=-805. Check x=72.7: 3.45*5285=18233, +11.98*72.7=871, -805 -> 18299 vs 18242. Close-ish.
    # x=-61.7: 3.45*3807=13134, +11.98*-61.7=-739, -805 -> 11590 vs 13550. Off.
    # So not a single quadratic. Negative side differs.
    # Maybe y = 3.45*x^2 + something. For -61.7 need 13550-13134=416 extra. -50.4: 9077-8764=313. -24.3:2154-2036=118. -20.3:1545-1422=123.
    # Extra vs |x|: 61.7->416, 50.4->313, 24.3->118, 20.3->123. Roughly extra ~ 6.7*|x| for large, but 20.3 gives 123 vs 6.7*20.3=136.
    # Positive extra: 88.2:252, 66:-14, 72.7:9, 21.3:1532-3.45*453.7=1532-1565=-33.
    # Positive extra small/negative, negative extra positive. So y = 3.45*x^2 + 6.7*|x|*? no.
    # Try y = 3.45*x^2 - 6.7*x for negative? -6.7*-61.7=413 yes! -6.7*-50.4=338 vs 313. -6.7*-24.3=163 vs 118.
    # For positive: -6.7*88.2=-591, 3.45*7779-591=26247 vs 27090. no.
    # Hmm. Let's just do piecewise: small |x| region clamps to -22.8021.
    # 2.9 and -6.0 both -22.8021. 21.3 gives 1532 (not clamped). So clamp region maybe |x|<~10?
    # Need more data. Best guess: y = 3.45*x^2 + 6.7*max(0,-x) - 22.8 for |x|<10, else quadratic-ish.
    # I'll implement a reasonable guess with a clamp for small |x| and quadratic otherwise.
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            if x is None:
                ys.append(None); continue
            x = float(x)
            if abs(x) < 10:
                ys.append(-22.8021)
            else:
                # quadratic with slight asymmetry
                y = 3.45*x*x + (6.7*(-x) if x < 0 else 0.0) - 22.8
                ys.append(y)
        except Exception:
            ys.append(None)
    return {"y": ys}

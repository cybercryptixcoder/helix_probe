import math

def predict(probe):
    # Left linear region: y = -0.7*x for x <= -10.5 [E1,E2,E3]
    #   E3: -10.9..-10.1 all give 7.7 (constant 7.7, not -0.7x). So left linear ends at -11.
    #   E2: -11 -> 7.7 = -0.7*(-11). -10.5 -> 7.7 too (so -10.5 is NOT on -0.7x; it's in a flat 7.7 zone).
    #   E3: -10.9..-10.1 -> 7.7. So there is a flat zone at y=7.7 from about -11 to -10 (or beyond).
    #   E1: -10 -> 7.0 = -0.7*(-10). So -10 is back on the line! 
    #   So: x <= -11: y=-0.7x; -11 < x < -10: y=7.7 (flat); x=-10: y=7.0.
    #   Wait E1 -10->7.0, E3 -10.1->7.7. So flat zone is (-11, -10), and at -10 it's 7.0.
    #   Actually -10.1 -> 7.7 but -10 -> 7.0. Boundary between -10.1 and -10.
    #   Hmm, maybe the flat zone is a "clamp" at 7.7 for x in (-11, -10)? Let's model: 
    #   x <= -11: -0.7x ; -11 < x <= -10.1: 7.7 ; x >= -10: -0.7x? But -10->7.0=-0.7*-10 yes.
    #   But then -5..-1 are constant -402. So between -10 and -5 there's a transition.
    #   E1: -10->7.0, -5->-402.3. So somewhere between -10 and -5 it drops to constant.
    #   E2: -9->6.3=-0.7*-9, -8->5.6, -7->4.9, -6->4.2. So -9..-6 are STILL on -0.7x!
    #   So left linear extends to -6 at least. E1 -5->-402.3. So boundary between -6 and -5.
    #   E2: -6->4.2=-0.7*-6. So x<=-6: -0.7x. x>=-5: constant.
    #   But then what about -10.5, -10.9..-10.1 giving 7.7? -0.7*-10.5=7.35, -0.7*-10.9=7.63. Observed 7.7.
    #   So there's a flat 7.7 plateau around -11..-10.1, then back to -0.7x for -10..-6.
    #   That's weird. Maybe it's a clamp: y = min(-0.7x, 7.7)? For x<=-11, -0.7x>=7.7, so min gives 7.7. 
    #   Check: x=-15: -0.7*-15=10.5, min(10.5,7.7)=7.7. But observed 10.5! So no.
    #   Maybe max? No.
    #   Alternative: the flat 7.7 is a separate small plateau. Let's just encode it.
    #   Actually maybe rounding: -10.5 -> 7.7 could be -0.7*-11 rounded? Unlikely.
    #   Let's hypothesize: for -11 <= x <= -10, y=7.7 (a flat step). Elsewhere on left, -0.7x.
    #   E3 confirms -10.9..-10.1 -> 7.7. E1 -10->7.0. So plateau is [-11,-10) roughly.
    #   I'll use: -11 <= x < -10: 7.7 ; x <= -11 or (-10 <= x <= -6): -0.7x.
    # Constant middle: -6 < x < 19: y ~ -402.3 [E1,E2,E3]
    #   E3: 16.5..18.5 -> -402.3; 19,19.5 -> -319.2. So right boundary between 18.5 and 19.
    #   -319.2 / 19 = -16.8. So 19 is on right linear! 19.5: -16.8*19.5=-327.6, observed -319.2. 
    #   Hmm -319.2 = -16.8*19. So 19.5 also gives -319.2? That's flat at -319.2?
    #   E1: 20->-336=-16.8*20. So 20 on line. 19.5->-319.2=-16.8*19. 
    #   So maybe right linear starts at 19, and 19.5 is... -16.8*19.5=-327.6 not -319.2.
    #   So 19 and 19.5 both -319.2. Flat plateau at -319.2 for [19,19.5]? Then 20 on line.
    #   Similar to left plateau! Maybe clamp: y = max(-16.8x, -319.2)? For x>=19, -16.8x<=-319.2, max gives -319.2. 
    #   Check x=20: -16.8*20=-336, max(-336,-319.2)=-319.2. But observed -336! So no.
    #   Maybe min? min(-336,-319.2)=-336. x=19: min(-319.2,-319.2)=-319.2. x=19.5: min(-327.6,-319.2)=-327.6, observed -319.2. No.
    #   So it's a flat plateau at -319.2 for [19,19.5], then line from 20.
    #   Let's just encode: 19 <= x < 20: -319.2 ; x >= 20: -16.8x.
    # Right linear: x >= 20: y = -16.8*x [E1]
    out = []
    for x in probe.get("x", []):
        try:
            if -11 <= x < -10:
                out.append(7.7)
            elif x <= -6:
                out.append(-0.7 * x)
            elif x < 19:
                out.append(-402.3)
            elif x < 20:
                out.append(-319.2)
            else:
                out.append(-16.8 * x)
        except Exception:
            out.append(None)
    return {"y": out}

def predict(probe):
    # Left region x < -5: f(x) = -0.7 * floor(x)  [E5: -48.6->34.3, -7.1->5.6, -16.9->11.9, -102.2->72.1; E8: -6.5->4.9, -6.25->4.9, -6.1->4.9, -6.0->4.2, -5.9..-5.1->4.2]
    #   E8 confirms floor: -6.5..-6.1 all -> 4.9 = -0.7*(-7); -6.0..-5.1 -> 4.2 = -0.7*(-6).
    # Flat region -5 <= x < 18.55: f ~ -402.3 (noisy, constant mean)  [E4,E6,E10,E12]
    #   E8: -5.0 -> -402.2471 (flat). So left/flat boundary at x = -5.
    #   E12: 18.5 -> -402.3403 (flat), 18.55 -> -302.4 (right). So flat/right boundary in (18.5, 18.55].
    #   Guess boundary = 18.55? Actually 18.55 already right. So T in (18.5, 18.55]. Pick 18.55? 
    #   But 18.5 flat and 18.55 right -> T = 18.55 (x >= 18.55 right)? Or T somewhere in (18.5,18.55].
    #   Let's pick T = 18.55 as the start of right region (x >= 18.55). ?
    # Right region x >= 18.55: f(x) = -16.8 * floor(x)  [E2,E3,E4,E5,E6,E12]
    #   E12: 18.55..18.9 -> -302.4 = -16.8*18; 19.0,19.1 -> -319.2 = -16.8*19.
    import math
    out = []
    for x in probe.get("x", []):
        try:
            if x < -5:
                y = -0.7 * math.floor(x)
            elif x < 18.55:
                y = -402.3
            else:
                y = -16.8 * math.floor(x)
        except Exception:
            y = None
        out.append(y)
    return {"y": out}

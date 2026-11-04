def predict(probe):
    # Piecewise-constant with a spike at 0.
    # Boundaries appear to be at -5 and 5, but E3 shows the transition is
    # shifted: -4.9999 -> 8.8 and 4.99 -> -12.4, while -5.0001 -> 8.8 and 5.0001 -> -12.4.
    # So the left boundary is at -5 (x<=-5 -> 8.8), and the right boundary is at 5
    # but 4.99 already gives -12.4, so the upper region starts at ~4.99? 
    # Re-examine E3:
    #   -5.0001 -> 8.8   (x <= -5 region)
    #   -4.9999 -> 8.8   (still 8.8! so boundary is not exactly -5)
    #   -5.01   -> 8.8
    #   -4.99   -> 8.8   (still 8.8!)
    # So the 8.8 region extends past -5 up to somewhere between -4.99 and -2.1.
    # E2: -4.9 -> 8.8, -2.1 -> 9.8. So boundary between -4.9 and -2.1.
    # E3: -4.99 -> 8.8. So boundary is between -4.99 and -2.1.
    # Hmm, but E1: -5 -> 8.8, -2 -> 9.8.
    # The 9.8 region: E2 -2.1,-1.9,... -> 9.8; E3 -0.0001 -> 9.8.
    # Right side: E3 4.99 -> -12.4, 4.9999 -> -12.4, 5.0001 -> -12.4.
    # E2: 4.9 -> -12.4, 5.1 -> -12.4. E1: 5,10,... -> -12.4.
    # So -11.4 region: E1 0.5,1,2 -> -11.4; E2 0.01..2.1 -> -11.4; E3 0.0001 -> -11.4.
    # Boundary between -11.4 and -12.4 is between 2.1 and 4.9.
    # Let's guess boundaries at -5 and 5 but E3 contradicts: -4.9999 -> 8.8 means
    # the 8.8 region includes values > -5. And 4.99 -> -12.4 means -12.4 includes < 5.
    # Perhaps boundaries are at -4.99? and 4.99? Let's use: x < -4.99 -> 8.8? 
    # But -4.99 -> 8.8 too. So 8.8 for x <= -4.99. And -11.4 for x < 4.99? 4.99 -> -12.4.
    # So -11.4 for 0 < x < 4.99, -12.4 for x >= 4.99.
    # Left: 8.8 for x <= -4.99, 9.8 for -4.99 < x < 0.
    # Check E2: -4.9 -> 8.8? That contradicts x <= -4.99. Hmm -4.9 > -4.99 so would be 9.8, but observed 8.8.
    # So boundary is between -4.9 and -2.1, and -4.99 -> 8.8, -4.9999 -> 8.8.
    # Maybe boundary at -4.5? -4.9 -> 8.8, -2.1 -> 9.8. Use -4.5? uncertain.
    # Actually maybe the step is at -5 but with a small offset/rounding. 
    # Let's pick: 8.8 for x < -4.95 (covers -4.99, -4.9999, -5.0001, -5.01, -4.9? -4.9 > -4.95 no).
    # -4.9 -> 8.8 so boundary must be > -4.9. Between -4.9 and -2.1.
    # Guess -4.5? No evidence. Use midpoint-ish -4.5? Mark uncertain.
    # Right: -11.4 for 0 < x < 4.95 (covers 4.9 -> -12.4? no, 4.9 -> -12.4).
    # 4.9 -> -12.4 so boundary <= 4.9. 2.1 -> -11.4 so boundary > 2.1.
    # Guess boundary at 4.5? uncertain.
    out = []
    for x in probe.get("x", []):
        try:
            if x == 0:
                y = 1548.92
            elif x <= -4.5:      # ? boundary between -4.9 and -2.1
                y = 8.8
            elif x < 0:
                y = 9.8
            elif x < 4.5:        # ? boundary between 2.1 and 4.9
                y = -11.4
            else:
                y = -12.4
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}

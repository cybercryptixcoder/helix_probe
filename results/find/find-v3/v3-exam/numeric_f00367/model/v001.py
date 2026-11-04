def predict(probe):
    # Linear through origin: y = 2.42 * x [E1]
    # Check: 88.2*2.42=213.444~213.48; 66*2.42=159.72~160.2; -20.3*2.42=-49.1? no...
    # Recheck ratios: 213.48/88.2=2.4204; 160.2/66=2.4273; -37.02/-20.3=1.8236? no
    # -136.38/-61.7=2.2104; 8.76/2.9=3.0207; -46.62/-24.3=1.9185
    # Ratios vary -> not pure linear. Try y = x + something? 
    # 213.48-88.2=125.28; 160.2-66=94.2; -37.02+20.3=-16.72
    # Try y = 2.42*x rounded? 2.9*2.42=7.018 vs 8.76 no.
    # Look: 8.76 = 3*2.92? 2.9*3=8.7 close. -2.7 = -6*0.45? 
    # 52.92/21.3=2.4845; 176.28/72.7=2.4248; -109.26/-50.4=2.1679
    # Hmm. Try y = 2.42*x + small? 2.9->7.018 vs 8.76 diff 1.74
    # Maybe y = x*2.42 but with rounding to 2 decimals of x*2.42? 
    # 2.9*2.42=7.018 not 8.76.
    # Try y = 2.42*x + 0.6*sin? unlikely.
    # Look at -6.0 -> -2.7: ratio 0.45. 2.9->8.76 ratio 3.02. Wild.
    # Maybe piecewise. -6 gives -2.7. 2.9 gives 8.76.
    # Try y = x*2.42 for |x|>10, else something?
    # -20.3*2.42=-49.1 vs -37.02 no.
    # Try y = 2.42*x - 12? -20.3: -49.1-12=-61 no.
    # Let's fit: differences. Maybe y = 2.42*x rounded to nearest 0.06?
    # 88.2*2.42=213.444 -> 213.48 diff .036
    # 66*2.42=159.72 -> 160.2 diff .48
    # Try y = 2.42*x + 0.06*round? 
    # Alternative: y = 2.42*x but x snapped? 
    # 66 -> 160.2 = 2.4273*66. 88.2->2.4204. 
    # Maybe y = 2.42*x + 0.06*sin(x)? 66: sin=~ -0.026 -> -0.0016 no.
    # Try y = 2.42*x + 0.06*cos? 
    # Actually 160.2 = 2.42*66 + 0.48. 213.48=2.42*88.2+0.036.
    # Hmm 0.48 vs 0.036.
    # Try y = 2.42*x + 0.06*floor(x/?)...
    # Let's just try y = 2.42*x and see residuals:
    # 88.2: 213.444 res .036
    # 66: 159.72 res .48
    # -20.3: -49.126 res 12.106
    # -61.7: -149.314 res 12.934
    # 2.9: 7.018 res 1.742
    # -24.3: -58.806 res 12.186
    # 72.7: 175.934 res .346
    # -50.4: -121.968 res 12.708
    # -6: -14.52 res 11.82
    # 21.3: 51.546 res 1.374
    # Residuals ~12 for negatives, ~0-1 for positives large, ~1.7 for small positive.
    # Looks like y = 2.42*x + 12 for x<0? -20.3: -49.126+12=-37.126 vs -37.02 close!
    # -61.7: -149.314+12=-137.314 vs -136.38 close
    # -24.3: -58.806+12=-46.806 vs -46.62
    # -50.4: -121.968+12=-109.968 vs -109.26
    # -6: -14.52+12=-2.52 vs -2.7
    # Slight off. Maybe y = 2.42*x + 12.2? -6: -2.32 no.
    # Try y = 2.42*x + 12.24? -6: -2.28.
    # Residuals for negatives: 12.106,12.934,12.186,12.708,11.82. avg ~12.35
    # Hmm not constant. Maybe y = 2.42*x + 12.35? 
    # Actually maybe it's y = 2.42*x + 12.24*sign? no.
    # Let's try exact: -6 -> -2.7. If y=2.42x+c: -14.52+c=-2.7 => c=11.82
    # -20.3: -49.126+11.82=-37.306 vs -37.02
    # Not exact. Maybe slope differs.
    # Fit two points -6,-2.7 and -20.3,-37.02: slope=(-37.02+2.7)/(-20.3+6)=(-34.32)/(-14.3)=2.4
    # intercept: -2.7=2.4*(-6)+c => c=11.7
    # Check -61.7: 2.4*-61.7+11.7=-148.08+11.7=-136.38 YES!
    # Check -24.3: 2.4*-24.3+11.7=-58.32+11.7=-46.62 YES!
    # Check -50.4: 2.4*-50.4+11.7=-120.96+11.7=-109.26 YES!
    # So for x<0: y = 2.4*x + 11.7
    # For x>0: 88.2->213.48: slope? 66->160.2. slope=(213.48-160.2)/(88.2-66)=53.28/22.2=2.4
    # intercept: 160.2=2.4*66+c => c=1.8
    # Check 72.7: 2.4*72.7+1.8=174.48+1.8=176.28 YES!
    # Check 21.3: 2.4*21.3+1.8=51.12+1.8=52.92 YES!
    # Check 2.9: 2.4*2.9+1.8=6.96+1.8=8.76 YES!
    # So piecewise: x<0: 2.4x+11.7; x>=0: 2.4x+1.8
    # Boundary at 0. Discontinuity: at 0- gives 11.7, at 0+ gives 1.8.
    out = []
    for x in probe["x"]:
        if x < 0:
            out.append(round(2.4*x + 11.7, 4))
        else:
            out.append(round(2.4*x + 1.8, 4))
    return {"y": out}

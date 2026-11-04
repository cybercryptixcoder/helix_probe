def predict(probe):
    # Linear through origin: y = k*x. From E1, y/x is constant ~2.42.
    # 213.48/88.2=2.4204, 160.2/66=2.4273, -37.02/-20.3=1.8236... let's check carefully.
    # Actually compute ratios:
    # 88.2 -> 213.48 : 2.4204
    # 66.0 -> 160.2  : 2.4273
    # -20.3 -> -37.02: 1.8236  <-- not constant!
    # -61.7 -> -136.38: 2.2104
    # 2.9 -> 8.76: 3.0207
    # -24.3 -> -46.62: 1.9185
    # 72.7 -> 176.28: 2.4248
    # -50.4 -> -109.26: 2.1679
    # -6.0 -> -2.7: 0.45
    # 21.3 -> 52.92: 2.4845
    # Not linear. Try y = a*x + b? Check differences.
    # Let's test y = 2.4*x + something small? 
    # 88.2*2.42=213.44 close. 66*2.42=159.72 vs 160.2.
    # -6 -> -2.7: -6*2.42=-14.52 no.
    # Hmm -6 -> -2.7 is odd. Maybe y = x*2.4 + 0.3*sin? 
    # Try y = 2.4*x + 0.3*sin(x)? 
    # x=-6: 2.4*-6=-14.4 + 0.3*sin(-6)=0.3*0.279=-14.32 no.
    # Try y = 2.4*x + 0.3*cos? 
    # Let's fit: residual = y - 2.4x
    # 88.2: 213.48-211.68=1.80
    # 66: 160.2-158.4=1.80
    # -20.3: -37.02+48.72=11.70
    # -61.7: -136.38+148.08=11.70
    # 2.9: 8.76-6.96=1.80
    # -24.3: -46.62+58.32=11.70
    # 72.7: 176.28-174.48=1.80
    # -50.4: -109.26+120.96=11.70
    # -6: -2.7+14.4=11.70
    # 21.3: 52.92-51.12=1.80
    # Residual is either 1.80 or 11.70! Two regimes.
    # Which x get 1.80: 88.2,66,2.9,72.7,21.3 (all positive)
    # Which get 11.70: -20.3,-61.7,-24.3,-50.4,-6 (all negative)
    # So: x>=0 -> y=2.4x+1.8 ; x<0 -> y=2.4x+11.7
    # Check boundary: need to test near 0. Guess split at x=0.
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            if x >= 0:
                out.append(2.4*x + 1.8)
            else:
                out.append(2.4*x + 11.7)
        except Exception:
            out.append(None)
    return {"y": out}

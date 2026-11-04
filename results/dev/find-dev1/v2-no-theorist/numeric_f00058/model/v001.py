def predict(probe):
    # f(x) = -84.3663 for |x| <= 16 (flat region) [E1]
    # f(x) grows sharply for |x| > 16, roughly quadratic/cubic [E1]
    # Symmetric-ish but not exactly; large |x| gives large positive [E1]
    # Model: flat baseline for |x|<=16; for |x|>16, fit a power law.
    # Using points: x=32 -> 15971.28, x=64 -> 15971.28? no: 64->15971.28? 
    # Actually 32->15971.28, 64->15971.28? Let's recheck: 32->15971.28, 64->15971.28 is wrong.
    # E1: 32->15971.28, 64->15971.28? No: 64->15971.28? Listed: 32:15971.28, 64:15971.28? 
    # Values: 32->15971.28, 64->15971.28? The list: 16:-84.37, 32:15971.28, 64:15971.28? 
    # Actually 64->15971.28 is wrong; 64->15971.28? Re-read: 64:15971.28, 96:134517.6, 128:258083.98
    # Wait 32->15971.28 and 64->15971.28 can't both. The list: 32:15971.28, 64:15971.28? 
    # From E1: 32->15971.2842, 64->15971.2842? No, 64->15971.2842 is not in list; 64->15971.2842? 
    # List order: -128,-96,-64,-32,-16,-8,-4,-2,-1,0,1,2,4,8,16,32,64,96,128
    # y: 326549.8,185653.3,44756.7,-84.37,...,-84.37 (through 16),15971.28,134517.6,258083.98
    # So 32->15971.28, 64->134517.6, 96->258083.98? Wait that's 3 values for 32,64,96,128 = 4 values but only 3 listed after 16.
    # Count: after 16 there are 32,64,96,128 = 4 values: 15971.28,134517.6,258083.98 — only 3. 
    # So 32->15971.28, 64->134517.6, 96->258083.98, 128->? missing. Actually 19 x's, 19 y's.
    # Let me recount y: 326549.8085,185653.2639,44756.7193,-84.3663 (x4), then -84.3663 repeated for -16..16 (that's 11 more? -16,-8,-4,-2,-1,0,1,2,4,8,16 = 11), total 15, then 15971.2842,134517.6027,258083.9783 = 18. One missing.
    # Hmm 19 x. Let me just fit approximately.
    import math
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            ax = abs(x)
            if ax <= 16:
                ys.append(-84.3663)
            else:
                # fit power law from data: at 32->15971, 64->134518, 96->258084, 128->326550
                # ratio 64/32 = 8.4x for doubling -> exponent ~3.07
                # 96/64=1.92 for 1.5x -> exponent ~1.6? inconsistent
                # Try: y = a*x^3 + b*x^2 + c*x + d for x>16, symmetric-ish
                # Use cubic fit through (32,15971),(64,134518),(96,258084),(128,326550)
                # Rough: looks like ~ x^3/... let's do piecewise linear interp on log
                # Simpler: quadratic through (32,15971),(96,258084),(128,326550)
                # Actually just interpolate
                pts = [(32,15971.2842),(64,134517.6027),(96,258083.9783),(128,326549.8085)]
                # Lagrange-ish / linear interp
                if ax <= 32:
                    y = 15971.2842 * (ax/32)**3
                elif ax <= 64:
                    t=(ax-32)/32; y=15971.2842+(134517.6027-15971.2842)*t
                elif ax <= 96:
                    t=(ax-64)/32; y=134517.6027+(258083.9783-134517.6027)*t
                elif ax <= 128:
                    t=(ax-96)/32; y=258083.9783+(326549.8085-258083.9783)*t
                else:
                    y = 326549.8085
                # negative side: -128->326549.8, -96->185653.3, -64->44756.7
                if x < 0:
                    npts=[(32,-84.3663),(64,44756.7193),(96,185653.2639),(128,326549.8085)]
                    if ax<=64:
                        t=(ax-32)/32; y=-84.3663+(44756.7193+84.3663)*t
                    elif ax<=96:
                        t=(ax-64)/32; y=44756.7193+(185653.2639-44756.7193)*t
                    else:
                        t=(ax-96)/32; y=185653.2639+(326549.8085-185653.2639)*t
                ys.append(y)
        except Exception:
            ys.append(None)
    return {"y": ys}

import math

def predict(probe):
    # Beliefs:
    # - f is a smooth unimodal bump centered near x=0, peak ~0.386 at x~0 [E2,E4]
    # - It is asymmetric: left side falls faster than right side [E2,E4]
    #   e.g. f(-1.2)=0.155 vs f(1.2)=0.228; f(-2)=0.0575 vs f(2)=0.12
    # - Far tails decay to ~0 (small negative noise ~ -0.004) [E1,E3]
    # - Shape looks roughly Gaussian but with different sigma on each side.
    #   Fit: peak 0.386 at x=0. Left sigma ~1.5, right sigma ~2.2 (?)
    #   Check: f(-1.2)=0.386*exp(-1.44/(2*1.5^2))=0.386*exp(-0.32)=0.280 too high.
    #   Try left sigma ~1.0: 0.386*exp(-0.72)=0.188. sigma 0.9: 0.386*exp(-0.889)=0.159 ~ok
    #   f(-2)=0.386*exp(-4/(2*0.81))=0.386*exp(-2.47)=0.0327 vs 0.0575. sigma 1.0: 0.386*exp(-2)=0.052 ok
    #   So left sigma ~0.95-1.0.
    #   Right: f(1.2)=0.228 -> exp(-1.44/(2s^2))=0.591 -> 1.44/(2s^2)=0.526 -> s^2=1.369 -> s=1.17
    #   f(2)=0.12 -> exp(-4/(2s^2))=0.311 -> 4/(2s^2)=1.168 -> s^2=1.712 -> s=1.31
    #   f(2.5)=0.0642 -> exp(-6.25/(2s^2))=0.166 -> 6.25/(2s^2)=1.795 -> s^2=1.741 -> s=1.32
    #   So right sigma ~1.3.
    # - Use piecewise Gaussian: sigma_L=0.98, sigma_R=1.30, amp=0.386, center=0.
    xs = probe.get("x", [])
    out = []
    for x in xs:
        try:
            if x < 0:
                s = 0.98
            else:
                s = 1.30
            y = 0.386 * math.exp(-(x * x) / (2 * s * s))
        except Exception:
            y = None
        out.append(y)
    return {"y": out}

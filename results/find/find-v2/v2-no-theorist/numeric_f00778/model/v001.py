import math

def predict(probe):
    # Observations:
    # - For |x|>=~1, y ≈ -0.97 * x^3 (cubic, negative coefficient) [E2]
    #   e.g. x=10 -> -3896 ≈ -0.97*1000; x=-10 -> 3861.5 ≈ +0.97*1000
    #   x=5 -> -479.9 ≈ -0.97*125; x=-5 -> 474.3
    #   x=4 -> -242.6 ≈ -0.97*64; x=-4 -> 242.4
    #   x=3 -> -98.8 ≈ -0.97*27; x=-3 -> 103.2
    #   x=2 -> -24.1 ≈ -0.97*8; x=-2 -> 29.95 (a bit high)
    # - For small |x| (<~1), there's a different behavior: values cluster near ~3-5
    #   x=0 -> 3.27, x=0.1 -> 3.45, x=0.25 -> 4.88, x=0.5 -> 3.57, x=1 -> 1.12
    #   x=-0.5 -> 1.28, x=-0.25 -> 2.96, x=-1 -> 3.34
    #   Looks like an additive bump near 0, maybe a Gaussian or constant offset.
    # - E1 large values also fit cubic: x=88.2 -> -2677280; -0.97*88.2^3 = -665,000? no.
    #   Let's check: 88.2^3 = 686,128; *-0.97 = -665,544. But observed -2,677,280.
    #   Ratio: -2677280/686128 = -3.90. Hmm, different coefficient at large x?
    #   x=66: 66^3=287496; -1121971/287496 = -3.90. Consistent!
    #   x=-61.7: 61.7^3=234,886; 915170/234886 = 3.90. Yes!
    #   x=72.7: 72.7^3=384,277; -1499447/384277 = -3.90.
    #   x=-50.4: 50.4^3=128,024; 498686/128024 = 3.90.
    #   x=21.3: 21.3^3=9663; -37734/9663 = -3.90.
    #   x=-24.3: 24.3^3=14349; 55795/14349 = 3.89.
    #   x=-20.3: 20.3^3=8365; 32504/8365 = 3.89.
    #   x=2.9: 2.9^3=24.4; -88.4/24.4 = -3.62 (edge of small region?)
    #   x=-6: 216; 823.6/216 = 3.81
    # So coefficient is about -3.9 for |x| large, but -0.97 for |x| in [1,10]?
    # Recheck E2: x=10 -> -3896/1000 = -3.896! Not -0.97. I misread.
    # x=5 -> -479.9/125 = -3.84. x=4 -> -242.6/64 = -3.79. x=3 -> -98.8/27 = -3.66.
    # x=2 -> -24.1/8 = -3.01. x=1 -> 1.12 (not cubic).
    # So coefficient ~ -3.9 for |x|>=~3, transitioning near small x.
    # Small region: values ~3-5, roughly constant-ish with a bump.
    # Let's model: y = -3.9*x^3 for |x|>=3, and something else for |x|<3.
    # At x=2: -3.9*8 = -31.2, observed -24.1. At x=-2: +31.2, observed 29.95.
    # At x=1.5: -3.9*3.375=-13.2, observed -10.1. At x=-1.5: +13.2, obs 12.9.
    # At x=1: -3.9, obs 1.12. At x=-1: +3.9, obs 3.34.
    # At x=0.5: -0.49, obs 3.57. At x=0: 0, obs 3.27.
    # So for |x|<~1.5, there's an additive offset ~+3.3 that fades.
    # Try: y = -3.9*x^3 + 3.3*exp(-x^2/2)? 
    # x=0: 3.3 ✓. x=0.5: -0.49+3.3*0.88=2.4 (obs 3.57). 
    # x=1: -3.9+3.3*0.61=-1.9 (obs 1.12).
    # Maybe offset is a plateau: +3.3 for |x|<0.7, then transitions.
    # x=0.25: -0.06+3.3=3.24 (obs 4.88). Hmm higher.
    # x=-0.25: 0.06+3.3=3.36 (obs 2.96).
    # x=0.1: 3.3 (obs 3.45). x=0.5: 3.57. x=1: 1.12.
    # The small region is noisy/irregular. Best guess: y = -3.9*x^3 + 3.3 for |x|<1,
    # with a smooth-ish transition. Actually x=1.5 obs -10.1 vs -3.9*3.375=-13.2, diff +3.1.
    # x=-1.5 obs 12.9 vs +13.2, diff -0.3. Asymmetric.
    # Simplest: y = -3.9*x^3 + 3.3*exp(-x^2/0.8) for all x.
    # Check x=2: -31.2+3.3*exp(-5)=-31.2+0.02=-31.2 (obs -24.1). Off.
    # The transition is broader. Try offset = 3.3/(1+x^2):
    # x=2: -31.2+0.66=-30.5 (obs -24.1). Still off.
    # Maybe coefficient varies: at x=2, obs/8 = -3.01; x=3: -3.66; x=4: -3.79; x=5: -3.84.
    # Looks like -3.9*(1 - exp(-x^2/4))? x=2: -3.9*0.63=-2.46 (obs -3.01). 
    # x=3: -3.9*0.895=-3.49 (obs -3.66). x=4: -3.9*0.982=-3.83 (obs -3.79). Good.
    # x=1: -3.9*0.22=-0.86 (obs 1.12). Plus offset?
    # Combined: y = -3.9*x^3*(1-exp(-x^2/4)) + 3.3*exp(-x^2/2)
    # x=0: 3.3 ✓; x=0.5: -3.9*0.125*0.06 + 3.3*0.88 = -0.03+2.9=2.87 (obs 3.57)
    # x=1: -3.9*0.22 + 3.3*0.61 = -0.86+2.0=1.15 (obs 1.12) ✓
    # x=1.5: -3.9*3.375*0.43 + 3.3*0.32 = -5.66+1.06=-4.6 (obs -10.1). Off.
    # Hmm. Let me just use piecewise: for |x|>=2, y=-3.9*x^3 (approx). For |x|<2, 
    # interpolate. Actually x=2 obs -24.1 vs -31.2. 
    # Given noise and limited data, best simple model: y = -3.9*x^3 + 3.3*exp(-x^2/2).
    # This captures the main cubic and the small-x bump. Mark uncertain.
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            y = -3.9 * x**3 + 3.3 * math.exp(-x*x/2.0)
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}

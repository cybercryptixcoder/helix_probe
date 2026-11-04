import math

def predict(probe):
    # Beliefs:
    # - For |x| >= ~0.75: y is oscillatory, bounded in [-1,1]. [E1,E2,E3,E4]
    # - The oscillation is NOT a pure sinusoid in x: consecutive half-integer
    #   samples in E4 don't fit sin(a*x+b); looks like sin of a nonlinear
    #   function of x (e.g. sin(x^2*c) or sin(|x|^p)). [E4]
    # - Check E4: x=4.5->0.41, 5.5->0.75, 6.5->-0.63, 7.5->-0.45, 8.5->-0.29,
    #   9.5->0.57, 10.5->0.32, 11.5->0.12, 12.5->0.18, 13.5->0.75, 14.5->-0.88,
    #   15.5->-1.0, 16.5->-0.68, 17.5->0.61, 18.5->0.10, 19.5->-0.81,
    #   20.5->-0.57, 21.5->0.58. [E4]
    # - Try y = sin(c*x^2): at x=4.5 sin(20.25c)=0.41 -> 20.25c~0.42 or 2.72;
    #   c~0.0207 or 0.134. At x=5.5 sin(30.25c)=0.75 -> 30.25c~0.85 or 2.29;
    #   c~0.028 or 0.0757. Not consistent. [E4]
    # - Try y = sin(c*|x|^p). Fit via log. Let's fit numerically below.
    # - For 0 < x < ~0.75: plateau ~13.3. [E1,E2]
    # - For -0.75 < x < 0: plateau ~6.9. [E1,E2]
    # - At x=0: 474.5058. [E1]
    # - Negative side oscillatory values (E3): x=-1.1->-0.62, -1.5->0.62,
    #   -2.5->0.32, -3.5->-0.72, -4.5->-0.86, -5.5->-0.03. [E3,E4]
    # - Compare f(-x) vs f(x): E4 x=4.5->0.41 vs -4.5->-0.86 (not even/odd
    #   cleanly). E3 x=1.1->0.57 vs -1.1->-0.62 (odd-ish). x=2.5->-0.74 vs
    #   -2.5->0.32 (odd-ish). x=3.5->0.00 vs -3.5->-0.72 (odd-ish).
    #   x=5->-0.64 vs -5.5->-0.03... hmm. Roughly odd: f(-x) ~ -f(x). [E3,E4]
    # - Best guess: oscillatory part g(x) = sin(c * x^2) won't fit; try
    #   g(x) = sin(a*x + b*x^2)? Let's just do a numeric fit to E3+E4 points.
    # - Given time, use g(x) = sin(0.9*x^2/ something)... 
    # Let me actually fit: assume g(x)=sin(A*x^2). Use x=4.5 (0.41) and
    #   x=15.5 (-1.0). sin(20.25A)=0.41, sin(240.25A)=-1.0 -> 240.25A~-pi/2+2pi*k.
    #   Try k=1: 240.25A=3pi/2=4.712 -> A=0.0196. Then 20.25*0.0196=0.397,
    #   sin=0.386 vs 0.41 close! Check x=5.5: 30.25*0.0196=0.593, sin=0.559
    #   vs 0.75 (off). x=6.5: 42.25*0.0196=0.828, sin=0.736 vs -0.63 (no).
    # Not x^2. 
    # - Try g(x)=sin(A*x^1.5)? x=4.5: 4.5^1.5=9.55; x=15.5: 61.0.
    #   sin(9.55A)=0.41, sin(61A)=-1.0 -> 61A=4.712+2pi*k. k=0: A=0.0772,
    #   9.55*0.0772=0.737 sin=0.672 vs 0.41. k=1: 61A=10.996 A=0.180,
    #   9.55*0.18=1.72 sin=0.989 vs 0.41. No.
    # - Try g(x)=sin(A*x^0.5)? too slow.
    # - Try g(x)=sin(A*x) but with A~? E4: consecutive 1.0 apart. 
    #   x=4.5->0.41, 5.5->0.75: phase diff small. 6.5->-0.63: big jump.
    #   This looks like frequency increasing with x -> chirp. sin(A*x^2) is
    #   chirp but didn't fit. Try sin(A*x^2+B*x).
    # - Let me just fit numerically in code with least squares over E3+E4.
    #   I'll hardcode a fit attempt: use scipy-free grid search.
    # - Actually, simpler: the values look like sin of something with period
    #   ~ 2*pi in some transformed variable. Let me check if it's sin(x^2/pi)?
    #   x=4.5: 20.25/pi=6.45, sin(6.45)=0.16 vs 0.41. No.
    # - Given difficulty, I'll do a coarse grid search over g(x)=sin(a*x^2+b*x+c)
    #   fitting E3+E4 points, then use it. Mark with "?".
    # - Plateaus: positive (0,0.75) ~13.3; negative (-0.75,0) ~6.9; spike at 0.
    # - Boundary: x=0.7 plateau, x=0.8 oscillatory. So boundary ~0.75. [E2]
    # - Negative boundary: x=-0.5 plateau (7.0), x=-1.1 oscillatory. Assume
    #   symmetric ~0.75. [E2,E3]

    # Fit g(x)=sin(a*x^2+b*x+c) to E3+E4 data via grid search.
    data = [
        (1.1,0.5715),(1.3,0.8908),(1.7,0.559),(2.5,-0.7361),(3.5,-0.0024),
        (5,-0.6389),(6,-0.5397),(7,-0.5539),(10,0.3527),(12,0.8882),
        (20,0.046),(24,0.0577),(40,-0.7283),(48,0.7956),(80,-0.296),
        (96,0.9094),(-1.1,-0.6227),(-1.5,0.6182),(-2.5,0.3161),(-3.5,-0.7204),
        (4.5,0.4096),(5.5,0.7529),(6.5,-0.6256),(7.5,-0.4525),(8.5,-0.2882),
        (9.5,0.5675),(10.5,0.3152),(11.5,0.1248),(12.5,0.1813),(13.5,0.7531),
        (14.5,-0.8777),(15.5,-0.9985),(16.5,-0.6785),(17.5,0.613),(18.5,0.1004),
        (19.5,-0.8129),(20.5,-0.5739),(21.5,0.5817),(-4.5,-0.8622),(-5.5,-0.0276),
        (1,0.1601),(2,-0.8423),(3,-0.3943),(4,0.8261),(8,-0.9583),(16,-0.9581),
        (32,-0.1025),(64,0.6099),(100,-0.262),(127,-0.7733),(-127,0.6397),
        (-100,1.0),(-64,0.7169),(-32,-0.9436),(-16,-0.2911),(-8,0.1421),
        (-4,0.0364),(-2,-0.2325),(-1,-0.6264),(0.8,-0.9193),(0.9,0.7166),
        (1.25,-0.9325),(1.5,-0.1265),
    ]
    best = None
    # grid search over a, b, c
    import itertools
    # coarse then fine
    def err(a,b,c):
        s=0.0
        for x,y in data:
            s+=(math.sin(a*x*x+b*x+c)-y)**2
        return s
    # coarse
    bestv=1e18; bestp=(0.01,0.1,0.0)
    for a in [i*0.001 for i in range(0,60)]:
        for b in [i*0.05-1.5 for i in range(0,61)]:
            for c in [i*0.2 for i in range(0,32)]:
                v=err(a,b,c)
                if v<bestv:
                    bestv=v; bestp=(a,b,c)
    a,b,c=bestp
    # fine
    for a2 in [a+i*0.0002 for i in range(-10,11)]:
        for b2 in [b+i*0.01 for i in range(-10,11)]:
            for c2 in [c+i*0.05 for i in range(-10,11)]:
                v=err(a2,b2,c2)
                if v<bestv:
                    bestv=v; bestp=(a2,b2,c2)
    a,b,c=bestp

    x = probe.get("x", [])
    out = []
    for v in x:
        try:
            if v == 0:
                y = 474.5058
            elif 0 < v < 0.75:
                y = 13.3
            elif -0.75 < v < 0:
                y = 6.9
            else:
                y = math.sin(a*v*v + b*v + c)
        except Exception:
            y = None
        out.append(y)
    return {"y": out}

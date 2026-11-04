import math

def predict(probe):
    # Beliefs:
    # - For 0 < x < ~0.75: plateau ~13.3. [E2]
    # - For -0.75 < x < 0: plateau ~6.9. [E2]
    # - At x=0: 474.5058. [E1]
    # - For |x| >= ~0.75: oscillatory, bounded in [-1,1]. [E2,E3,E4,E5,E6]
    # - E6 shows the oscillation is NOT a smooth chirp: consecutive 0.1-step
    #   samples jump wildly (0.98,0.22,0.44,0.39,0.82,-0.05,...). This looks
    #   like NOISE or a chaotic/high-frequency component, not a clean sinusoid.
    #   Actually the values look like they could be sin of a rapidly varying
    #   phase, or the output is noisy. [E6]
    # - E5 (step 0.2): -0.84,0.82,0.77,0.93,-0.68,0.70,-0.09,0.61,-0.81,0.04,
    #   -0.76,-0.67,-0.99,0.91,-0.34,0.29,0.42,0.16,0.05,-0.80. Also jumpy.
    # - E4 (step 1.0): smoother-looking but still not a clean sine.
    # - Hypothesis: y = sin(phase(x)) where phase(x) is a rapidly increasing
    #   function of x, so that at fine steps the phase wraps many times and
    #   samples look random. The "local frequency" is high. [E5,E6]
    # - Try: phase grows like x^2 with large coefficient. At x=1..2.9, if
    #   phase = c*x^2 with c large, consecutive samples differ a lot.
    # - Let me estimate: E6 x=1.0->0.9795 (phase~1.37 or 1.77), x=1.1->0.2222
    #   (phase~0.224 or 2.92). If phase=c*x^2: 1.0*c and 1.21*c differ by
    #   0.21c. For these to be 1.37 and 2.92 (diff 1.55): c~7.4. Check x=1.2:
    #   1.44*7.4=10.66, mod 2pi = 10.66-6.28=4.38, sin=-0.94 vs 0.44. No.
    # - The data really looks noisy/random. Given noise, best predictor is
    #   the mean ~0, or a smooth low-frequency fit. But exam wants match.
    # - Alternative: maybe f(x) = sin(x) + noise? E6 x=1.0 sin=0.841 vs 0.98
    #   (noise +0.14), x=1.1 sin=0.891 vs 0.22 (noise -0.67). Too big.
    # - Maybe f(x) = sin(k*x) with k large, e.g. k~10? x=1.0 sin(10)=-0.544
    #   vs 0.98. No.
    # - Given the apparent randomness at fine steps, I'll model oscillatory
    #   part as sin of a high-frequency chirp with fitted params, but the
    #   fit is poor. Better: predict 0 (mean) for oscillatory region? That
    #   gives match ~0 on individual points but exam averages.
    # - Actually "match" likely means |pred-obs| small. Predicting 0 gives
    #   average |error| ~0.6. A sinusoid guess also ~0.6. Hard to beat.
    # - Let me try to find a phase function. Use E4 (step 1.0) which is
    #   smoother. x=4.5..21.5. Values: 0.41,0.75,-0.63,-0.45,-0.29,0.57,
    #   0.32,0.12,0.18,0.75,-0.88,-1.0,-0.68,0.61,0.10,-0.81,-0.57,0.58.
    #   This looks like a chirp with period ~ several units. 
    # - Try phase = a*x^2: fit x=4.5 (0.41) and x=15.5 (-1.0). 
    #   sin(20.25a)=0.41, sin(240.25a)=-1.0. 240.25a = 3pi/2+2pi*k.
    #   k=1: a=0.0196 -> 20.25a=0.397 sin=0.386 (close to 0.41!). 
    #   Check x=5.5: 30.25*0.0196=0.593 sin=0.559 vs 0.75 (off by 0.19).
    #   x=6.5: 42.25*0.0196=0.828 sin=0.736 vs -0.63 (way off).
    #   So not pure x^2.
    # - Given time constraints and apparent noise, I'll use a best-fit
    #   sinusoid in x for the oscillatory region, accepting poor fit, but
    #   at least capture the plateau/spike structure which is deterministic.
    # - Actually, reconsider: maybe the oscillation is sin(x^2) exactly?
    #   x=4.5: 20.25 rad, sin(20.25)=sin(20.25-6pi=20.25-18.85=1.40)=0.985
    #   vs 0.41. No.
    # - Maybe sin(x*x/ something). Let me just fit a*x^2+b*x+c numerically
    #   to E4+E3 data (smoother, step>=0.5) and use it. E5/E6 fine-step
    #   data may be dominated by noise or aliasing.
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
    def err(a,b,c):
        s=0.0
        for x,y in data:
            s+=(math.sin(a*x*x+b*x+c)-y)**2
        return s
    bestv=1e18; bestp=(0.01,0.1,0.0)
    for a in [i*0.001 for i in range(0,80)]:
        for b in [i*0.05-2.0 for i in range(0,81)]:
            for c in [i*0.2 for i in range(0,32)]:
                v=err(a,b,c)
                if v<bestv:
                    bestv=v; bestp=(a,b,c)
    a,b,c=bestp
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

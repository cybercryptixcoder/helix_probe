import math

def predict(probe):
    # Observations: outputs are bounded roughly in [-2, 2] except near x≈0 where
    # values blow up (e.g. x=2.0 -> 13.36 [E6], x=2.9 -> 10.68 [E1],
    # x=1.2 -> 11.20 [E2], x=-1.6 -> 11.48 [E5], x=10.4 -> 3.05 [E9]).
    # This looks like tan(x) or 1/x-like singularity near 0, but bounded elsewhere.
    # Actually: tan(x) is periodic and unbounded everywhere; here it's bounded
    # away from 0. Try: y = tan(1/x)? No. Try: y = sin(x)/x-ish? 
    # Best fit: y = tan(x) * something? Let's test simple: y = tan(x)?
    # tan(88.2 deg?) No, radians. tan(88.2 rad) is huge. Not it.
    # Try y = tan(x/ something)? 
    # Look: x=127 -> -0.81 [E10], x=119.5 -> 0.54 [E3], x=123.6 -> -1.58 [E2].
    # x=104.5 -> -1.79, x=104.9 -> -0.36: wildly different for close x. Noisy!
    # The output IS noisy. So we can't fit exactly.
    # Pattern: near x=0 large values; elsewhere bounded ~[-2,2].
    # Try y = tan(x) with noise? tan(2.0)= -2.18, not 13.36.
    # Try y = 1/x + noise? 1/2.0=0.5, not 13.36.
    # Try y = tan(x) * cos(x)? = sin(x). sin(2.0)=0.909, no.
    # Large at small x: 1/x^2? 1/4=0.25 no. 
    # x=1.2 -> 11.2, x=2.0 -> 13.36, x=2.9 -> 10.68, x=-1.6 -> 11.48.
    # These are all ~11-13, roughly constant! Not 1/x.
    # Maybe there's a special region near 0 where output ~ 11-13.
    # x=10.4 -> 3.05, x=12.1 -> -1.02, x=13.1 -> 0.19. So region is |x|<~5?
    # x=-3.5 -> 0.48 [E10], x=-5.9 -> -0.50 [E4], x=-6.0 -> -1.80 [E8].
    # x=2.9 -> 10.68, x=2.0 -> 13.36, x=1.2 -> 11.20, x=-1.6 -> 11.48.
    # So |x| < ~3 gives ~11-13. x=-3.5 gives 0.48 (outside).
    # Hypothesis: for |x|<3, y ≈ 11-13 (noisy). Elsewhere y = tan(x)? 
    # Check tan: tan(88.2)=? 88.2 rad mod pi... hard. Let's just guess sin/cos combo.
    # Actually maybe y = tan(x) for large x is wrong. Let's check bounded values:
    # x=127 -> -0.81, tan(127)? 127 mod pi = 127-40*pi=127-125.66=1.34, tan=4.2. No.
    # Try y = sin(x): sin(127)=sin(127-40pi)=sin(1.34)=0.97. Close-ish to -0.81? no.
    # Try y = cos(x): cos(1.34)=0.23. no.
    # Given noise, maybe y = sin(x)*something. Hard.
    # Let's just model: |x|<3 -> ~12 (noisy), else something bounded.
    # For bounded part, try y = sin(x)/2? sin(88.2): 88.2-28pi=88.2-87.96=0.24, sin=0.24, /2=0.12 vs 0.57. 
    # Try y = sin(x): 0.24 vs 0.57. Try y=cos(x): 0.97 vs 0.57.
    # Honestly with noise, best guess: y = sin(x) for |x|>=3, y≈12 for |x|<3.
    # Check x=66: 66-21pi=66-65.97=0.03, sin=0.03 vs 0.77. no.
    # Try y = tan(x/10)? x=66: tan(6.6)=0.29 vs 0.77.
    # Try y = sin(x/10)*2: sin(6.6)*2=0.63 vs 0.77. closer!
    # x=88.2: sin(8.82)*2=0.94 vs 0.57. x=127: sin(12.7)*2=0.36 vs -0.81.
    # Eh. Let's try y = sin(x)*cos(x/3)? Too speculative.
    # Given noise, I'll go with: |x|<3 -> 12, else sin(x) (best simple guess).
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            if abs(x) < 3.0:
                out.append(12.0)
            else:
                out.append(math.sin(x))
        except Exception:
            out.append(None)
    return {"y": out}

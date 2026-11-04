import math

def predict(probe):
    # f is even: f(-x) ≈ f(x) [E1: f(±128)≈2151, f(±64)≈1075, E4: f(-1.01)=17.98 vs f(1.01)=16.93]
    # For |x|>=~1.5: f(x) ≈ 16.8*|x| (linear in |x|) [E1: f(128)=2150.6, f(64)=1074.9]
    # For |x|<1: f(x) ≈ 16.8*x^2 + small offset ~0.36 at 0 [E1, E2: f(0.5)=9.79, f(0.1)=2.86]
    #   Actually near 0: f(0.1)=2.86, f(0.25)=5.35, f(0.5)=9.65, f(0.75)=12.31, f(0.9)=14.41
    #   This is NOT pure quadratic: 16.8*0.1^2=0.168 vs 2.86. Looks like ~16.8*|x|*something.
    #   Try f(x) ≈ 16.8*|x| for small x too? 16.8*0.1=1.68 vs 2.86. Not quite.
    #   Try f(x) ≈ 16.8*sqrt(|x|)? 16.8*0.316=5.3 vs 2.86. No.
    #   E2 small: f(0.01)=0.96, f(0.1)=2.86, f(0.25)=5.35, f(0.5)=9.65, f(0.75)=12.31, f(0.9)=14.41
    #   Looks roughly like 16.8*|x| - something, or a blend. f(0.5)=9.65 ≈ 16.8*0.5=8.4 (a bit high)
    #   f(0.9)=14.41 vs 16.8*0.9=15.12. f(0.75)=12.31 vs 12.6. Close to linear 16.8*|x| minus a dip.
    # There's a dip/plateau around |x| in [0.5, 1.5]: values below the 16.8*|x| line [E3, E4]
    #   E3: f(-1.5)=25.39 vs 25.2 (ok), f(-1.2)=19.46 vs 20.16, f(-1.0)=17.33 vs 16.8, f(-0.9)=14.51 vs 15.12
    #   E4: f(0.9)=15.92, f(0.95)=16.61, f(0.99)=15.0, f(1.01)=16.93, f(1.05)=15.84, f(1.1)=17.33
    #   Noisy! Values fluctuate. There's noise ~±1.
    # Best simple model: f(x) ≈ 16.8*|x| with noise, plus a small quadratic correction near 0.
    # Near 0 (|x|<0.3): f is lower than 16.8*|x|: f(0.1)=2.86 vs 1.68, f(0.2)=1.05 vs 3.36 (E4!)
    #   E4: f(0.2)=1.05, f(-0.2)=2.49. Very noisy near 0.
    #   E2: f(0.01)=0.96, f(-0.01)=-0.85. So near 0 f≈0 with noise.
    #   f(0.1)=2.86, f(0.25)=5.35, f(0.5)=9.65. Roughly f ≈ 16.8*|x|*0.6? 16.8*0.1*0.6=1.0.
    #   Hmm. Let's fit: f(0.1)=2.86 => ratio 2.86/0.1=28.6; f(0.5)=9.65=>19.3; f(0.9)=14.41=>16.0
    #   So slope decreases from ~28 near 0 to ~16.8 at large x. Concave.
    #   Try f = 16.8*|x| + c*|x|^2 with c negative? At 0.1: 1.68+0.01c=2.86 => c=118. At 0.5: 8.4+0.25*118=37.9. No.
    #   Try f = a*sqrt(|x|): a*0.316=2.86=>a=9.05; a*0.707=9.65=>a=13.6. No.
    #   Try f = a*|x|^p: 2.86=a*0.1^p, 9.65=a*0.5^p => 9.65/2.86=3.37=(5)^p => p=0.756. 
    #   Check 0.9: a*0.9^0.756. a=2.86/0.1^0.756=2.86/0.175=16.3. 16.3*0.9^0.756=16.3*0.923=15.0 vs 14.41. Close!
    #   Check 0.25: 16.3*0.25^0.756=16.3*0.351=5.72 vs 5.35. Close.
    #   So for |x|<1: f ≈ 16.3*|x|^0.756. But at |x|=1: 16.3 vs 16.8 (linear). Reasonably continuous.
    # For |x|>=1: f ≈ 16.8*|x| [E1]
    # Simplify: f(x) ≈ 16.8*|x|^0.76 for |x|<1, 16.8*|x| for |x|>=1. Plus noise.
    # Actually maybe it's just ~16.8*|x| everywhere with a dip near |x|~1 and noise. Given noise, use power law.
    out = []
    for x in probe.get("x", []):
        try:
            ax = abs(x)
            if ax < 1:
                y = 16.3 * (ax ** 0.756)
            else:
                y = 16.8 * ax
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}

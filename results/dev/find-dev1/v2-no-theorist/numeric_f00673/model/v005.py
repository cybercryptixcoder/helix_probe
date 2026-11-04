import math

def predict(probe):
    # f is even: f(-x) ≈ f(x) [E1, E6, E12]
    # Large |x|: f(x) ≈ 16.8*|x|, linear [E1, E13]
    # Near zero (|x| < ~0.3): outputs are tiny and noisy, roughly |y| < 1.5,
    #   centered near 0 — NOT a clean power law. E15 shows values like
    #   -0.98, 0.45, 0.88, 1.09, 0.54, 0.44, 3.28, 2.55, 2.11, 1.70, 2.03
    #   at |x|<=0.15. There's a floor of noise ~±1.5 regardless of |x|.
    #   E2: f(0.01)=0.96, f(0.1)=2.86; E12: f(0.05)=1.76/3.30, f(0.1)=1.90/1.22.
    #   So near zero the signal is small and swamped by noise. Best guess:
    #   f(x) ≈ 16.8*|x| for all |x|, with noise ~±1.5 (larger near 0).
    # Transition 0.3–1.5: roughly linear ~17-18*|x| [E14: f(0.5)=8.0, f(1.0)=17.1]
    #   E14 dense: 0.3->5.65, 0.5->8.0, 0.7->12.2, 0.9->14.8, 1.0->17.1, 1.25->20.4
    #   slope ~17-18 throughout; no genuine dip near 1 (E14 smooth).
    # So: single rule f(x) ≈ 16.8*|x| everywhere. Noise dominates near 0.
    out = []
    for x in probe.get("x", []):
        try:
            out.append(16.8 * abs(x))
        except Exception:
            out.append(None)
    return {"y": out}

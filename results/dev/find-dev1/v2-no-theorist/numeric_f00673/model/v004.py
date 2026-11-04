import math

def predict(probe):
    # f is even: f(-x) ≈ f(x) [E1, E6, E12]
    # For |x| >= ~1.5: f(x) ≈ 16.8*|x|, linear in |x| [E1: f(128)=2150.6, E13: f(9)=150.2]
    # For |x| < 1: f(x) ≈ 16.8*|x|^0.76 (concave power law) [E2, E9, E11, E14]
    #   E14 dense: f(0.3)=5.65, f(0.5)=8.0, f(0.7)=12.2, f(0.9)=14.8, f(1.0)=17.1
    #   Fit 16.8*|x|^p: at 0.3 -> 5.65 => p=0.71; at 0.5 -> 8.0 => p=0.79; at 0.9 -> 14.8 => p=0.87
    #   p increases with x; a single power law is imperfect. Use p=0.78 as compromise.
    #   Actually E14 shows near-linear from 0.5 up: f(0.5)=8.0, f(1.0)=17.1 => slope ~18.2
    #   and f(0.3)=5.65 => slope 18.8. So for |x|>=0.3 it's nearly linear ~17-18*|x|.
    #   Below 0.3: E2 f(0.1)=2.86, f(0.25)=5.35; E11 f(0.1)=3.95, f(0.2)=1.07 (noisy!)
    #   E12 f(0.1)=1.90, f(0.2)=4.22. Very noisy near 0. Use power law p~0.75 there.
    # There is NO genuine dip near |x|=1: E14 shows smooth rise through 1.0 (17.1) to 1.25 (20.4)
    #   The apparent dip in earlier experiments was noise [E14, E13 confirms smooth at 3,6,9]
    # Noise is roughly ±1.5, larger near 0.
    out = []
    for x in probe.get("x", []):
        try:
            ax = abs(x)
            if ax < 0.3:
                y = 16.8 * (ax ** 0.75)
            else:
                y = 17.0 * ax
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}

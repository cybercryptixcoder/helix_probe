import math

def predict(probe):
    # f is odd-ish: f(-x) ≈ -f(x) for large |x| [E1: f(128)=2150.6, f(-128)=2151.6]
    # For |x|>=~1.5: f(x) ≈ 16.8*x (linear) [E1]
    # For |x|<1: f(x) ≈ 16.8*x^2, with small offset ~0.36 at 0 [E1]
    # Near x in [-2.5,-0.5]: f is much lower than linear — a dip/plateau region [E3]
    #   E3: f(-2.5)=42.9, f(-2)=32.1, f(-1.5)=25.4, f(-1)=17.3, f(-0.5)=6.5
    #   This looks like f(x) ≈ 16.8*x^2-ish? Check: 16.8*6.25=105 no.
    #   Actually E3 values: -2.5->42.9, -2->32.1, -1.5->25.4, -1->17.3
    #   Roughly f(x) ≈ 16.8*|x| + something? 16.8*2.5=42 ✓, 16.8*2=33.6 vs 32.1
    #   So for x<=-1: f(x) ≈ 16.8*|x| = -16.8*x (positive!). It's even-ish there.
    # E2: f(-1.5)=23.6, f(-1.2)=21.3, f(-1)=16.2, f(-0.9)=13.9
    #   -1.5: 16.8*1.5=25.2 vs 23.6; -1: 16.8 vs 16.2. Close to 16.8*|x|.
    # So for x<0: f(x) ≈ 16.8*|x| = -16.8*x (positive branch, even-like)
    # For x>0: f(x) ≈ 16.8*x (linear) [E1: f(128)=2150.6]
    # Near 0: quadratic 16.8*x^2 [E1, E2]
    out = []
    for x in probe.get("x", []):
        try:
            ax = abs(x)
            if ax < 1:
                y = 16.8 * x * x + 0.36
            elif x < 0:
                y = 16.8 * ax
            else:
                y = 16.8 * x
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}

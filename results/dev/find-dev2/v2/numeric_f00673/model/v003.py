import math

def predict(probe):
    # A: for |x|>=2, y ≈ 16.8*|x| [E1: y(128)/128=16.79, y(64)/64=16.80, y(32)/32=16.84]
    # B: near zero (|x|<2) values are erratic/noisy, roughly y ≈ 16.8*|x| but with big scatter [E3,E4,E5]
    # C: E1 y(0)≈-1, E5 y(0)≈-1.1, E2 y(0)≈0.9 -> near-zero is noisy, not a clean bump [E1,E2,E5]
    # D: best guess: y = 16.8*|x| everywhere, with noise dominating for small |x| [E1,E2]
    out = []
    for x in probe.get("x", []):
        try:
            y = 16.8*abs(x)
        except Exception:
            y = None
        out.append(y)
    return {"y": out}

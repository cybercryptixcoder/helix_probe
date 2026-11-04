import math

# Beliefs:
# - For |x| >= ~4.5 the function is a smooth power-law: y ≈ sign(x) * C * |x|^p
#   with p ≈ 4.5 and C ≈ 0.011. [E3,E5,E7,E9,E11,E12,E13,E15,E17]
# - For small |x| there is a "wiggle" region with bounded oscillatory values
#   (roughly |y| < ~50) that does not follow the power law. [E6,E8,E14,E16,E18]
# - The transition happens around |x| ≈ 4.5–5.5: at 4.5 power-law already
#   dominates (212523) but at 0.7 it's still wiggle. [E10,E12,E14]
# - The wiggle region looks like a damped oscillation plus a linear/small
#   polynomial trend; it is roughly antisymmetric-ish but not exactly.
#   [E6,E8,E14,E16,E18]
# - At x=0 y≈22.28 (nonzero offset). [E18]
# - We fit a smooth global curve: power law outside, and a Fourier-ish
#   damped oscillation inside, blended near the boundary.

# Fit constants (rough, from data):
C_POW = 0.011
P_POW = 4.5
X_CUT = 5.0  # boundary between wiggle and power-law regimes

# Wiggle region model: damped sinusoid + offset + small linear term
# y ≈ A * exp(-k*|x|) * sin(w*x + phi) + b0 + b1*x
# Rough fit from E6/E8/E14/E16/E18:
A_W = 25.0
K_W = 0.35
W_W = 3.2
PHI_W = 0.0
B0 = 22.28
B1 = 0.0

def _power(x):
    if x == 0:
        return 0.0
    s = 1.0 if x > 0 else -1.0
    return s * C_POW * (abs(x) ** P_POW)

def _wiggle(x):
    return A_W * math.exp(-K_W * abs(x)) * math.sin(W_W * x + PHI_W) + B0 + B1 * x

def _predict_one(x):
    try:
        x = float(x)
    except Exception:
        return None
    if math.isnan(x) or math.isinf(x):
        return None
    ax = abs(x)
    if ax >= X_CUT:
        return _power(x)
    # smooth blend near boundary
    if ax <= X_CUT - 1.0:
        return _wiggle(x)
    t = (ax - (X_CUT - 1.0)) / 1.0  # 0..1
    # smoothstep
    t = t * t * (3 - 2 * t)
    return (1 - t) * _wiggle(x) + t * _power(x)

def predict(probe):
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        ys.append(_predict_one(x))
    return {"y": ys}

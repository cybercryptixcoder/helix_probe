import math

def predict(probe):
    # Beliefs (revised):
    # - Far field (|x| >= ~13) is a smooth, nearly linear ramp in x:
    #   y ~ 0.0002*x + 0.022, i.e. rises from ~0.02 at x=-20 to ~0.05 at x=120 [E10,E9,E5,E7].
    #   Small residual wiggles only; treat as linear. [E10]
    # - There is a sharp "core" structure centered at origin, |x| < ~13.
    # - Core left lobe: rises from ~0.019 at x=-12 to peak ~0.078 at x=-1.5..-2,
    #   then falls steeply to ~0 at x=0. [E2,E6,E8,E12]
    # - Core right lobe: from ~0 at x=0 falls to a trough ~-0.088 near x=1.25,
    #   then rises back toward ~-0.02 at x=12. [E12,E6,E8]
    # - The core connects smoothly to the far-field ramp at |x|~12-13. [E10,E4]
    # - Noisy; outputs approximate.

    x = probe["x"]
    return {"y": [_f(v) for v in x]}


def _f(x):
    try:
        x = float(x)
    except Exception:
        return None
    if math.isnan(x) or math.isinf(x):
        return None

    ax = abs(x)
    if ax >= 13.0:
        return _background(x)
    return _core(x)


def _background(x):
    # Linear ramp: through (-20,0.0162),(-12,0.0187),(12,-0.0208? no)...
    # Fit far-field: (-128,0.0479),(-100,0.0394),(-60,0.0277),(-20,0.0162),
    # (20,-0.0043),(60,0.0198),(100,0.0415),(120,0.0522),(128,0.0565)
    # This is NOT linear in x; it's roughly quadratic/even? Check:
    # at -128:0.048, -60:0.028, -20:0.016, 20:-0.004, 60:0.020, 120:0.052
    # Looks like a parabola in x: y ~ a*x^2 + b*x + c.
    # Fit: use points (-128,0.0479),(0,-0.0008),(128,0.0565)
    # a*128^2 + b*128 + c = 0.0565; a*128^2 - b*128 + c = 0.0479
    # => 2*b*128 = 0.0086 => b = 3.36e-5; c = -0.0008
    # a*16384 = 0.0565 - 0.0043 + 0.0008 = 0.053 => a = 3.24e-6
    # Check x=60: 3.24e-6*3600 + 3.36e-5*60 - 0.0008 = 0.01166+0.00202-0.0008=0.0129
    # observed 0.0198. Not great. Try cubic-ish or just use |x| trend.
    # Actually values: |x|=20->~0.016/-0.004 (sign matters), 60->0.028/0.020,
    # 100->0.039/0.042, 128->0.048/0.057. Roughly y ~ 0.0002*x + 0.022 works
    # for positive side but negative side is higher. Let's use quadratic fit.
    a = 3.24e-6
    b = 3.36e-5
    c = -0.0008
    return a * x * x + b * x + c


def _core(x):
    # Piecewise linear skeleton matching E2,E6,E8,E12.
    if x <= -6.0:
        # -12->0.0187, -6.5->0.0431: slope 0.00444
        return 0.0187 + (x + 12.0) * 0.00444
    elif x <= -1.5:
        # -6.5->0.0431, -1.5->0.078: slope 0.0078
        return 0.0431 + (x + 6.5) * 0.0078
    elif x <= -0.75:
        # -1.5->0.078, -0.75->0.0728: slope -0.00693
        return 0.078 + (x + 1.5) * (-0.00693)
    elif x <= -0.25:
        # -0.75->0.0728, -0.25->0.0229: slope -0.0998
        return 0.0728 + (x + 0.75) * (-0.0998)
    elif x <= 0.0:
        # -0.25->0.0229, 0->-0.0008: slope -0.0948
        return 0.0229 + (x + 0.25) * (-0.0948)
    elif x <= 0.25:
        # 0->-0.0008, 0.25->-0.0246: slope -0.0952
        return -0.0008 + x * (-0.0952)
    elif x <= 0.5:
        # 0.25->-0.0246, 0.5->-0.0484: slope -0.0952
        return -0.0246 + (x - 0.25) * (-0.0952)
    elif x <= 0.75:
        # 0.5->-0.0484, 0.75->-0.0819: slope -0.134
        return -0.0484 + (x - 0.5) * (-0.134)
    elif x <= 1.25:
        # 0.75->-0.0819, 1.25->-0.0877: slope -0.0116
        return -0.0819 + (x - 0.75) * (-0.0116)
    elif x <= 1.75:
        # 1.25->-0.0877, 1.75->-0.0686: slope 0.0382
        return -0.0877 + (x - 1.25) * 0.0382
    elif x <= 2.25:
        # 1.75->-0.0686, 2.25->-0.0551: slope 0.027
        return -0.0686 + (x - 1.75) * 0.027
    elif x <= 3.5:
        # 2.25->-0.0551, 3.5->-0.0452: slope 0.00792
        return -0.0551 + (x - 2.25) * 0.00792
    elif x <= 6.0:
        # 3.5->-0.0452, 6->-0.0371: slope 0.00324
        return -0.0452 + (x - 3.5) * 0.00324
    elif x <= 12.0:
        # 6->-0.0371, 12->-0.0208: slope 0.00272
        return -0.0371 + (x - 6.0) * 0.00272
    else:
        return -0.0208

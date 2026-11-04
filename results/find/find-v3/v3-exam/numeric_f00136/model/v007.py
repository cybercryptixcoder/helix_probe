import math

def predict(probe):
    # Beliefs:
    # - Left baseline (x <= -16): linear, f(-128)=0.0479, f(-16)=0.0149, slope -0.000295 [E6]
    # - Right baseline (x >= 22): linear, f(24)=0.0003, f(76)=0.0285, slope 0.000542 [E12]
    # - Middle region [-16, 22]: complex bump-dip shape, interpolated from dense observations [E4,E8,E14,E16]
    #   rises from -16 to peak ~0.078 at -2, plateau to -0.9, then plunge to min -0.095 at 1, recovers by 22
    # - The dip is one-sided: negative side stays flat ~0.0776 until x=-0.9, then drops [E16]
    #   positive side drops steeply from x=0.1 [E16]
    
    a_L = (0.0149 - 0.0479) / (-16 - (-128))
    b_L = 0.0149 - a_L * (-16)
    a_R = (0.0285 - 0.0003) / (76 - 24)
    b_R = 0.0003 - a_R * 24
    
    anchors = [
        (-16, 0.0149), (-14, 0.0142), (-12, 0.0187), (-10, 0.0249),
        (-9, 0.028), (-8, 0.031), (-7, 0.0389), (-6, 0.0471),
        (-5.5, 0.0511), (-5, 0.055), (-4.5, 0.0589), (-4, 0.0628),
        (-3.5, 0.0667), (-3, 0.0706), (-2.5, 0.0745), (-2, 0.0784),
        (-1.5, 0.078), (-1.2, 0.0778), (-1.1, 0.0777), (-1.0, 0.0776),
        (-0.9, 0.0775), (-0.8, 0.0753), (-0.7, 0.0704), (-0.6, 0.0626),
        (-0.5, 0.049), (-0.4, 0.0372), (-0.3, 0.0277), (-0.2, 0.0182),
        (-0.1, 0.0087), (0, -0.0008), (0.1, -0.0104), (0.2, -0.0199),
        (0.3, -0.0294), (0.4, -0.0389), (0.5, -0.0484), (0.6, -0.0622),
        (0.8, -0.0876), (1, -0.0951), (1.2, -0.0895), (1.5, -0.0782),
        (1.8, -0.0667), (2, -0.0595), (2.5, -0.0507), (3, -0.0466),
        (4, -0.0438), (5, -0.0405), (6, -0.0371), (7, -0.0336),
        (8, -0.03), (10, -0.0249), (12, -0.0208), (15, -0.0146),
        (18, -0.0084), (22, -0.0008),
    ]
    
    def interp(x):
        if x <= anchors[0][0]:
            return a_L * x + b_L
        if x >= anchors[-1][0]:
            return a_R * x + b_R
        for i in range(len(anchors) - 1):
            x0, y0 = anchors[i]
            x1, y1 = anchors[i+1]
            if x0 <= x <= x1:
                t = (x - x0) / (x1 - x0)
                return y0 + t * (y1 - y0)
        return a_R * x + b_R
    
    out = []
    for xv in probe.get("x", []):
        try:
            x = float(xv)
        except (TypeError, ValueError):
            out.append(None)
            continue
        if not math.isfinite(x):
            out.append(None)
            continue
        try:
            out.append(round(interp(x), 4))
        except Exception:
            out.append(None)
    return {"y": out}

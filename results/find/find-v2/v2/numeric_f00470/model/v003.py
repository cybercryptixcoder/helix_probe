import math

def predict(probe):
    # Model hypotheses (v3):
    # - Ordinary range (|x| >= 1): f(x) = c * x^5, sign-dependent coefficient [E6,E15,E16,E17]
    #   c+ ≈ 113.87, c- ≈ 34.4 (roughly constant; slight drift is noise)
    # - Special interval |x| < 1: a smooth bump, sign-asymmetric [E2,E4,E18]
    # - At |x| = 1 exactly: f(1)=70.35, f(-1)=-35.091 [E2,E18]
    # - The special interval does NOT have a hard boundary at |x|=1: values just inside
    #   (0.85..0.98) are far from the c*x^5 law and far from a linear interp of sparse
    #   anchors; they follow a smooth curve that meets the ordinary law around |x|=1 [E18]
    # - E18 shows: f(0.85)=6.806, f(0.9)=22.9947, f(0.95)=44.9221, f(0.98)=60.0667,
    #   f(1.0)=70.35, f(1.02)=82.6472, f(1.05)=104.1206, f(1.1)=144.1608, f(1.15)=192.4859,
    #   f(1.2)=251.2048. Negative side: f(-0.85)=-2.7689, f(-0.9)=-12.1291, f(-0.95)=-22.4759,
    #   f(-0.98)=-31.3536, f(-1.0)=-35.091, f(-1.02)=-43.2404, f(-1.05)=-51.283,
    #   f(-1.1)=-72.3889, f(-1.15)=-94.7753, f(-1.2)=-120.8396.
    # - Note f(1.0)=70.35 but c+*1^5=113.87; f(-1.0)=-35.091 but c-*(-1)^5=-34.4 (close!).
    #   So the positive side has a big offset near 1; negative side nearly matches power law at 1.
    # - The special interval is |x| < 1.0 (roughly), with a smooth transition.
    #   Use dense anchors from E2/E4/E18 for |x|<1, and the power law outside.

    # Anchors for the special interval (|x| < 1), from E2, E4, E18.
    # Sorted by x.
    anchors = [
        (-1.0, -35.091),
        (-0.98, -31.3536),
        (-0.95, -22.4759),
        (-0.9, -12.1291),
        (-0.85, -2.7689),
        (-0.8, 5.8605),
        (-0.6, 22.3562),
        (-0.5, 26.692),
        (-0.3, 27.3822),
        (-0.25, 27.77),
        (-0.1, 23.8483),
        (0.0, 21.28),
        (0.1, 11.4473),
        (0.25, -3.2851),
        (0.3, -7.9163),
        (0.5, -22.9553),
        (0.6, -24.6466),
        (0.8, -3.3302),
        (0.85, 6.806),
        (0.9, 22.9947),
        (0.95, 44.9221),
        (0.98, 60.0667),
        (1.0, 70.35),
    ]

    def special(x):
        if x <= anchors[0][0]:
            return anchors[0][1]
        if x >= anchors[-1][0]:
            return anchors[-1][1]
        for i in range(len(anchors) - 1):
            x0, y0 = anchors[i]
            x1, y1 = anchors[i + 1]
            if x0 <= x <= x1:
                t = (x - x0) / (x1 - x0)
                return y0 + t * (y1 - y0)
        return 0.0

    def power(x):
        c = 113.87 if x >= 0 else 34.4
        return c * (x ** 5)

    ys = []
    for x in probe.get("x", []):
        if x is None:
            ys.append(None)
            continue
        try:
            x = float(x)
        except Exception:
            ys.append(None)
            continue
        if abs(x) < 1.0:
            ys.append(special(x))
        else:
            ys.append(power(x))
    return {"y": ys}

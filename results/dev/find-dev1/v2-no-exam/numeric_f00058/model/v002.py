def predict(probe):
    # Beliefs:
    # - Left branch: for x <= -64, y is linear with slope ~-4403.0 [E1]
    #   Points (-128,326549.8),(-64,44756.7) fit y = -4403.0*x - 237034.0
    # - Plateau: for -48 <= x <= 48, y = -84.3663 constant [E1, E2]
    # - Right branch: for x >= 64, y is linear with slope ~3783.0 [E1]
    #   Points (64,15971.3),(128,258084.0) fit y = 3783.0*x - 226141.0
    # - Left transition between -64 and -48: unknown, assume linear ramp (?)
    # - Right transition: plateau holds through x=48, then rises sharply.
    #   E2 shows y(52)=428.0, y(56)=2090.6, y(60)=6839.0, y(62)=10136.6,
    #   y(63)=13053.9, y(64)=15971.3. This is NOT linear; it's a convex
    #   curve accelerating toward the right branch. Fit a quadratic through
    #   (48,-84.37),(56,2090.6),(64,15971.3)? Let's check shape.
    #   Actually the jump from 48->52 is small (512), then grows. Looks like
    #   a smooth ramp starting around x=48. Use a quadratic anchored at
    #   x=48 (value -84.37, slope ~0) and x=64 (value 15971.3, slope 3783).
    #   Quadratic: y = a*(x-48)^2 + b*(x-48) + c with c=-84.37.
    #   At x=64: a*256 + b*16 - 84.37 = 15971.3 => 256a+16b = 16055.65
    #   Slope at 64: 2a*16 + b = 3783 => 32a + b = 3783
    #   From second: b = 3783 - 32a. Sub: 256a + 16(3783-32a)=16055.65
    #   256a + 60528 - 512a = 16055.65 => -256a = -44472.35 => a=173.72
    #   b = 3783 - 32*173.72 = 3783 - 5559 = -1776
    #   Check x=56: 173.72*64 + (-1776)*8 - 84.37 = 11118 - 14208 - 84 = -3174. Wrong.
    #   So not that shape. Try fitting quadratic through (48,-84.37),(56,2090.6),(64,15971.3):
    #   Let t=x-48. Points: t=0:-84.37, t=8:2090.6, t=16:15971.3
    #   c=-84.37. 64a+8b=2174.97 => 8a+b=271.87. 256a+16b=16055.65 => 16a+b=1003.48
    #   Subtract: 8a=731.61 => a=91.45, b=271.87-731.6=-459.73
    #   Check t=4 (x=52): 91.45*16 -459.73*4 -84.37 = 1463.2-1838.9-84.4=-460. Wrong (obs 428).
    #   So it's not a simple quadratic either. The curve is convex, steeper near 64.
    #   Use interpolation through observed points for x in [48,64], and linear
    #   extrapolation beyond. Mark as best guess (?).
    try:
        xs = probe["x"]
        out = []
        # observed anchor points in right transition
        anchors = [(48,-84.3663),(52,428.046),(56,2090.5829),(60,6838.9942),
                   (62,10136.592),(63,13053.9381),(64,15971.2842)]
        for x in xs:
            if x is None:
                out.append(None)
                continue
            x = float(x)
            if x <= -64:
                y = -4403.0 * x - 237034.0
            elif x <= -48:
                y_left = -4403.0 * (-64) - 237034.0
                t = (x + 64) / 16.0
                y = y_left + t * (-84.3663 - y_left)
            elif x <= 48:
                y = -84.3663
            elif x < 64:
                # piecewise linear interpolation through anchors (?)
                y = None
                for i in range(len(anchors)-1):
                    x0,y0 = anchors[i]; x1,y1 = anchors[i+1]
                    if x0 <= x <= x1:
                        t = (x-x0)/(x1-x0)
                        y = y0 + t*(y1-y0)
                        break
                if y is None:
                    y = -84.3663
            else:
                y = 3783.0 * x - 226141.0
            out.append(y)
        return {"y": out}
    except Exception:
        return {"y": [None] * len(probe.get("x", []))}

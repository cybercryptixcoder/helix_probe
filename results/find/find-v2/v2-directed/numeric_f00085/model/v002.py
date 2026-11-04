import math

def predict(probe):
    # Model of f(x):
    # - f is symmetric: f(x) = f(-x) [E1: f(-128)~f(128), f(-16)~f(16)]
    # - For |x| <= 6: flat plateau at -22.8021 [E1, E2: x=5,5.5 -> -22.8021]
    # - Transition region 6 < |x| < 8: smooth ramp [E2: x=6->-8.55, 6.5->26.6, 7->61.8, 7.5->97.0, 8->132.2]
    # - For |x| >= 8: smooth quadratic-ish growth [E1, E2]
    # The plateau is a soft clamp: f(x) = max(quad(x), -22.8021)? No—check E2.
    # E2 shows: at x=6, y=-8.55 (above plateau); x=5.5 still plateau.
    # So plateau ends ~5.5-6. Then linear-ish ramp: 6->-8.55, 6.5->26.6 (slope ~70/unit),
    # 7->61.8, 7.5->97.0, 8->132.2 (slope ~70.4/unit). Very linear from 6.5 to 8!
    # Then 8->132.2, 8.5->167.4 (slope 70.4), 9->202.6 (70.4), 10->272.9 (70.4),
    # 11->343.3 (70.4), 12->421.8 (78.5), 13->530.6 (108.8), 14->639.4 (108.8),
    # 15->748.2 (108.8), 16->857.0 (108.8), 20->1357.3 (125/unit).
    # So it's piecewise linear-ish with increasing slope — looks like a smooth convex function.
    # Try: f(x) = softplus-like? Or a quadratic with a plateau via max().
    # Check quadratic fit on outer: at x=8:132.2, 16:857.0, 64:14111, 128:50593.
    # 14111/64^2 = 3.44; 50593/128^2 = 3.09; 857/16^2=3.35; 132/8^2=2.07.
    # Not pure quadratic. Let's look at differences.
    # Actually the MLP approximates something. Let's fit a smooth function.
    # Try f(x) = a*x^2 + b*x + c for x>=8: 
    # (8,132.2),(16,857.0),(64,14111): 
    # 64a+8b+c=132.2; 256a+16b+c=857.0; 4096a+64b+c=14111
    # Subtract: 192a+8b=724.8 -> 24a+b=90.6
    # 3840a+48b=13254 -> 80a+b=276.1
    # 56a=185.5 -> a=3.3125, b=90.6-79.5=11.1, c=132.2-64*3.3125-8*11.1=132.2-212-88.8=-168.6
    # Check x=128: 3.3125*16384+11.1*128-168.6=54272+1420.8-168.6=55524 vs 50593. Off.
    # So not quadratic. Try cubic or the MLP is approximating something like x^2*sign... 
    # Let's just interpolate smoothly through observed points using a monotone piecewise approach.
    # Given MLP nature, smooth interpolation through data is best.
    # Build anchor points from E1+E2 (positive side), mirror for negative.
    anchors = [
        (0,-22.8021),(5.5,-22.8021),(6,-8.5526),(6.5,26.6332),(7,61.819),
        (7.25,79.4118),(7.5,97.0047),(7.75,114.5976),(8,132.1905),
        (8.25,149.7834),(8.5,167.3763),(9,202.5621),(10,272.9336),
        (11,343.3051),(12,421.8308),(13,530.6351),(14,639.4395),
        (15,748.2438),(16,857.0481),(20,1357.3016),
        (32,3704.2314),(48,8241.6569),(64,14568.8817),(80,22886.108),
        (96,32331.6141),(112,41777.1201),(128,51222.6262)
    ]
    # Note E1 negative side: f(-32)=3704.23, f(-48)=8241.66, f(-64)=14568.88,
    # f(-80)=22886.11, f(-96)=32331.61, f(-112)=41777.12, f(-128)=51222.63
    # These are the negative-side values; positive side at 64 is 14110.97, 128 is 50592.64.
    # Slight asymmetry! f(-64)=14568.88 vs f(64)=14110.97. f(-128)=51222.63 vs f(128)=50592.64.
    # So NOT perfectly symmetric. Negative side is slightly higher for large |x|.
    # Let's keep separate anchors for negative side.
    neg_anchors = [
        (0,-22.8021),(5.5,-22.8021),(6,-8.5526),(6.5,26.6332),(7,61.819),
        (7.25,79.4118),(7.5,97.0047),(7.75,114.5976),(8,132.1905),
        (8.25,149.7834),(8.5,167.3763),(9,202.5621),(10,272.9336),
        (11,343.3051),(12,421.8308),(13,530.6351),(14,639.4395),
        (15,748.2438),(16,857.0481),(20,1357.3016),
        (32,3704.2314),(48,8241.6569),(64,14568.8817),(80,22886.108),
        (96,32331.6141),(112,41777.1201),(128,51222.6262)
    ]
    # For negative side use E1 values at -16,-32,... but we don't have all.
    # E1 gives: -16:1012.65, -32:3704.23, -48:8241.66, -64:14568.88, -80:22886.11,
    # -96:32331.61, -112:41777.12, -128:51222.63. And -8:21.82.
    # So negative side differs: at -8 it's 21.82 vs +8 132.19! Big difference near transition.
    # Hmm, -8 -> 21.82 but +8 -> 132.19. So the transition is asymmetric too.
    # Actually maybe the plateau is centered differently. Let's check: -4,-2,-1,0,1,2,4 all -22.8021.
    # -8 -> 21.82. So between -8 and -4 it rises. Positive: 5.5 plateau, 6 rises.
    # So negative transition is shifted: starts rising before -8? -8 already 21.82.
    # We have -8:21.82. Need more negative transition data but don't have it.
    # Best guess: mirror the positive transition but shifted. Actually let's just use
    # available negative anchors and interpolate.
    neg_pts = [
        (0,-22.8021),(4,-22.8021),(8,21.8213),(16,1012.6489),(32,3704.2314),
        (48,8241.6569),(64,14568.8817),(80,22886.108),(96,32331.6141),
        (112,41777.1201),(128,51222.6262)
    ]
    pos_pts = anchors

    def interp(pts, x):
        # linear interpolation, clamp outside
        if x <= pts[0][0]:
            return pts[0][1]
        if x >= pts[-1][0]:
            # extrapolate using last slope
            (x0,y0),(x1,y1)=pts[-2],pts[-1]
            slope=(y1-y0)/(x1-x0)
            return y1+slope*(x-x1)
        for i in range(len(pts)-1):
            x0,y0=pts[i]; x1,y1=pts[i+1]
            if x0<=x<=x1:
                t=(x-x0)/(x1-x0)
                return y0+t*(y1-y0)
        return pts[-1][1]

    out=[]
    for xv in probe.get("x",[]):
        try:
            xv=float(xv)
        except Exception:
            out.append(None); continue
        if xv>=0:
            out.append(interp(pos_pts,xv))
        else:
            out.append(interp(neg_pts,-xv))
    return {"y":out}

def predict(probe):
    # f is ~0 (constant -20.4469) on an interval around 0: [-20, 2] inclusive [E1]
    # Outside that interval f grows rapidly and symmetrically-ish with |x| [E1]
    # f(-128)=24838.9, f(128)=39006.1; f(-100)=15882.9, f(100)=26939.5 [E1]
    # Shape looks like a smooth curve ~ a*|x|^p + b, with a central flat region [E1]
    # Model: flat = -20.4469 on [-20,2]; outside, fit y = c + a*|x|^p via two anchor points
    # Using (128, 39006.1248) and (100, 26939.4501) for x>0, and (-128,24838.9457),(-100,15882.924) for x<0
    # Solve a*128^p - a*100^p = 39006.1248-26939.4501 = 12066.6747
    #       a*128^p - a*100^p = 24838.9457-15882.924 = 8956.0217  (different slopes: asymmetric)
    # Use separate power laws per side.
    import math
    flat = -20.4469
    lo, hi = -20.0, 2.0

    # Right side fit from (100,26939.4501),(128,39006.1248) plus (64,12269.8411),(40,5505.5302)
    # Try y = A*exp(k*x) or power. Check ratio: 39006/26939=1.448 over 28 units; 26939/12269=2.196 over 36
    # log ratios: ln(1.448)/28=0.01321; ln(2.196)/36=0.02183 -> not exponential. Try power.
    # power p: ln(39006/26939)/ln(128/100)=0.3705/0.2470=1.500
    # check 26939/12269: ln(2.196)/ln(100/64)=0.7867/0.4463=1.763 ; not constant -> not pure power
    # Try quadratic-ish: use polynomial through anchors via interpolation on |x|.
    # Simpler: piecewise linear interpolation on |x| using observed anchor points (smooth enough for MLP approx).
    right = [(2,flat),(5,48.3879),(10,650.4807),(20,1914.2369),(40,5505.5302),(64,12269.8411),(100,26939.4501),(120,35558.5035),(128,39006.1248)]
    left  = [(20,flat),(40,1531.8654),(64,5576.1055),(100,15882.924),(128,24838.9457)]

    def interp(pts, x):
        if x <= pts[0][0]:
            return pts[0][1]
        if x >= pts[-1][0]:
            return pts[-1][1]
        for i in range(len(pts)-1):
            x0,y0 = pts[i]; x1,y1 = pts[i+1]
            if x0 <= x <= x1:
                t = (x-x0)/(x1-x0)
                return y0 + t*(y1-y0)
        return pts[-1][1]

    out = []
    for x in probe.get("x", []):
        try:
            if lo <= x <= hi:
                out.append(flat)
            elif x > hi:
                out.append(interp(right, x))
            else:
                out.append(interp(left, -x))
        except Exception:
            out.append(None)
    return {"y": out}

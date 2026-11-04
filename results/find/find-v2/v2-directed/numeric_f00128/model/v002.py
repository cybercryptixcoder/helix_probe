import math

def predict(probe):
    # f is a smooth function, monotone decreasing, with a kink/transition near x=0 [E1,E2,E4]
    # f(0) ~ 5.42 [E1]; near 0 slope is steep (~ -16.8 for x in [0.25,1]) [E4]
    # For x>0: slope ~ -16.8 for small x, decreasing in magnitude to ~ -16.8 at large x? 
    #   Actually from E3: between 18 and 127, y drops from -293 to -2135 over 109 => slope ~ -16.9
    #   From E2: x=0.25->4.417, x=1->-5.32 => slope ~ -13; x=1->2: -5.32->-22.68 slope -17.4
    #   So slope ~ -16.8 fairly constant for x>1. Near 0 (x in [0,0.25]) slope ~ -5.2/unit? 
    #   f(0)=5.4186, f(0.25)=4.4171 => slope -4.0; f(0.1)=5.1041 => slope -3.15
    #   So there's a rounded transition near 0.
    # For x<0: slope ~ -6.8 at large |x| (from E1: -128->-96: (651-867)/32=-6.76)
    #   near 0 from left: f(-0.1)=5.704, f(0)=5.4186 => slope -2.85; f(-0.25)=6.132 => slope -2.85
    #   f(-1)=9.3469, f(-2)=15.9142 => slope -6.57; f(-2)->-4: (29.43-15.91)/2=-6.76
    #   So for x<0, slope ~ -6.76 for |x|>1, and ~ -2.85 near 0.
    # For x>0, slope ~ -16.8 for x>1, and ~ -4 near 0.
    # There's a smooth transition region around |x| < ~1.
    # Model: piecewise with smooth blend near 0.
    # Use anchor points and linear interpolation, with fine anchors near 0.
    pts = [
        (-128,867.6846),(-96,651.3619),(-64,435.0393),(-48,326.878),(-32,218.7167),
        (-16,110.5554),(-8,56.4747),(-4,29.4344),(-3,22.6743),(-2.5,19.2942),
        (-2,15.9142),(-1.75,14.2242),(-1.5,12.5417),(-1.25,10.8971),(-1,9.3469),
        (-0.75,7.8986),(-0.5,6.8447),(-0.25,6.1321),(-0.1,5.704),(0,5.4186),
        (0.1,5.1041),(0.25,4.4171),(0.5,2.1182),(0.75,-1.3675),(1,-5.3245),
        (1.25,-9.4067),(1.5,-13.7572),(1.75,-18.2649),(2,-22.6804),(2.5,-31.1292),
        (3,-39.4742),(4,-56.3287),(5,-73.2881),(7,-107.1067),(8,-124.0066),
        (16,-259.2056),(32,-529.6037),(48,-800.0018),(64,-1070.3998),(128,-2151.9921)
    ]
    xs = probe.get("x", [])
    out = []
    for x in xs:
        try:
            x = float(x)
        except Exception:
            out.append(None); continue
        if x <= pts[0][0]:
            s = (pts[1][1]-pts[0][1])/(pts[1][0]-pts[0][0])
            out.append(pts[0][1] + s*(x-pts[0][0]))
        elif x >= pts[-1][0]:
            s = (pts[-1][1]-pts[-2][1])/(pts[-1][0]-pts[-2][0])
            out.append(pts[-1][1] + s*(x-pts[-1][0]))
        else:
            for i in range(len(pts)-1):
                x0,y0 = pts[i]; x1,y1 = pts[i+1]
                if x0 <= x <= x1:
                    t = (x-x0)/(x1-x0)
                    out.append(y0 + t*(y1-y0))
                    break
    return {"y": out}

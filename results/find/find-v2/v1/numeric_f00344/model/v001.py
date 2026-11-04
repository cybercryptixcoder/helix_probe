import math

def predict(probe):
    try:
        xs = probe.get("x", [])
        out = []
        for x in xs:
            try:
                out.append(_f(float(x)))
            except Exception:
                out.append(None)
        return {"y": out}
    except Exception:
        return {"y": []}

def _f(x):
    # Small-|x| regime: interpolate through observed points near 0
    # Observed: (-1,-7.4),(-0.5,-10.375),(0,472.73),(0.5,-37.825),(1,-41.7)
    if -1.0 <= x <= 1.0:
        pts = [(-1.0,-7.4),(-0.5,-10.375),(0.0,472.73),(0.5,-37.825),(1.0,-41.7)]
        # piecewise linear interpolation
        for i in range(len(pts)-1):
            x0,y0 = pts[i]; x1,y1 = pts[i+1]
            if x0 <= x <= x1:
                t = (x - x0)/(x1 - x0)
                return y0 + t*(y1 - y0)
        return pts[-1][1]
    # Outside: exponential growth in magnitude, negative sign
    # Use log-linear fit from data:
    # x=4 -> -528, x=8 -> -6443.2, x=16 -> -90763.2, x=32 -> -1355761.6, x=64 -> -20915544, x=128 -> -328399499.2
    # log|y| vs x: roughly slope ~0.6? Let's estimate from 4->528 (log 6.27), 128->3.28e8 (log 19.6): slope=(19.6-6.27)/124=0.1075
    # Hmm that's not 0.6. Let's check 4->8: log(6443/528)=log(12.2)=2.5 over 4 -> 0.626. 8->16: log(14.1)=2.65/8=0.33. 16->32: log(14.9)=2.7/16=0.169. 32->64: log(15.4)=2.73/32=0.085. 64->128: log(15.7)=2.75/64=0.043.
    # Slope decreases. Looks like log|y| ~ a + b*log|x|? Check: log|y| vs log|x|:
    # x=4: log4=1.386, log528=6.27; x=128: log128=4.852, log3.28e8=19.6
    # slope=(19.6-6.27)/(4.852-1.386)=13.33/3.466=3.85. So |y| ~ C * |x|^3.85
    # Check x=8: log8=2.079, predicted log|y|=6.27+3.85*(2.079-1.386)=6.27+2.67=8.94 -> 7650 vs actual 6443. Close-ish.
    # Check x=16: log16=2.773, pred=6.27+3.85*(2.773-1.386)=6.27+5.34=11.61 -> 110000 vs 90763. Close.
    # Check x=32: log32=3.466, pred=6.27+3.85*(3.466-1.386)=6.27+8.01=14.28 -> 1.6e6 vs 1.36e6. Close.
    # Check x=64: log64=4.159, pred=6.27+3.85*(4.159-1.386)=6.27+10.68=16.95 -> 2.3e7 vs 2.09e7. Close.
    # So |y| ~ C*|x|^3.85 with C from x=4: 528/4^3.85 = 528/ (4^3.85). 4^3.85 = e^(3.85*1.386)=e^5.337=207.9. C=528/207.9=2.54.
    # Check x=128: 2.54*128^3.85 = 2.54*e^(3.85*4.852)=2.54*e^18.68=2.54*1.29e8=3.28e8. 
    # Negative side: x=-4 -> -106.1, x=-8 -> -3320.5, x=-16 -> -66110.9, x=-32 -> -1159026.1, x=-64 -> -19342450.1, x=-128 -> -24973124.5656
    # Wait -128 and -100 are close: -24973124.56 and -24973124.53. That's odd - nearly flat!
    # -64 -> -19342450.1, -100 -> -24973124.53, -128 -> -24973124.5656. Saturating around -2.5e7.
    # Hmm. Let me reconsider. Maybe negative side saturates.
    # For x<=-64, y saturates near -2.5e7. For -64<x<-4, grows.
    # Let's fit negative side for -64<=x<=-4: log|y| vs log|x|:
    # x=-4: log4=1.386, log106=4.66; x=-64: log64=4.159, log1.93e7=16.78
    # slope=(16.78-4.66)/(4.159-1.386)=12.12/2.773=4.37. C=106/4^4.37=106/e^(4.37*1.386)=106/e^6.06=106/428=0.248
    # Check x=-8: 0.248*8^4.37=0.248*e^(4.37*2.079)=0.248*e^9.09=0.248*8880=2202 vs 3320. Off.
    # Check x=-16: 0.248*16^4.37=0.248*e^(4.37*2.773)=0.248*e^12.12=0.248*1.83e5=45400 vs 66110. Off.
    # Check x=-32: 0.248*32^4.37=0.248*e^(4.37*3.466)=0.248*e^15.15=0.248*3.8e6=9.4e5 vs 1.16e6. Close.
    # Check x=-64: 0.248*64^4.37=0.248*e^(4.37*4.159)=0.248*e^18.18=0.248*7.9e7=1.96e7 vs 1.93e7. 
    # So negative side: |y| ~ 0.248*|x|^4.37 for -64<=x<=-4, saturating near -2.5e7 for x<=-64.
    
    ax = abs(x)
    if x > 0:
        # positive side: |y| ~ 2.54 * x^3.85
        val = 2.54 * (ax ** 3.85)
        return -val
    else:
        # negative side
        if ax >= 64:
            # saturate near -2.5e7
            # smooth approach
            return -24973124.5656
        else:
            val = 0.248 * (ax ** 4.37)
            return -val

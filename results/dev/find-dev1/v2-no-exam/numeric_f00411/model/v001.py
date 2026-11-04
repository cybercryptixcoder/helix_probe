import math

def predict(probe):
    # Model hypotheses from E1:
    # For x >= 0: y = 12 + 2*x + 0.02*x^2 approximately? Let's check.
    # x=0: 444.28 is an outlier/spike (special point at 0)
    # x=0.5: 10.7, x=1: 12.0, x=2: 14.6, x=4: 19.8, x=8: 30.2, x=16: 51.0
    # x=32: 92.6, x=64: 175.8, x=96: 259.0, x=128: 342.2
    # Differences: 12->14.6 (2.6 for +1), 14.6->19.8 (5.2 for +2), 19.8->30.2 (10.4 for +4)
    # Looks like y = 12 + 2*x + something? x=1:14, x=2:16, x=4:20, x=8:28, x=16:44, x=32:76, x=64:140, x=128:268
    # Actual: 12,14.6,19.8,30.2,51,92.6,175.8,342.2
    # Try y = 12 + 2*x + 0.02*x^2? x=128: 12+256+327.68=595 no
    # Try y = 12 + 2*x + 0.01*x^2? x=128: 12+256+163.84=431.84 no
    # Try y = 12 + 2*x + 0.005*x^2? x=128: 12+256+81.92=349.92 close to 342.2
    # x=64: 12+128+20.48=160.48 vs 175.8 no
    # Try exponential-ish: 12,14.6,19.8,30.2,51,92.6,175.8,342.2
    # ratios: 14.6/12=1.217, 19.8/14.6=1.356, 30.2/19.8=1.525, 51/30.2=1.689, 92.6/51=1.816, 175.8/92.6=1.899, 342.2/175.8=1.947
    # approaching 2. Try y = 12*2^(x/16)? x=16: 24 no
    # Try y = 12 + something. Let's fit y = a + b*2^(x/c)
    # x=0: 12 (ignoring spike), x=16: 51, x=32: 92.6, x=64: 175.8, x=128: 342.2
    # 342.2-175.8=166.4, 175.8-92.6=83.2, 92.6-51=41.6, 51-12=39
    # Differences double every 32 units roughly: 41.6, 83.2, 166.4 -> ratio 2 per 32
    # So y = 12 + 41.6/2 * (2^(x/32) - 1)? At x=32: 12+20.8*(2-1)=32.8 no
    # Try y = A + B*2^(x/32). x=32: A+2B=92.6, x=64: A+4B=175.8 -> 2B=83.2, B=41.6, A=9.4
    # Check x=128: 9.4+41.6*16=9.4+665.6=675 no
    # Hmm. Try y = A + B*2^(x/64). x=64: A+2B=175.8, x=128: A+4B=342.2 -> 2B=166.4, B=83.2, A=9.4
    # x=32: 9.4+83.2*sqrt(2)=9.4+117.7=127 no
    # Try y = 12 + 2*x + x^2/... let's just do piecewise linear interpolation? No, need formula.
    # Actually check: y = 12 + 2*x + 0.02*x^2 for small x? x=4: 12+8+0.32=20.32 vs 19.8
    # x=8: 12+16+1.28=29.28 vs 30.2
    # x=16: 12+32+5.12=49.12 vs 51
    # x=32: 12+64+20.48=96.48 vs 92.6
    # x=64: 12+128+81.92=221.92 vs 175.8 no
    # Try y = 12 + 2*x + 0.01*x^1.5? x=64: 12+128+5.12=145 no
    # Try y = 12*2^(x/32) + something? x=0:12, x=32:24 no
    # Let's look: 12, 14.6, 19.8, 30.2, 51, 92.6, 175.8, 342.2
    # 12 = 12, 14.6, 19.8, 30.2, 51, 92.6, 175.8, 342.2
    # y-12: 0, 2.6, 7.8, 18.2, 39, 80.6, 163.8, 330.2
    # ratios of (y-12): 2.6, 7.8 (x3), 18.2 (x2.33), 39 (x2.14), 80.6 (x2.07), 163.8 (x2.03), 330.2 (x2.02)
    # approaching 2 per doubling. So y-12 ~ C*2^(x/16)? x=16: 39, x=32: 80.6, x=64: 163.8, x=128: 330.2
    # 39*2=78 vs 80.6, 80.6*2=161.2 vs 163.8, 163.8*2=327.6 vs 330.2
    # So y-12 = 39*2^((x-16)/16) + small correction? 
    # x=16: 39, x=32: 78+2.6, x=64: 156+7.8, x=128: 312+18.2
    # correction: 0, 2.6, 7.8, 18.2 -> these are the (y-12) values at x=0,1,2? No.
    # Actually correction at x=32 is 2.6 = (y-12) at x=1. At x=64: 7.8 = (y-12) at x=2. At x=128: 18.2 = (y-12) at x=4.
    # So y(x) = 12 + 39*2^((x-16)/16) + (y(x/32)-12)? That's recursive, weird.
    # Let's try: y(x) = 12 + 2*x + 0.02*x^2 for x<=16? x=16: 12+32+5.12=49.12 vs 51 close-ish
    # Hmm, maybe y = 12 + 2*x + x^2/50? x=16: 12+32+5.12=49.12, x=32: 12+64+20.48=96.48 vs 92.6
    # x=64: 12+128+81.92=221.92 vs 175.8 no
    # Try y = 12 + 2*x + x^2/100? x=64: 12+128+40.96=180.96 vs 175.8 close
    # x=128: 12+256+163.84=431.84 vs 342.2 no
    # Try y = 12 + 2*x + x^2/200? x=128: 12+256+81.92=349.92 vs 342.2 close
    # x=64: 12+128+20.48=160.48 vs 175.8 no
    # Not quadratic. Let's try y = 12 + 2*x + 0.02*x^2 for x<=16, then different?
    # Actually maybe it's y = 12 + 2*x + 0.02*x^2 for x<=16? x=8: 12+16+1.28=29.28 vs 30.2
    # x=4: 12+8+0.32=20.32 vs 19.8
    # x=2: 12+4+0.08=16.08 vs 14.6 no
    # Try y = 12 + 2*x + 0.01*x^2? x=2: 12+4+0.04=16.04 vs 14.6
    # Hmm x=1:12, x=2:14.6, x=4:19.8, x=8:30.2
    # 12, 14.6, 19.8, 30.2: differences 2.6, 5.2, 10.4 -> exactly doubling!
    # So for x in [1,8]: y(2x) = y(x) + 2*(y(x)-y(x/2))? 
    # Actually y(2)-y(1)=2.6, y(4)-y(2)=5.2=2*2.6, y(8)-y(4)=10.4=2*5.2
    # So y(x) = 12 + 2.6*(2^(log2(x)) - 1)? For x=1: 12, x=2: 14.6, x=4: 19.8, x=8: 30.2
    # y(x) = 12 + 2.6*(x-1)? x=2: 14.6, x=4: 19.8, x=8: 30.2, x=16: 51, x=32: 92.6
    # x=16: 12+2.6*15=51 YES! x=32: 12+2.6*31=92.6 YES!
    # x=64: 12+2.6*63=175.8 YES! x=128: 12+2.6*127=342.2 YES!
    # x=0.5: 12+2.6*(-0.5)=10.7 YES!
    # So for x >= 0 (except 0): y = 12 + 2.6*(x-1) = 9.4 + 2.6*x
    # Check x=0: 9.4, but observed 444.28. So x=0 is special spike.
    # For x < 0: -0.5:12.9, -1:11.6, -2:9.0, -4:3.8, -8:-6.6, -16:-27.4, -32:-69.0, -64:-152.2, -128:-318.6
    # Try y = 9.4 + 2.6*x for negative? x=-1: 6.8 vs 11.6 no
    # Try y = 12 + 2.6*x? x=-1: 9.4 vs 11.6 no
    # Let's see: -0.5:12.9, -1:11.6, -2:9.0, -4:3.8, -8:-6.6, -16:-27.4
    # differences: -1.3, -2.6, -5.2, -10.4, -20.8 -> doubling
    # So y(-x) = 12.9 - 1.3*(2^(log2(2x))-1)? For x=-0.5: 12.9, x=-1: 11.6, x=-2: 9.0
    # y = 12.9 - 1.3*(2x-1)? x=-1: 12.9-1.3*1=11.6, x=-2: 12.9-1.3*3=9.0, x=-4: 12.9-1.3*7=3.8
    # x=-8: 12.9-1.3*15=-6.6 YES! x=-16: 12.9-1.3*31=-27.4 YES!
    # x=-32: 12.9-1.3*63=-69.0 YES! x=-64: 12.9-1.3*127=-152.2 YES!
    # x=-128: 12.9-1.3*255=-318.6 YES!
    # So for x < 0: y = 12.9 - 1.3*(2*(-x)-1) = 12.9 + 1.3 - 2.6*(-x) = 14.2 + 2.6*x
    # Check x=-0.5: 14.2-1.3=12.9 YES
    # So for x<0: y = 14.2 + 2.6*x
    # For x>0: y = 9.4 + 2.6*x
    # At x=0: spike 444.28
    # Discontinuity at 0: left limit 14.2, right limit 9.4, actual 444.28
    # Maybe x=0 is a special value. Or maybe the formula is y = 9.4 + 2.6*x for x>0, y=14.2+2.6*x for x<0, and x=0 gives 444.28.
    # Or maybe there's a small interval around 0? Only tested x=0. Let's assume only x=0 special.
    # Actually maybe y = 9.4 + 2.6*x + 434.88*delta(x,0)? 
    # Let's just model: x>0: 9.4+2.6x, x<0: 14.2+2.6x, x==0: 444.28
    # But wait, maybe the spike is at x=0 only, or maybe there's a narrow interval. We only have one data point.
    # Let's also consider: maybe y = 9.4 + 2.6*x for x>=0 except x=0, and the 444.28 is a spike.
    # Actually, could it be y = 9.4 + 2.6*x + 434.88*exp(-x^2/s)? At x=0: 444.28, at x=0.5: 10.7 (no spike contribution). 
    # exp(-0.25/s) negligible if s small. But we don't know. Let's just do x==0 special.
    # Hmm, but what if there's an interval? Let's test more values near 0 in a future probe.
    # For now: piecewise linear with spike at 0.
    
    xs = probe["x"]
    ys = []
    for x in xs:
        if x == 0:
            ys.append(444.28)
        elif x > 0:
            ys.append(9.4 + 2.6 * x)
        else:
            ys.append(14.2 + 2.6 * x)
    return {"y": ys}

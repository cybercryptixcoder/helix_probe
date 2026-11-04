import math

def predict(probe):
    # Model hypotheses from E1:
    # For large |x|, y grows roughly like x^2 (e.g. 88.2 -> 1150.92, 66 -> 860.1, 72.7 -> 946.87)
    #   Check: 88.2^2 = 7779 too big; sqrt(1150.92)=33.9; 88.2*13.05? Let's test x^2/6.76...
    #   Actually 1150.92/88.2 = 13.05; 860.1/66 = 13.03; 946.87/72.7 = 13.02. So y ~ 13*x for large x!
    #   Wait: 88.2*13.05=1151, 66*13.03=860, 72.7*13.02=947. So y ≈ 13*x for large positive x.
    # For negative large: -61.7 -> -91.727; ratio 1.487. -50.4 -> -76.924; ratio 1.526. Not 13.
    # Small: 2.9 -> 34.49; ratio 11.9. -6 -> -18.76; ratio 3.13. -20.3 -> -37.493; ratio 1.847.
    # -24.3 -> -40.733; ratio 1.676. 21.3 -> 273.53; ratio 12.84.
    # Hypothesis: y = x * something. For x>0 large: ~13x. For x>0 small: 2.9->34.49 (11.9x), 21.3->273.53 (12.84x).
    # Try y = x * (x+something)? 88.2: 88.2*(88.2+a)=1150.92 -> 88.2+a=13.05 -> a=-75.15. No.
    # Try y = x^2/k? 88.2^2=7779/1150.92=6.76. 66^2=4356/860.1=5.065. No.
    # Try y = x^2/(x+c)? 88.2^2/1150.92 = 6.76 = 88.2+c -> c=-81.4. 66^2/860.1=5.065=66+c -> c=-60.9. No.
    # Try y = a*x + b*x^2? 
    #   Use 88.2, 66: 88.2a+7779b=1150.92; 66a+4356b=860.1
    #   From 2nd: a=(860.1-4356b)/66=13.032-66b
    #   Sub: 88.2(13.032-66b)+7779b=1150.92 -> 1149.4-5821b+7779b=1150.92 -> 1958b=1.52 -> b=0.000776, a=12.98
    #   Check 72.7: 12.98*72.7+0.000776*5285=943.6+4.1=947.7 vs 946.87. Close!
    #   Check 21.3: 12.98*21.3+0.000776*453.7=276.5+0.35=276.8 vs 273.53. Off by 3.
    #   Check 2.9: 12.98*2.9+0.000776*8.41=37.6 vs 34.49. Off.
    # Try y = x^2/(x+c) form differently, or piecewise.
    # Notice negatives: -61.7->-91.727 (1.487x), -50.4->-76.924 (1.526x), -24.3->-40.733 (1.676x), -20.3->-37.493 (1.847x), -6->-18.76 (3.127x)
    #   As x->0-, ratio grows. Try y = x + x^2/something? -6: -6+36/k=-18.76 -> 36/k=-12.76 -> k=-2.82. 
    #   -20.3: -20.3+412/k=-37.493 -> 412/k=-17.19 -> k=-23.97. No.
    # Try y = x^2/(x+c) with different c for negatives? -6: 36/(-6+c)=-18.76 -> -6+c=-1.919 -> c=4.08. 
    #   -20.3: 412/(-20.3+c)=-37.493 -> -20.3+c=-10.99 -> c=9.31. No.
    # Try y = x*|x|/k? -6: 36/k=-18.76 -> k=-1.919. -20.3: 412/k=-37.49 -> k=-10.99. No.
    # Try y = x^2/k with sign? -6: 36/k=-18.76 -> k=-1.919; -20.3: 412/k=-37.49 -> k=-10.99. No.
    # Try y = a*x^2 + b*x + c fit to negatives:
    #   -6: 36a-6b+c=-18.76
    #   -20.3: 412.09a-20.3b+c=-37.493
    #   -61.7: 3806.89a-61.7b+c=-91.727
    #   Diff1: 376.09a-14.3b=-18.733
    #   Diff2: 3394.8a-41.4b=-54.234
    #   From Diff1: b=(376.09a+18.733)/14.3=26.3a+1.31
    #   Diff2: 3394.8a-41.4(26.3a+1.31)=-54.234 -> 3394.8a-1088.8a-54.2=-54.234 -> 2306a=0 -> a≈0
    #   So b≈1.31, c: 36*0-6*1.31+c=-18.76 -> c=-10.9. Check -50.4: 1.31*(-50.4)-10.9=-66-10.9=-76.9. Yes! -76.924!
    #   Check -24.3: 1.31*(-24.3)-10.9=-31.8-10.9=-42.7 vs -40.733. Close-ish.
    #   Check -61.7: 1.31*(-61.7)-10.9=-80.8-10.9=-91.7. Yes!
    #   So negatives: y ≈ 1.31*x - 10.9? But -6: 1.31*(-6)-10.9=-7.86-10.9=-18.76. Yes!
    #   -20.3: 1.31*(-20.3)-10.9=-26.6-10.9=-37.5. Yes!
    #   -24.3: 1.31*(-24.3)-10.9=-31.83-10.9=-42.7 vs -40.733. Hmm off by 2.
    #   Maybe slope slightly different. Let's fit -6 and -61.7: slope=(-91.727+18.76)/(-61.7+6)=-72.967/-55.7=1.31. intercept: -18.76-1.31*(-6)=-18.76+7.86=-10.9. 
    #   -24.3 predicted -42.7 vs -40.733. -50.4 predicted -76.9 vs -76.924 ok. -20.3 predicted -37.5 vs -37.493 ok.
    #   Only -24.3 off. Maybe noise. So negatives: y = 1.31*x - 10.9 roughly.
    # Positives: 2.9->34.49, 21.3->273.53, 66->860.1, 72.7->946.87, 88.2->1150.92
    #   Try y = a*x^2+b*x+c. 2.9,21.3,66:
    #   8.41a+2.9b+c=34.49
    #   453.69a+21.3b+c=273.53
    #   4356a+66b+c=860.1
    #   D1: 445.28a+18.4b=239.04
    #   D2: 3902.31a+44.7b=586.57
    #   From D1: b=(239.04-445.28a)/18.4=12.99-24.2a
    #   D2: 3902.31a+44.7(12.99-24.2a)=586.57 -> 3902.31a+580.65-1081.7a=586.57 -> 2820.6a=5.92 -> a=0.0021, b=12.94
    #   c: 8.41*0.0021+2.9*12.94+c=34.49 -> 0.018+37.53+c=34.49 -> c=-3.06
    #   Check 72.7: 0.0021*5285+12.94*72.7-3.06=11.1+940.7-3.06=948.7 vs 946.87. Close.
    #   Check 88.2: 0.0021*7779+12.94*88.2-3.06=16.3+1141.3-3.06=1154.5 vs 1150.92. Close.
    #   So positives: y ≈ 0.0021x^2 + 12.94x - 3.06. Roughly y≈13x for large.
    # This is messy. Maybe simpler: y = x + 12*max(x,0) + ...? 
    #   For x>0: y ≈ 13x. For x<0: y ≈ 1.31x - 10.9.
    #   Hmm, maybe y = x + 12*relu(x) - something? 
    #   x>0: x+12x=13x. 88.2*13=1146.6 vs 1150.92. 66*13=858 vs 860.1. 72.7*13=945.1 vs 946.87. 21.3*13=276.9 vs 273.53. 2.9*13=37.7 vs 34.49.
    #   Close but not exact. Maybe y = x + 12*relu(x) + small quadratic.
    # For x<0: y = x + 0.31x - 10.9 = 1.31x-10.9. Or y = x - 10.9 + 0.31x.
    #   Hmm -10.9 constant for negatives. Maybe y = x + 12*relu(x) - 10.9*relu(-x)? 
    #   x<0: y = x - 10.9. -6: -16.9 vs -18.76. No.
    # Try y = x + 12*relu(x) + 0.31*min(x,0) - 10.9*indicator(x<0)?
    #   This is getting complicated. Let me just use piecewise linear fit.
    # Positives: fit line through (2.9,34.49) and (88.2,1150.92): slope=(1150.92-34.49)/85.3=13.09, intercept=34.49-13.09*2.9=-3.47
    #   Check 66: 13.09*66-3.47=860.5 vs 860.1. Good. 72.7: 948.2 vs 946.87. 21.3: 275.4 vs 273.53. OK.
    # Negatives: slope 1.31, intercept -10.9.
    # But there's a discontinuity at 0: as x->0+, y->-3.47; as x->0-, y->-10.9. 
    # Maybe there's a region near 0 that's different. But we only have data.
    # Let me just do piecewise linear: x>=0: 13.09x-3.47; x<0: 1.31x-10.9.
    # Actually check x=0: would be -3.47 or -10.9. Unknown.
    # Let me refine positives with least squares on all 5 points.
    # Points: (2.9,34.49),(21.3,273.53),(66,860.1),(72.7,946.87),(88.2,1150.92)
    # Sum x=251.1, sum y=3265.91, sum x^2=2.9^2+21.3^2+66^2+72.7^2+88.2^2=8.41+453.69+4356+5285.29+7779.24=17882.63
    # sum xy=2.9*34.49+21.3*273.53+66*860.1+72.7*946.87+88.2*1150.92
    #   =100.02+5826.19+56766.6+68837.45+101511.14=233041.4
    # n=5. slope=(5*233041.4-251.1*3265.91)/(5*17882.63-251.1^2)
    #   =(1165207-820083)/(89413.15-63051.21)=345124/26361.94=13.09
    # intercept=(3265.91-13.09*251.1)/5=(3265.91-3286.9)/5=-4.2
    # So positives: y≈13.09x-4.2
    # Negatives: points (-6,-18.76),(-20.3,-37.493),(-24.3,-40.733),(-50.4,-76.924),(-61.7,-91.727)
    # sum x=-162.7, sum y=-265.637, sum x^2=36+412.09+590.49+2540.16+3806.89=7385.63
    # sum xy=(-6)(-18.76)+(-20.3)(-37.493)+(-24.3)(-40.733)+(-50.4)(-76.924)+(-61.7)(-91.727)
    #   =112.56+761.11+989.81+3876.97+5660.56=11401.01
    # slope=(5*11401.01-(-162.7)(-265.637))/(5*7385.63-162.7^2)
    #   =(57005.05-43219.14)/(36928.15-26471.29)=13785.91/10456.86=1.318
    # intercept=(-265.637-1.318*(-162.7))/5=(-265.637+214.44)/5=-10.24
    # So negatives: y≈1.318x-10.24
    # Check -24.3: 1.318*(-24.3)-10.24=-32.03-10.24=-42.27 vs -40.733. Off by 1.5.
    # Hmm. Maybe there's a quadratic term. Let me try y = a*x^2+b*x+c for negatives again with all 5.
    # Actually the -24.3 point is the outlier. Maybe noise. I'll go with linear.
    # But wait, maybe the function is y = x + 12*relu(x) - 10.24*relu(-x) + ...? 
    #   x<0: x - 10.24 = 1x-10.24, but we need 1.318x. So y = 1.318x - 10.24 for x<0.
    #   x>0: 13.09x-4.2.
    # Could be y = x + 12.09*relu(x) - 4.2*indicator(x>0) + 0.318*min(x,0) - 10.24*indicator(x<0)?
    # Too complex. Piecewise linear is fine.
    # Actually maybe simpler: y = x + 12*relu(x) + 0.318*min(x,0) - 10.24*indicator(x<0) - 4.2*indicator(x>0)?
    # Let me just do piecewise.
    # But there might be an interval where behavior differs. We only have data at these points. 
    # Let me check if there's a simpler form: y = x + 12*relu(x) + something.
    # For x>0: y-x = 12.09x-4.2. For x<0: y-x = 0.318x-10.24.
    # Hmm, 0.318x-10.24 for x<0... at x=0 gives -10.24. 
    # Maybe y = x + 12*relu(x) - 10.24 + 0.318*min(x,0) + ... no.
    # I'll go with piecewise linear. It's the best fit.
    
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
            if x >= 0:
                y = 13.09 * x - 4.2
            else:
                y = 1.318 * x - 10.24
            ys.append(y)
        except Exception:
            ys.append(None)
    return {"y": ys}

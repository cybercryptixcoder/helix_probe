import math

def predict(probe):
    # E2 reveals a sharp spike at x=0: y(0) = -385.12, far below the linear branches.
    # For x != 0 the behavior is essentially linear with a kink at 0:
    #   x>0: y = 13*x + 0.5   [E2: 0.5->4.05? no. Let's fit]
    # E2 positives: (0.5,4.05),(1,10.6),(2,20.7),(5,60),(10,127.5),(15,191),(30,389.5),(45,585),(60,780.5),(100,1305.5),(120,1567.5)
    #   slope ~13.0, intercept ~0.5? 13*0.5=6.5 vs 4.05. 13*1=13 vs 10.6. 13*2=26 vs 20.7.
    #   Try y = 13x - 2.5: 0.5->4.0 (4.05 ok), 1->10.5 (10.6), 2->23.5 (20.7 off), 5->62.5 (60), 10->127.5 (127.5!), 15->192.5 (191), 30->387.5 (389.5), 45->582.5 (585), 60->777.5 (780.5), 100->1297.5 (1305.5), 120->1557.5 (1567.5).
    #   Hmm at large x slope slightly >13. Fit (10,127.5) and (120,1567.5): slope=(1567.5-127.5)/110=13.09, intercept=127.5-130.9=-3.4.
    #   Check 60: 13.09*60-3.4=782 vs 780.5. 30: 389.3 vs 389.5. 5: 62.05 vs 60. 2: 22.78 vs 20.7. 1: 9.69 vs 10.6. 0.5: 3.15 vs 4.05.
    #   E1 positives: 2.9->34.49, 21.3->273.53, 66->860.1, 72.7->946.87, 88.2->1150.92
    #   13.09*2.9-3.4=34.56 (34.49 ok). 13.09*21.3-3.4=275.4 (273.53). 13.09*66-3.4=860.5 (860.1). 13.09*72.7-3.4=948.2 (946.87). 13.09*88.2-3.4=1151.1 (1150.92).
    #   Good. Positives: y ≈ 13.09x - 3.4.
    # E2 negatives: (-0.5,-10.555),(-1,-10.21),(-2,-12.52),(-5,-16.45),(-10,-22),(-15,-30.55),(-30,-50.2),(-100,-141.9)
    #   slope ~1.3, intercept ~-10.2? -0.5: 1.3*(-0.5)-10.2=-10.85 vs -10.555. -1: -11.5 vs -10.21. -2: -12.8 vs -12.52. -5: -16.7 vs -16.45. -10: -23.2 vs -22. -15: -29.7 vs -30.55. -30: -49.2 vs -50.2. -100: -140.2 vs -141.9.
    #   Fit (-10,-22) and (-100,-141.9): slope=(-141.9+22)/(-90)=1.332, intercept=-22-1.332*(-10)=-8.68.
    #   Check -30: 1.332*(-30)-8.68=-48.64 vs -50.2. -15: -28.66 vs -30.55. -5: -15.34 vs -16.45. -2: -11.34 vs -12.52. -1: -10.01 vs -10.21. -0.5: -9.35 vs -10.555.
    #   Hmm. E1 negatives: (-6,-18.76),(-20.3,-37.493),(-24.3,-40.733),(-50.4,-76.924),(-61.7,-91.727)
    #   1.332*(-6)-8.68=-16.67 vs -18.76. 1.332*(-20.3)-8.68=-35.72 vs -37.49. 1.332*(-24.3)-8.68=-41.05 vs -40.73. 1.332*(-50.4)-8.68=-75.81 vs -76.92. 1.332*(-61.7)-8.68=-90.86 vs -91.73.
    #   Slight curvature. Try y = a*x + b + c/x? Or quadratic.
    #   Fit quadratic to negatives using E1+E2 points. Let's just use a*x+b with best fit.
    #   Actually the -24.3 point in E1 was an outlier for linear. Let's try y = 1.3*x - 10.2 + small quadratic.
    #   Let's fit y = a*x^2 + b*x + c to negatives (all 13 points). 
    #   Quick: use (-100,-141.9),(-30,-50.2),(-1,-10.21):
    #   10000a-100b+c=-141.9
    #   900a-30b+c=-50.2
    #   a-b+c=-10.21
    #   D1: 9100a-70b=-91.7 -> 130a-b=-1.31 -> b=130a+1.31
    #   D2: 899a-29b=-39.99 -> 899a-29(130a+1.31)=-39.99 -> 899a-3770a-37.99=-39.99 -> -2871a=-2 -> a=0.000697, b=1.4006
    #   c: 0.000697-1.4006+c=-10.21 -> c=-8.81
    #   Check -6: 0.000697*36+1.4006*(-6)-8.81=0.025-8.40-8.81=-17.19 vs -18.76. Off 1.6.
    #   Check -20.3: 0.287-28.43-8.81=-36.95 vs -37.49. Off 0.5.
    #   Check -50.4: 1.77-70.59-8.81=-77.63 vs -76.92. Off 0.7.
    #   Check -61.7: 2.65-86.42-8.81=-92.58 vs -91.73. Off 0.85.
    #   Check -0.5: 0.00017-0.70-8.81=-9.51 vs -10.555. Off 1.
    #   Check -2: 0.0028-2.80-8.81=-11.61 vs -12.52. Off 0.9.
    #   Check -5: 0.017-7.00-8.81=-15.79 vs -16.45. Off 0.66.
    #   Check -10: 0.07-14.01-8.81=-22.75 vs -22. Off 0.75.
    #   Check -15: 0.157-21.01-8.81=-29.66 vs -30.55. Off 0.9.
    #   Not great. The data seems noisy. Let's just use linear fit.
    #   Best linear fit to all negatives (E1+E2):
    #   Points: (-0.5,-10.555),(-1,-10.21),(-2,-12.52),(-5,-16.45),(-6,-18.76),(-10,-22),(-15,-30.55),(-20.3,-37.493),(-24.3,-40.733),(-30,-50.2),(-50.4,-76.924),(-61.7,-91.727),(-100,-141.9)
    #   Sum x = -(0.5+1+2+5+6+10+15+20.3+24.3+30+50.4+61.7+100) = -326.2
    #   Sum y = -(10.555+10.21+12.52+16.45+18.76+22+30.55+37.493+40.733+50.2+76.924+91.727+141.9) = -560.022
    #   Sum x^2 = 0.25+1+4+25+36+100+225+412.09+590.49+900+2540.16+3806.89+10000 = 18640.88
    #   Sum xy = 0.5*10.555+1*10.21+2*12.52+5*16.45+6*18.76+10*22+15*30.55+20.3*37.493+24.3*40.733+30*50.2+50.4*76.924+61.7*91.727+100*141.9
    #     =5.2775+10.21+25.04+82.25+112.56+220+458.25+761.11+989.81+1506+3876.97+5660.56+14190
    #     =27898.04
    #   n=13. slope=(13*27898.04-(-326.2)(-560.022))/(13*18640.88-326.2^2)
    #     =(362674.5-182680.4)/(242331.4-106406.4)=179994.1/135925=1.3242
    #   intercept=(-560.022-1.3242*(-326.2))/13=(-560.022+431.95)/13=-9.852
    #   So negatives: y ≈ 1.324x - 9.85.
    #   Check -24.3: 1.324*(-24.3)-9.85=-32.17-9.85=-42.02 vs -40.733. Off 1.3. (noise)
    #   Check -6: -7.94-9.85=-17.79 vs -18.76. Off 1.
    #   Check -100: -132.4-9.85=-142.25 vs -141.9. Good.
    #   Check -0.5: -0.66-9.85=-10.51 vs -10.555. Good.
    #   Check -1: -1.32-9.85=-11.17 vs -10.21. Off 1.
    #   OK, decent.
    # Positives best fit: y ≈ 13.09x - 3.4 (from above).
    # The spike at x=0: y(0) = -385.12. This is a special point. 
    #   Could be a narrow interval around 0 where y is very negative. But we only have x=0 exactly.
    #   Maybe y = -385.12 at x=0 only (a single point anomaly), or a narrow dip.
    #   Given only one data point, model as: if x==0, y=-385.12.
    #   But that's suspicious. Could be y = something like -385*exp(-x^2/small)? 
    #   Without more data, treat x=0 as special value.
    #   Actually maybe the function is y = 13x - 3.4 for x>0, 1.324x-9.85 for x<0, and at x=0 there's a discontinuity/spike.
    #   Let's model: x>0: 13.09x-3.4; x<0: 1.324x-9.85; x==0: -385.12.
    #   But what about very small nonzero x? E2 has 0.5 and -0.5 which follow the linear branches. So the spike is only at exactly 0 (or very narrow).
    #   I'll use: if abs(x) < 1e-9: -385.12 else piecewise linear.
    #   Hmm, but maybe the spike is a narrow interval. Without data, keep it as a point.

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
            if abs(x) < 1e-9:
                y = -385.12
            elif x > 0:
                y = 13.09 * x - 3.4
            else:
                y = 1.324 * x - 9.85
            ys.append(y)
        except Exception:
            ys.append(None)
    return {"y": ys}

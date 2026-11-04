def predict(probe):
    # f(x) = -sign(x)*A*|x|^p for |x|>=2, with A and p to be fit [E1,E2,E5,E8,E14,E16]
    #   positive x -> negative y; negative x -> negative y (same sign) [E2,E8]
    #   |f(-x)| > |f(x)| by a roughly constant ratio ~1.15-1.19 [E14,E16]
    # Small |x|<1: y=0 for x>0; for -1<x<0 a positive bump peaking ~6.76 near -0.7 [E2,E4]
    # Transition region 1<=x<2: smooth curve from -4.3 at 1 to -60.2 at 2 [E4,E6]
    #   x=1->-4.3, 1.1->-5.23, ..., 1.9->-25.2, 1.95->-27.56, 1.99->-29.58, 2->-60.2 [E6,E12]
    # Negative transition -2<x<-1: its own curve, NOT mirrored [E12]
    #   -1.05->11.46, -1.1->10.53, -1.2->8.00, -1.3->4.46, -1.4->-0.28, -1.5->-6.43,
    #   -1.6->-14.21, -1.7->-23.88, -1.8->-35.69, -1.9->-49.96, -1.95->-58.11, -1.99->-65.16, -2->-67.0 [E12]
    # Power law: fit from E14/E16 clean points. |f(-x)|/|f(x)| ~ 1.15-1.19, exponent ~5.7-5.8
    import math
    xs = probe.get("x", [])
    ys = []
    ptab_x = [1.0,1.05,1.1,1.15,1.2,1.25,1.3,1.35,1.4,1.45,1.5,1.55,1.6,1.65,1.7,1.75,1.8,1.85,1.9,1.95,1.99,2.0]
    ptab_y = [-4.3,-4.7333,-5.2257,-5.7808,-6.4027,-7.0958,-7.8647,-8.7143,-9.6501,-10.6776,-11.8031,-13.033,-14.3742,-15.8342,-17.4207,-19.1421,-21.0072,-23.0254,-25.2065,-27.561,-29.5769,-60.2]
    ntab_x = [-2.0,-1.99,-1.95,-1.9,-1.8,-1.7,-1.6,-1.5,-1.4,-1.3,-1.2,-1.1,-1.05,-1.0]
    ntab_y = [-67.0,-65.1615,-58.1125,-49.9606,-35.6938,-23.8769,-14.2134,-6.4313,-0.2819,4.4607,8.0016,10.5259,11.4595,6.1]
    def interp(tab_x, tab_y, x):
        if x <= tab_x[0]: return tab_y[0]
        if x >= tab_x[-1]: return tab_y[-1]
        for i in range(len(tab_x)-1):
            if tab_x[i] <= x <= tab_x[i+1]:
                t = (x-tab_x[i])/(tab_x[i+1]-tab_x[i])
                return tab_y[i]*(1-t)+tab_y[i+1]*t
        return tab_y[-1]
    stab_x = [-1.0,-0.9,-0.7,-0.5,-0.3,-0.1,0.0]
    stab_y = [6.1,6.5864,6.7646,6.2406,5.3558,4.3688,0.0]
    # Fit power law from clean large-|x| points [E14,E16]
    # positive: 20->29631878, 40->1963909756, 80->128250953912
    # log-log slope: ln(128250953912/29631878)/ln(80/20) = ln(4328.1)/ln(4) = 8.373/1.386 = 6.04? 
    # Actually let's compute: 128250953912/29631878 = 4328.1; ln=8.373; /ln4=1.386 -> 6.04
    # Hmm 20->40: 1963909756/29631878=66.28; ln=4.194; /ln2=0.693 -> 6.05
    # So exponent ~6.05 for positive! Let's check 40->80: 128250953912/1963909756=65.30; ln=4.179/0.693=6.03
    # So p ~ 6.04 for positive side. A = 29631878/20^6.04
    # 20^6.04 = exp(6.04*ln20)=exp(6.04*2.9957)=exp(18.094)=7.19e7; A=29631878/7.19e7=0.412
    # Check 80: 0.412*80^6.04 = 0.412*exp(6.04*4.382)=0.412*exp(26.47)=0.412*3.13e11=1.29e11 ✓
    # negative: 20->35356522, 40->2147947844, 80->134146940488
    # 40/20: 2147947844/35356522=60.75; ln=4.107/0.693=5.93
    # 80/40: 134146940488/2147947844=62.45; ln=4.135/0.693=5.97
    # p_neg ~ 5.95. A_neg = 35356522/20^5.95 = 35356522/exp(5.95*2.9957)=35356522/exp(17.824)=35356522/5.5e7=0.643
    # Check 80: 0.643*80^5.95=0.643*exp(5.95*4.382)=0.643*exp(26.07)=0.643*2.09e11=1.34e11 ✓
    # Let's refine with more points. Use 3,4,5,6,8,10,15,20,40,80 positive:
    # 3->427.5, 4->2004.4, 5->7119.5, 6->20683.8, 8->115148, 10->442789, 15->5175283.5, 20->29631878, 40->1963909756, 80->128250953912
    # ln(427.5)/ln(3)=6.08/1.099=5.53? Let's compute: ln427.5=6.058, ln3=1.099 -> 5.51
    # Hmm, exponent drifts. 3->4: 2004.4/427.5=4.688; ln=1.545/ln(4/3)=0.288 -> 5.37
    # 4->5: 7119.5/2004.4=3.552; ln=1.267/ln1.25=0.223 -> 5.68
    # 5->6: 20683.8/7119.5=2.905; ln=1.066/ln1.2=0.182 -> 5.86
    # 6->8: 115148/20683.8=5.567; ln=1.717/ln1.333=0.288 -> 5.97
    # 8->10: 442789/115148=3.845; ln=1.347/ln1.25=0.223 -> 6.04
    # 10->15: 5175283.5/442789=11.69; ln=2.459/ln1.5=0.405 -> 6.07
    # 15->20: 29631878/5175283.5=5.726; ln=1.745/ln1.333=0.288 -> 6.06
    # 20->40: 6.05, 40->80: 6.03
    # So exponent approaches ~6.05 for large x, lower for small. This suggests f(x) = -A*x^p + something, or a different form.
    # Actually maybe f(x) = -A*|x|^6 * (something). Or maybe it's -A*|x|^6 + B*|x|^3?
    # Let's try: at x=3, 427.5; x=6, 20683.8. Ratio 48.4. 2^6=64. So less than 6.
    # Try f = -a*x^6 - b*x^3: at 3: 729a+27b=427.5; at 6: 46656a+216b=20683.8
    # 27*(27a+b)=427.5 -> 27a+b=15.833; 216*(216a+b)=20683.8 -> 216a+b=95.76
    # 189a=79.93 -> a=0.4229; b=15.833-11.418=4.415
    # Check x=10: 0.4229*1e6+4.415*1000=422900+4415=427315 vs 442789. Close-ish.
    # Check x=20: 0.4229*64e6+4.415*8000=27065600+35320=27100920 vs 29631878. Off by ~8%.
    # Try f = -a*x^6 - b*x^2: at 3: 729a+9b=427.5; at 6: 46656a+36b=20683.8
    # 9*(81a+b)=427.5 -> 81a+b=47.5; 36*(1296a+b)=20683.8 -> 1296a+b=574.55
    # 1215a=527.05 -> a=0.4338; b=47.5-35.14=12.36
    # x=10: 433800+1236=435036 vs 442789. x=20: 27763200+4944=27768144 vs 29631878. Still off.
    # Hmm. Let's just use a log-log interpolation table for the power law region, it's more reliable.
    # Actually the simplest: use a piecewise power law with exponent varying, or interpolate in log-log space.
    # Build a table of (log x, log|y|) for positive and negative, interpolate, then exponentiate.
    # Positive points from E14,E16 (clean):
    pos_lx = [math.log(3),math.log(4),math.log(5),math.log(6),math.log(8),math.log(10),math.log(15),math.log(20),math.log(30),math.log(40),math.log(50),math.log(60),math.log(70),math.log(80),math.log(90),math.log(100),math.log(128)]
    pos_ly = [math.log(427.5),math.log(2004.4),math.log(7119.5),math.log(20683.8),math.log(115148),math.log(442789),math.log(5175283.5),math.log(29631878),math.log(345196467),math.log(1963909756),math.log(7550888945),math.log(22668795234),math.log(57387033823),math.log(128250953912),math.log(260611048701),math.log(491312155390),math.log(2168936181440)]
    neg_lx = [math.log(3),math.log(4),math.log(5),math.log(6),math.log(8),math.log(10),math.log(15),math.log(20),math.log(30),math.log(40),math.log(50),math.log(60),math.log(70),math.log(80),math.log(90),math.log(100),math.log(128)]
    neg_ly = [math.log(722.7),math.log(3534.8),math.log(12155.5),math.log(33683.4),math.log(171815.2),math.log(618311),math.log(6527191.5),math.log(35356522),math.log(388817433),math.log(2147947844),math.log(8112838555),math.log(24067524366),math.log(60410784077),math.log(134146940488),math.log(271236660399),math.log(509307754610),math.log(2230774482035.2)]
    def interp_log(lx_tab, ly_tab, x):
        lx = math.log(x)
        if lx <= lx_tab[0]:
            # extrapolate with local slope
            slope = (ly_tab[1]-ly_tab[0])/(lx_tab[1]-lx_tab[0])
            return math.exp(ly_tab[0]+slope*(lx-lx_tab[0]))
        if lx >= lx_tab[-1]:
            slope = (ly_tab[-1]-ly_tab[-2])/(lx_tab[-1]-lx_tab[-2])
            return math.exp(ly_tab[-1]+slope*(lx-lx_tab[-1]))
        for i in range(len(lx_tab)-1):
            if lx_tab[i] <= lx <= lx_tab[i+1]:
                t = (lx-lx_tab[i])/(lx_tab[i+1]-lx_tab[i])
                return math.exp(ly_tab[i]*(1-t)+ly_tab[i+1]*t)
        return math.exp(ly_tab[-1])
    for x in xs:
        try:
            ax = abs(x)
            if x >= 2.0:
                y = -interp_log(pos_lx, pos_ly, ax)
            elif x > 0:
                if x < 1.0:
                    y = 0.0
                else:
                    y = interp(ptab_x, ptab_y, x)
            elif x <= -2.0:
                y = -interp_log(neg_lx, neg_ly, ax)
            else:  # -2 < x < 0
                if x > -1.0:
                    y = interp(stab_x, stab_y, x)
                else:
                    y = interp(ntab_x, ntab_y, x)
            ys.append(y)
        except Exception:
            ys.append(None)
    return {"y": ys}

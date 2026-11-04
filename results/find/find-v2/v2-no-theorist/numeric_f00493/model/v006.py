def predict(probe):
    # f(x) for |x|>=3: power law, sign negative both sides [E2,E8,E14,E16]
    #   positive: |f| ~ A*x^6.04; negative: |f| ~ A*x^5.95, ratio ~1.15-1.19 [E14,E16]
    # Jump at |x|=2: inner region ends, outer transition begins [E20,E22]
    #   positive: 1.99->-29.58, 2.0->-60.2 (jump); then smooth 2->3 [E6,E20,E22]
    #   negative: -2.0->-67.0, -2.001->-100.78 (jump); then smooth -2->-3 [E12,E20,E22]
    # Transition 2<|x|<3: lower local exponent (~4-5), NOT the power law [E20,E22]
    #   positive 2.9->-247.7 then jump to 3.0->-427.5 [E22]
    #   negative -2.8->-527.0 then to -3.0->-722.7 [E22]
    # Inner positive 1<=x<2: smooth curve -4.3 at 1 to -29.58 at 1.99 [E6,E12]
    # Inner negative -2<x<-1: own curve, -1.05->11.46 ... -1.99->-65.16, -2.0->-67.0 [E12]
    # Small |x|<1: y=0 for x>0; -1<x<0 positive bump peak ~6.76 near -0.7 [E2,E4]
    import math
    xs = probe.get("x", [])
    ys = []
    # positive inner transition 1..2
    ptab_x = [1.0,1.05,1.1,1.15,1.2,1.25,1.3,1.35,1.4,1.45,1.5,1.55,1.6,1.65,1.7,1.75,1.8,1.85,1.9,1.95,1.99,2.0]
    ptab_y = [-4.3,-4.7333,-5.2257,-5.7808,-6.4027,-7.0958,-7.8647,-8.7143,-9.6501,-10.6776,-11.8031,-13.033,-14.3742,-15.8342,-17.4207,-19.1421,-21.0072,-23.0254,-25.2065,-27.561,-29.5769,-60.2]
    # negative inner transition -2..-1
    ntab_x = [-2.0,-1.99,-1.95,-1.9,-1.8,-1.7,-1.6,-1.5,-1.4,-1.3,-1.2,-1.1,-1.05,-1.0]
    ntab_y = [-67.0,-65.1615,-58.1125,-49.9606,-35.6938,-23.8769,-14.2134,-6.4313,-0.2819,4.4607,8.0016,10.5259,11.4595,6.1]
    # positive outer transition 2..3
    pot_x = [2.0,2.001,2.005,2.01,2.02,2.05,2.1,2.15,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3.0]
    pot_y = [-60.2,-60.3055,-60.729,-61.2619,-62.3396,-65.67,-71.5566,-77.8856,-84.6838,-99.8034,-117.1594,-137.0188,-159.6733,-185.4403,-214.664,-247.7167,-427.5]
    # negative outer transition -3..-2
    not_x = [-3.0,-2.9,-2.8,-2.7,-2.6,-2.5,-2.4,-2.3,-2.2,-2.15,-2.1,-2.05,-2.02,-2.01,-2.005,-2.001,-2.0]
    not_y = [-722.7,-614.0,-527.0222,-445.5106,-373.645,-310.5656,-255.4661,-207.5913,-166.236,-147.7959,-130.7427,-115.0015,-106.1563,-103.3045,-101.8964,-100.7783,-67.0]
    stab_x = [-1.0,-0.9,-0.7,-0.5,-0.3,-0.1,0.0]
    stab_y = [6.1,6.5864,6.7646,6.2406,5.3558,4.3688,0.0]
    def interp(tab_x, tab_y, x):
        if x <= tab_x[0]: return tab_y[0]
        if x >= tab_x[-1]: return tab_y[-1]
        for i in range(len(tab_x)-1):
            if tab_x[i] <= x <= tab_x[i+1]:
                t = (x-tab_x[i])/(tab_x[i+1]-tab_x[i])
                return tab_y[i]*(1-t)+tab_y[i+1]*t
        return tab_y[-1]
    # power law tables for |x|>=3
    pos_lx = [math.log(3),math.log(4),math.log(5),math.log(6),math.log(8),math.log(10),math.log(15),math.log(20),math.log(30),math.log(40),math.log(50),math.log(60),math.log(70),math.log(80),math.log(90),math.log(100),math.log(128)]
    pos_ly = [math.log(427.5),math.log(2004.4),math.log(7119.5),math.log(20683.8),math.log(115148),math.log(442789),math.log(5175283.5),math.log(29631878),math.log(345196467),math.log(1963909756),math.log(7550888945),math.log(22668795234),math.log(57387033823),math.log(128250953912),math.log(260611048701),math.log(491312155390),math.log(2168936181440)]
    neg_lx = [math.log(3),math.log(4),math.log(5),math.log(6),math.log(8),math.log(10),math.log(15),math.log(20),math.log(30),math.log(40),math.log(50),math.log(60),math.log(70),math.log(80),math.log(90),math.log(100),math.log(128)]
    neg_ly = [math.log(722.7),math.log(3534.8),math.log(12155.5),math.log(33683.4),math.log(171815.2),math.log(618311),math.log(6527191.5),math.log(35356522),math.log(388817433),math.log(2147947844),math.log(8112838555),math.log(24067524366),math.log(60410784077),math.log(134146940488),math.log(271236660399),math.log(509307754610),math.log(2230774482035.2)]
    def interp_log(lx_tab, ly_tab, x):
        lx = math.log(x)
        if lx <= lx_tab[0]:
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
            if x >= 3.0:
                y = -interp_log(pos_lx, pos_ly, ax)
            elif x >= 2.0:
                y = interp(pot_x, pot_y, x)
            elif x > 0:
                if x < 1.0:
                    y = 0.0
                else:
                    y = interp(ptab_x, ptab_y, x)
            elif x <= -3.0:
                y = -interp_log(neg_lx, neg_ly, ax)
            elif x <= -2.0:
                y = interp(not_x, not_y, x)
            else:  # -2 < x < 0
                if x > -1.0:
                    y = interp(stab_x, stab_y, x)
                else:
                    y = interp(ntab_x, ntab_y, x)
            ys.append(y)
        except Exception:
            ys.append(None)
    return {"y": ys}

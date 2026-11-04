def predict(probe):
    # Positive side: f(x) = 12.55*x + 0.05 for x > 0 [E6, E7]
    #   E7: 0.25->-1.225? no; check: 12.55*0.25+0.05=3.1875 but observed -1.225.
    #   Actually positive large x: 1->7.6? 12.55*1+0.05=12.6 no.
    #   Recompute slope from E6: (309.9-22.7)/(24-2)=287.2/22=13.05; intercept 22.7-13.05*2=-3.4
    #   E7 large: (413.7-257.5)/(32-20)=156.2/12=13.0167; 257.5-13.0167*20=-2.83
    #   E1: 128->1673.3, 64->832.9: slope (1673.3-832.9)/64=13.131; 832.9-13.131*64=-7.5
    #   Hmm not perfectly linear. Try f(x)=13x + something? 13*128=1664 vs 1673.3.
    #   Let's fit: E7 20->257.5, 32->413.7 slope 13.0167. E6 16->204.1,24->309.9 slope 13.225.
    #   E1 100->1305.5,128->1673.3 slope 13.135. Not constant -> maybe piecewise or slight curvature.
    #   Try f(x)=13x - 3? 13*32-3=413 yes! 13*20-3=257 yes! 13*24-3=309 yes!
    #   13*16-3=205 vs 204.1 close. 13*128-3=1661 vs 1673.3 no.
    #   Try 13.05x? 13.05*128=1670.4 vs 1673.3. 13.1*128=1676.8.
    #   E1: 64->832.9 => 13.014x. 100->1305.5 =>13.055. 128->1673.3=>13.073.
    #   Maybe f(x)=13x + 0.05x? =13.05x: 128->1670.4 vs 1673.3 (off 3).
    #   Perhaps rounding noise. Use 13.05x? Check 32: 417.6 vs 413.7 off 4.
    #   Use 13x-3 for small, but large diverges. Let's just do linear fit 13.05x-3? 32->414.6 ok, 128->1667.4 vs 1673.3.
    #   Given noise, use f(x)=13.05x - 3 for x>0? 0.5->3.525 vs 2.05 no.
    #   Small positive: E7 0.5->2.05, 0.75->4.325, 1->7.6: slope ~11.1, intercept -3.5
    #   0.25->-1.225, 0.5->2.05 slope 13.1; 0.75->4.325 slope 9.1; noisy.
    #   E2: 0.5->1.05, 1->10.6, 1.5->14.15, 2->22.7: slope ~14.4
    #   E6: 0.1->-4.19,0.2->-0.88,0.3->-1.57,0.4->-0.26,0.6->2.36,0.8->4.98: slope ~13
    #   Seems f(x)≈13x-3 with noise for x>0. Use that.
    # Negative side: E1 -8->-16.38, -4->-15.14, -2->-12.52, -1->-11.21
    #   E4: -128->-178.58, -96->-136.66, -48->-71.78, -24->-41.34, -12->-25.62
    #   slope: (-136.66+178.58)/32=1.31; (-71.78+136.66)/48=1.35; (-41.34+71.78)/24=1.27
    #   (-25.62+41.34)/12=1.31. So f(x)≈1.31x - something for x<-4?
    #   -128: 1.31*-128=-167.7 vs -178.58. intercept -10.9
    #   -96: -125.8 vs -136.66 intercept -10.9
    #   -48: -62.9 vs -71.78 intercept -8.9
    #   -24: -31.4 vs -41.34 intercept -9.9
    #   -12: -15.7 vs -25.62 intercept -9.9
    #   So f(x)≈1.31x - 10 for x<-4 roughly. But -8->-16.38: 1.31*-8-10=-20.5 no.
    #   -8->-16.38, -6->-13.76, -5->-16.45, -4->-15.14: noisy around -15
    #   Actually E3: -8->-19.38, -6->-13.76, -5->-16.45, -4.5->-15.795, -4->-15.14
    #   E4: -8->-19.38, -7->-18.07, -6->-18.76, -5->-16.45, -4->-16.14
    #   Noisy. Maybe f(x)=1.31x-10 for x<-8, and something else -8..-1.
    #   -4->-16.14, -3->-14.83, -2->-12.52, -1.5->-11.865, -1->-11.21
    #   slope from -4 to -1: (11.21-16.14)/3=1.64. intercept: -11.21-1.64*1=-12.85? 
    #   -1->-11.21, -2->-12.52: slope 1.31. -3->-14.83 slope 2.31. noisy.
    #   Try f(x)=1.31x - 10 for x<-4, and 1.31x-10 for -4..-1 too? -1->-11.31 vs -11.21 ok!
    #   -2->-12.62 vs -12.52 ok. -3->-13.93 vs -14.83 off. -4->-15.24 vs -16.14 off.
    #   E5 dense: -4->-16.14,-3.75->-12.8125,-3.5->-13.485,-3.25->-15.1575,-3->-11.83
    #   Very noisy! slope ~1.3 with noise ±2.
    #   So negative side: f(x)≈1.31x - 10 for x<0 (except anomaly near 0).
    # Anomaly: x=0 -> -385.12 [E1,E2,E4]. Also -0.1->-11.031, 0.05->-2.845
    #   0.1->-4.19, 0.01->-4.369, 0.02->-2.238, 0.05->-4.845
    #   So near 0 positive small values are negative-ish. Maybe f(x)=13x-3 fails for tiny x.
    #   Actually 0.01: 13*.01-3=-2.87 vs -4.369. 0.02: -2.74 vs -2.238. 0.05: -2.35 vs -4.845.
    #   Noisy. Perhaps there's a spike at 0 only.
    #   -0.1->-11.031: 1.31*-0.1-10=-10.13 ok. -0.25->-10.2275: -10.33 ok.
    #   -0.5->-11.555: -10.66 vs -11.555. -0.75->-11.8825: -10.98. -1->-11.21: -11.31 ok.
    #   So negative side consistent with 1.31x-10 down to -0.1.
    # Positive side: 0.1->-4.19? 13*.1-3=-1.7 no. Hmm.
    #   Maybe positive formula only for x>=0.5? 0.5->2.05: 13*.5-3=3.5 vs 2.05.
    #   E2 0.5->1.05. E7 0.5->2.05. inconsistent (noise).
    #   Let's just use 13x-3 for x>0 and 1.31x-10 for x<0, with 0->-385.12.
    #   But small positive like 0.1 gives -4.19 not -1.7. Maybe there's a dip near 0.
    #   E6: 0.05->-2.845, 0.1->-4.19, 0.2->-0.88, 0.3->-1.57, 0.4->-0.26
    #   E7: 0.01->-4.369, 0.02->-2.238, 0.05->-4.845, 0.1->-3.19, 0.15->-2.535
    #   These are all negative around -2 to -4 for small positive x. Then 0.25->-1.225, 0.5->2.05.
    #   So maybe for 0<x<0.25, f(x)≈-3 (roughly constant negative). Then rises.
    #   Actually 0.25->-1.225 (E7), 0.25->-2.225 (E2). Noisy around -2.
    #   Let's model: x>0: f(x)=13x-3 but for x<0.3 clamp? 
    #   Simpler: f(x)=13x-3 for x>=0.3; for 0<x<0.3 use ~-3 (noisy). 
    #   But 0.2->-0.88, 0.3->-1.57. Hmm.
    #   I'll use: x>0: 13x-3 (best fit overall), x<0: 1.31x-10, x==0: -385.12.
    #   Add noise? No, deterministic best guess.
    out = []
    for x in probe["x"]:
        try:
            if x == 0:
                out.append(-385.12)
            elif x > 0:
                out.append(13.0*x - 3.0)
            else:
                out.append(1.31*x - 10.0)
        except Exception:
            out.append(None)
    return {"y": out}

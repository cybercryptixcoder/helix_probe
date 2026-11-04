import math

def predict(probe):
    """
    Model of the black box f(x).
    
    Beliefs (each line cites evidence):
    # For x >= 0: f(x) grows roughly quadratically, f(x) ~ x^2/1.1 + small linear [E1,E2,E3]
    #   e.g. f(88.2)=9934 ~ 88.2^2/0.783? Let's check: 88.2^2=7779; 9934/7779=1.277 -> f ~ 1.277*x^2? 
    #   Actually f(104.9)=11795, 104.9^2=11004 -> ratio 1.072. f(123.6)=13879, 123.6^2=15277 -> 0.908.
    #   So not pure quadratic; it's a smooth MLP approximation of something like x^2/1.1 + 0.5*x? Let's fit.
    # For x < 0: f(x) is much smaller and roughly linear-ish/quadratic with a different scale, 
    #   and near x=0 it dips: f(-1.6)=16, f(-5.9)=128, f(2.0)=329, f(2.9)=429 [E5,E4,E6,E1]
    # There's a kink/region near 0: negative side much flatter, positive side steeper.
    # f(-127.7)=3304, f(-124.4)=3218, f(-107.4)=2775, f(-102.2)=2639: negative side ~ quadratic with coeff ~0.2
    #   check: 127.7^2=16307 *0.2=3261 ~ 3304. 107.4^2=11535*0.24=2768. Good ~0.2*x^2.
    # Positive side: f(119.5)=13422, 119.5^2=14280 -> 0.94. f(94.1)=10591, 94.1^2=8855 -> 1.196.
    #   Hmm ratio varies. Try f(x)=x^2/1.1 + 0.6*x? at 119.5: 12982+72=13054 (close to 13422).
    #   at 94.1: 8050+56=8106 (actual 10591) - no.
    # Let's fit positive side as a*x^2 + b*x + c using points.
    #   (88.2,9934),(66.0,7460),(72.7,8207),(104.5,11750),(123.6,13879),(119.5,13422),(94.1,10591)
    # Try a=0.9,b=0.5: 88.2-> 7000+44=7044 no.
    # Try pure x^2 * k + c: 88.2^2=7780 -> 9934/7780=1.277; 66^2=4356->7460/4356=1.713; not constant.
    # Try a*x^2+b*x: solve 88.2: 7780a+88.2b=9934; 123.6: 15277a+123.6b=13879.
    #   From first: b=(9934-7780a)/88.2. Sub: 15277a + 123.6*(9934-7780a)/88.2 = 13879
    #   15277a + 1.4014*(9934-7780a)=13879 -> 15277a +13922 -10903a =13879 -> 4374a=-43 -> a=-0.01. Bad.
    # Likely MLP approximating something like f(x)=x^2/1.2 + 0.4*x for x>0 plus a small wiggle.
    # Let's just use a piecewise smooth interpolation: positive side approximately 0.95*x^2/... 
    # Better: fit f(x)=c1*x^2 + c2*x + c3 on positive points by least squares mentally.
    # Use 66->7460, 94.1->10591, 123.6->13879.
    # 4356c1+66c2+c3=7460
    # 8855c1+94.1c2+c3=10591
    # 15277c1+123.6c2+c3=13879
    # Subtract: 4499c1+28.1c2=3131 ; 6422c1+29.5c2=3288
    # From first: c2=(3131-4499c1)/28.1=111.4-160.1c1
    # Sub: 6422c1+29.5*(111.4-160.1c1)=3288 -> 6422c1+3286-4723c1=3288 -> 1699c1=2 -> c1=0.0012. Bad.
    # So not quadratic. Maybe it's x^2/1.5 + 0.5*x + small? Let's try log or exp?
    # f(66)=7460, f(88.2)=9934, f(104.5)=11750, f(123.6)=13879. Differences: 
    #   slope 66->88.2: 2474/22.2=111.4; 88.2->104.5: 1816/16.3=111.4; 104.5->123.6: 2129/19.1=111.5
    # Wow! Linear on positive side with slope ~111.4! Check intercept: 7460-111.4*66=7460-7352=108.
    # f(94.1)=10591: 111.4*94.1+108=10483+108=10591. EXACT!
    # f(119.5)=13422: 111.4*119.5+108=13312+108=13420. YES!
    # f(72.7)=8207: 111.4*72.7+108=8099+108=8207. YES!
    # So positive side: f(x) = 111.4*x + 108 (approx). Actually let's refine: slope from 66 to 123.6: (13879-7460)/57.6=6419/57.6=111.44. intercept 7460-111.44*66=7460-7355=105.
    # Check 88.2: 111.44*88.2+105=9830+105=9935 (actual 9934). 
    # So f(x) ~ 111.44*x + 105 for x>0. But f(2.9)=429: 111.44*2.9+105=323+105=428. YES!
    # f(1.2)=240: 111.44*1.2+105=134+105=239. YES!
    # f(2.0)=329: 111.44*2+105=223+105=328. YES!
    # f(12.5)=1499: 111.44*12.5+105=1393+105=1498. YES!
    # So positive side is LINEAR: f(x) = 111.44*x + 105 for x >= 0 (approx).
    # Now negative side: f(-1.6)=16.3, f(-5.9)=128.4, f(-7.1)=159.7, f(-13.3)=321.3, f(-16.9)=415.2
    #   slope: (-1.6,16.3) to (-16.9,415.2): (415.2-16.3)/(-15.3)= -26.07? No, 398.9/-15.3=-26? 
    #   Wait x decreases, y increases. slope = (415.2-16.3)/(-16.9-(-1.6))=398.9/-15.3=-26.07. So y = -26.07*x + b. 
    #   b = 16.3+26.07*1.6=16.3+41.7=58. Check -5.9: -26.07*(-5.9)+58=153.8+58=211.8 (actual 128.4) - no.
    # Try quadratic: f(-5.9)=128.4, f(-16.9)=415.2, f(-24.3)=608.1, f(-50.4)=1288.6, f(-61.7)=1583.2, f(-102.2)=2639.1, f(-127.7)=3303.9
    #   Check x^2 coeff: 5.9^2=34.8 ->128/34.8=3.69; 16.9^2=285.6->415/285.6=1.45; 24.3^2=590.5->608/590.5=1.03
    #   Not pure quadratic. Try linear: slope from -61.7 to -127.7: (3303.9-1583.2)/(-66)=1720.7/-66=-26.07. 
    #   Ah same slope -26.07! So for large negative, linear slope -26.07.
    #   Check -102.2: -26.07*(-102.2)+b. From -61.7: 1583.2=-26.07*(-61.7)+b -> b=1583.2-1608.5=-25.3.
    #   Check -102.2: 2664.4-25.3=2639.1. YES! -127.7: 3329.1-25.3=3303.8. YES!
    #   Check -50.4: 1313.9-25.3=1288.6. YES! -24.3: 633.5-25.3=608.2. YES!
    #   Check -16.9: 440.6-25.3=415.3. YES! -13.3: 346.7-25.3=321.4. YES!
    #   Check -7.1: 185.1-25.3=159.8. YES! -6.0: 156.4-25.3=131.1 (actual 131.0). YES!
    #   Check -5.9: 153.8-25.3=128.5. YES! -1.6: 41.7-25.3=16.4 (actual 16.3). YES!
    # So negative side is LINEAR too: f(x) = -26.07*x - 25.3 for x < 0 (approx).
    # Wait but f(2.9)=429 with positive formula 111.44*2.9+105=428. OK.
    # What about x=0? Positive formula gives 105, negative formula gives -25.3. Discontinuity at 0!
    # Which applies at 0? Probe values near 0: f(-1.6)=16.3 (neg formula: 41.7-25.3=16.4 ✓). f(1.2)=239.8 (pos: 133.7+105=238.7 ✓).
    # So there's a jump at x=0. The box likely: if x>=0 use 111.44x+105, else -26.07x-25.3.
    # But wait, is it really linear? Let's double-check a few more.
    # f(-44.7)=1139.96: -26.07*(-44.7)-25.3=1165.3-25.3=1140.0. YES.
    # f(-65.6)=1684.86: 1710.2-25.3=1684.9. YES.
    # f(-66.9)=1718.75: 1744.1-25.3=1718.8. YES.
    # f(-79.1)=2036.83: 2062.1-25.3=2036.8. YES.
    # f(-100.1)=2584.33: 2609.6-25.3=2584.3. YES.
    # f(-107.4)=2774.65: 2800.0-25.3=2774.7. YES.
    # f(-124.4)=3217.87: 3243.1-25.3=3217.8. YES.
    # f(-127.7)=3303.91: 3329.1-25.3=3303.8. YES.
    # Positive: f(21.3)=2479.47: 111.44*21.3+105=2373.7+105=2478.7 (actual 2479.5). Close.
    # f(28.4)=3270.6: 3164.9+105=3269.9. YES.
    # f(30.3)=3482.3: 3376.6+105=3481.6. YES.
    # f(43.0)=4897.4: 4791.9+105=4896.9. YES.
    # f(47.1)=5354.3: 5248.8+105=5353.8. YES.
    # f(52.9)=6000.6: 5895.2+105=6000.2. YES.
    # f(56.2)=6368.3: 6262.9+105=6367.9. YES.
    # f(58.8)=6658.0: 6552.7+105=6657.7. YES.
    # f(65.5)=7404.6: 7299.3+105=7404.3. YES.
    # f(77.6)=8752.9: 8647.7+105=8752.7. YES.
    # f(78.1)=8808.6: 8703.5+105=8808.5. YES.
    # f(79.4)=8953.4: 8848.3+105=8953.3. YES.
    # f(83.2)=9376.8: 9271.8+105=9376.8. YES.
    # f(93.5)=10524.6: 10419.6+105=10524.6. YES.
    # f(94.8)=10669.4: 10564.5+105=10669.5. YES.
    # f(102.1)=11482.8: 11377.9+105=11482.9. YES.
    # f(103.0)=11583.1: 11478.3+105=11583.3. YES.
    # f(104.5)=11750.3: 11645.5+105=11750.5. YES.
    # f(104.9)=11794.8: 11690.1+105=11795.1. YES.
    # f(105.7)=11884.0: 11779.2+105=11884.2. YES.
    # f(110.8)=12452.3: 12347.6+105=12452.6. YES.
    # f(119.7)=13444.0: 13339.4+105=13444.4. YES.
    # f(123.6)=13878.5: 13774.0+105=13879.0. YES.
    # Excellent. So the model is piecewise linear with a jump at 0.
    # Refine constants: positive slope ~111.44, intercept ~105. Negative slope ~-26.07, intercept ~-25.3.
    # Let's refine using endpoints: pos: (1.2,239.7661),(123.6,13878.5306): slope=(13878.5306-239.7661)/122.4=13638.76/122.4=111.4284. intercept=239.7661-111.4284*1.2=239.7661-133.714=106.052.
    # Check 88.2: 111.4284*88.2+106.052=9827.98+106.05=9934.03 (actual 9933.986). 
    # Check 123.6: 111.4284*123.6+106.052=13772.55+106.05=13878.6 (actual 13878.53). Good.
    # Neg: (-1.6,16.2696),(-127.7,3303.9102): slope=(3303.9102-16.2696)/(-126.1)=3287.64/-126.1=-26.0717. intercept=16.2696-(-26.0717)*(-1.6)=16.2696-41.7147=-25.4451.
    # Check -127.7: -26.0717*(-127.7)-25.4451=3329.36-25.45=3303.91. YES.
    # Check -61.7: 1608.62-25.45=1583.18 (actual 1583.1784). YES.
    # So final: f(x) = 111.4284*x + 106.05 if x>=0 else -26.0717*x - 25.445.
    # What about x exactly 0? No evidence. Likely the MLP has a smooth-ish transition but the linear fits suggest a sharp piecewise. 
    # Since it's an MLP approximating a piecewise linear function, maybe it's actually continuous? But the fits are exact to 4 decimals with a jump.
    # At x=0: pos gives 106.05, neg gives -25.45. Big jump. MLP can approximate a jump with steep sigmoid. 
    # But maybe there's a small interval around 0 where it transitions? Evidence: f(-1.6)=16.27 (neg formula exact), f(1.2)=239.77 (pos formula exact). 
    # f(2.0)=328.9 (pos: 222.86+106.05=328.91 ✓). f(-5.9)=128.38 (neg: 153.82-25.45=128.37 ✓).
    # So the jump is between -1.6 and 1.2, likely at 0. Use x>=0 -> positive.
    # Mark uncertainty: exact jump location could be slightly off 0; assume 0.
    """
    try:
        xs = probe["x"]
        ys = []
        for x in xs:
            if x is None:
                ys.append(None)
                continue
            x = float(x)
            if x >= 0:
                y = 111.4284 * x + 106.052
            else:
                y = -26.0717 * x - 25.4451
            ys.append(round(y, 4))
        return {"y": ys}
    except Exception:
        return {"y": [None] * len(probe.get("x", []))}

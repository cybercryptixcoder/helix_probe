import math

def predict(probe):
    # A: for x in [-20.3, ~4.5] the output is a flat floor -20.4469 [E1, E2]
    # B: for x < ~-20.3 the output is a quadratic 2.0487x^2+44.64x+41.26 [E1]
    # C: for x in [~4.5, ~30] the output is linear 126.1155x-610.674 [E2]
    # D: for x > ~30 the output is quadratic 2.6174x^2-2.55x+1717.7 [E1]
    # E: E3 shows the large-x quadratic is too steep: at 104.5 obs 28878.7 vs pred 30033.9,
    #    at 123.6 obs 37109.9 vs pred 41388.4. Refit quadratic through E3 large positives:
    #    (65.5,12779.9647),(79.4,18061.8252),(104.5,28878.7371),(123.6,37109.9331)
    #    Fit a*x^2+b*x+c using (65.5),(104.5),(123.6):
    #    4290.25a+65.5b+c=12779.9647
    #    10920.25a+104.5b+c=28878.7371
    #    15276.96a+123.6b+c=37109.9331
    #    Eq2-Eq1: 6630a+39b=16098.7724
    #    Eq3-Eq2: 4356.71a+19.1b=8231.196
    #    From first: b=(16098.7724-6630a)/39=412.789-170.0a
    #    Sub: 4356.71a+19.1*(412.789-170.0a)=8231.196
    #    4356.71a+7884.27-3247a=8231.196 -> 1109.71a=346.926 -> a=0.3126
    #    b=412.789-170.0*0.3126=412.789-53.14=359.65
    #    c=12779.9647-4290.25*0.3126-65.5*359.65=12779.96-1341.13-23557.1=-12118.3
    #    Check 79.4: 0.3126*6304.36+359.65*79.4-12118.3=1970.7+28556.2-12118.3=18408.6 (obs 18061.8, off ~350)
    #    Hmm not great. Try including more points / least squares feel.
    #    Actually E1 gave 2.6174x^2-2.55x+1717.7 fitting (66,72.7,88.2) well.
    #    E3 at 65.5 obs 12779.96 matches E1 quad: 2.6174*4290.25-2.55*65.5+1717.7=11229.5-167+1717.7=12780.2 ✓
    #    So the quadratic IS 2.6174x^2-2.55x+1717.7 at 65.5. But at 104.5 it overshoots.
    #    So the large-x branch is NOT a pure quadratic — it bends down at high x.
    #    Compare obs vs quad 2.6174x^2-2.55x+1717.7:
    #      104.5: quad=28578.6? compute: 2.6174*10920.25=28582.6; -266.5+1717.7 -> 30033.8 (obs 28878.7)
    #      123.6: 2.6174*15276.96=39985.9; -315.2+1717.7=41388.4 (obs 37109.9)
    #      79.4: 2.6174*6304.36=16501.0; -202.5+1717.7=18016.2 (obs 18061.8) ✓ close
    #      103.0: 2.6174*10609=27767.0; -262.7+1717.7=29222.0 (obs 28232.3)
    #    So deviation grows with x beyond ~80. Looks like a cubic term or a different curve.
    #    Fit cubic through (65.5,12779.96),(79.4,18061.83),(104.5,28878.74),(123.6,37109.93):
    #    Let's fit a*x^2+b*x+c plus d*x^3. Use four points.
    #    Actually try: maybe it's quadratic in a different variable, or the linear region
    #    extends further and quadratic starts later. At 65.5 quad matches, so quad region.
    #    Let's fit cubic: y = A x^3 + B x^2 + C x + D. Four points -> solve.
    #    Use differences approach. Points x: 65.5,79.4,104.5,123.6
    #    This is getting complex; do a quick least-squares-ish fit mentally is hard.
    #    Alternative: the curve may be quadratic but with smaller leading coeff at large x,
    #    i.e. piecewise. But E1 points (66,72.7,88.2) fit a=2.6174 tightly.
    #    Check 88.2 with a=2.6174: 2.6174*7779.24=20361.4; -224.9+1717.7=21854.2 ✓ exact.
    #    So up to 88.2 the quad 2.6174 is exact. Beyond ~100 it deviates.
    #    So there's ANOTHER switch around x~90-100 to a gentler curve.
    #    Fit quadratic through (104.5,28878.74),(104.9,29051.12),(123.6,37109.93):
    #    These are close in x for first two. Slope between 104.5 and 104.9: (29051.12-28878.74)/0.4=431.0
    #    Slope between 104.9 and 123.6: (37109.93-29051.12)/18.7=430.9
    #    Nearly identical slopes! So it's LINEAR at high x with slope ~431.
    #    Line through (104.5,28878.74): intercept=28878.74-431.0*104.5=28878.74-45039.5=-16160.8
    #    Check 123.6: 431.0*123.6-16160.8=53271.6-16160.8=37110.8 (obs 37109.9) ✓
    #    Check 103.0: 431.0*103-16160.8=44393-16160.8=28232.2 (obs 28232.3) ✓✓
    #    Check 79.4: 431*79.4-16160.8=34221.4-16160.8=18060.6 (obs 18061.8) ✓ close!
    #    Check 65.5: 431*65.5-16160.8=28230.5-16160.8=12069.7 (obs 12779.96) off ~710
    #    Hmm at 65.5 linear gives 12070 vs obs 12780. Quad gives 12780. So switch between 65.5 and 79.4.
    #    At 79.4: linear 18060.6, quad 18016.2, obs 18061.8 -> linear wins.
    #    So switch is between 65.5 and 79.4. Where linear=quad?
    #    431x-16160.8 = 2.6174x^2-2.55x+1717.7
    #    2.6174x^2-433.55x+17878.5=0
    #    disc=433.55^2-4*2.6174*17878.5=187965-187190=775 -> sqrt=27.8
    #    x=(433.55±27.8)/5.2348 -> x=88.2 or x=77.5
    #    So they cross at 77.5 and 88.2. Between them quad>linear? At 79.4 quad=18016, linear=18061 -> linear>quad.
    #    At 88.2 quad=21854, linear=431*88.2-16160.8=38014-16160.8=21853.4 -> equal!
    #    Interesting: at 88.2 both give ~21854. So the switch is at x≈88.2 where they meet.
    #    For x<88.2 quad is used (matches E1 at 66,72.7,88.2), for x>88.2 linear slope 431.
    #    Wait but at 79.4 quad=18016 vs obs 18061.8 — obs is 45 higher. Linear=18060.6 matches better.
    #    Hmm. At 79.4 linear matches obs better than quad. But at 72.7 quad matches E1 exactly.
    #    Let me recheck quad at 79.4: 2.6174*6304.36=16501.0; -2.55*79.4=-202.5; +1717.7 -> 18016.2.
    #    Obs 18061.8. Diff 45.6. Linear 18060.6 diff 1.2. So linear better at 79.4.
    #    But E1 at 72.7: quad=2.6174*5285.29-185.4+1717.7=13833.7-185.4+1717.7=15366.0 ✓ exact.
    #    Linear at 72.7: 431*72.7-16160.8=31333.7-16160.8=15172.9. Obs 15366.1. Quad wins.
    #    So switch between 72.7 and 79.4. Where linear=quad? roots 77.5 and 88.2.
    #    At 77.5 they're equal. For x<77.5 quad>linear? At 72.7 quad=15366, linear=15173, quad>linear ✓
    #    For 77.5<x<88.2 linear>quad? At 79.4 linear=18061>quad=18016 ✓. At 88.2 equal again.
    #    For x>88.2 quad>linear again? At 104.5 quad=30034>linear=28879. But obs=28879=linear!
    #    So obs follows linear for x>77.5, even though quad is higher. So switch at ~77.5.
    #    At 88.2 obs=21854.2. Linear at 88.2=21853.4 ✓. Quad at 88.2=21854.2 ✓. Both match!
    #    So switch point ~77.5, and at 88.2 they coincide so can't distinguish.
    #    Conclusion: quad for x in [~30, 77.5], linear slope 431 for x>77.5.
    #    But wait — is the high-x linear the SAME as the mid linear (slope 126)? No, slope 431.
    #    So there are two linear regions? Or the mid "linear" is actually part of something.
    #    Let me reconsider. Maybe the whole thing is: floor, then a curve, then linear.
    #    Actually simplest consistent story:
    #      x < -20.3: neg quad
    #      -20.3 <= x <= 4.5: floor
    #      4.5 < x <= 77.5: quad 2.6174x^2-2.55x+1717.7  (but E2 showed LINEAR on [6,18]!)
    #    E2 [6,18] was perfectly linear slope 126. Quad 2.6174 would give curvature. Check:
    #    quad at 6: 2.6174*36-15.3+1717.7=94.2-15.3+1717.7=1796.6. Obs 146.0. NOT quad!
    #    So [6,18] is linear slope 126, NOT the quad. So quad only kicks in later.
    #    So: floor -> linear(126) -> quad(2.6174) -> linear(431).
    #    Where does linear(126) meet quad(2.6174)? Earlier computed no real intersection (disc<0).
    #    So there's a jump/discontinuity, OR the linear region ends and quad begins at a boundary.
    #    At x=18 linear=1659.4. At x=30.3 obs=3514.4. Linear(126) at 30.3=126.1155*30.3-610.674=3821.3-610.7=3210.6. Obs 3514.4. Quad at 30.3=2.6174*918.09-77.3+1717.7=2403.0-77.3+1717.7=4043.4. Obs 3514.4 between them.
    #    Hmm. At 30.3 obs 3514.4, linear 3210.6, quad 4043.4. Neither matches!
    #    So there's a transition region. Let me fit through (18,1659.4),(30.3,3514.4),(65.5,12780.0):
    #    Maybe a single quadratic through these? 
    #    324a+18b+c=1659.4
    #    918.09a+30.3b+c=3514.4
    #    4290.25a+65.5b+c=12780.0
    #    Eq2-Eq1: 594.09a+12.3b=1855.0
    #    Eq3-Eq2: 3372.16a+35.2b=9265.6
    #    From first: b=(1855.0-594.09a)/12.3=150.81-48.3a
    #    Sub: 3372.16a+35.2*(150.81-48.3a)=9265.6
    #    3372.16a+5308.5-1700.2a=9265.6 -> 1671.96a=3957.1 -> a=2.3667
    #    b=150.81-48.3*2.3667=150.81-114.31=36.5
    #    c=1659.4-324*2.3667-18*36.5=1659.4-766.8-657=-... 1659.4-766.8-657=235.6
    #    Check 65.5: 2.3667*4290.25+36.5*65.5+235.6=10153.8+2390.8+235.6=12780.2 ✓
    #    Check 30.3: 2.3667*918.09+36.5*30.3+235.6=2172.8+1106.0+235.6=3514.4 ✓✓
    #    Check 18: 2.3667*324+36.5*18+235.6=766.8+657+235.6=1659.4 ✓
    #    So a SINGLE quadratic 2.3667x^2+36.5x+235.6 fits (18,30.3,65.5)!
    #    But E2 [6,18] was linear slope 126... check this quad at 6: 2.3667*36+36.5*6+235.6=85.2+219+235.6=539.8. Obs 146. No.
    #    At 12: 2.3667*144+36.5*12+235.6=340.8+438+235.6=1014.4. Obs 902.7. No.
    #    So [6,18] linear doesn't fit this quad. But (18,30.3,65.5) fit quad well.
    #    Contradiction at 18: linear gives 1659.4, quad gives 1659.4 — they agree at 18!
    #    Check quad at 18 = 1659.4 ✓ (by construction). Linear at 18=1659.4 ✓.
    #    At 15: linear=126.1155*15-610.674=1891.7-610.7=1281.1. Obs 1281.06 ✓.
    #    Quad at 15: 2.3667*225+36.5*15+235.6=532.5+547.5+235.6=1315.6. Obs 1281.1. Quad off by 34.
    #    So near 15 linear is better, near 30.3 quad is better. They cross around 18.
    #    So switch from linear(126) to quad(2.3667) at x≈18!
    #    Check: linear=quad: 126.1155x-610.674=2.3667x^2+36.5x+235.6
    #    2.3667x^2-89.6155x+846.274=0
    #    disc=8031.0-4*2.3667*846.274=8031.0-8010.9=20.1 -> sqrt=4.48
    #    x=(89.6155±4.48)/4.7334 -> x=19.87 or x=17.98
    #    So they cross at ~18 and ~19.9. Between them quad<linear? At 19: linear=1785.5, quad=2.3667*361+36.5*19+235.6=854.4+693.5+235.6=1783.5. Close.
    #    So switch at x≈18-20. Use 19.
    #    Now where does quad(2.3667) meet quad(2.6174)? They're both quadratics.
    #    2.3667x^2+36.5x+235.6 = 2.6174x^2-2.55x+1717.7
    #    -0.2507x^2+39.05x-1482.1=0 -> 0.2507x^2-39.05x+1482.1=0
    #    disc=1524.9-4*0.2507*1482.1=1524.9-1486.3=38.6 -> sqrt=6.2
    #    x=(39.05±6.2)/0.5014 -> x=90.3 or x=65.5
    #    So they cross at 65.5 and 90.3. At 65.5 both give 12780 ✓ (that's why it fit).
    #    For x between 65.5 and 90.3, which is used? At 72.7 obs 15366. 
    #    quad2.3667 at 72.7: 2.3667*5285.29+36.5*72.7+235.6=12508.8+2653.6+235.6=15398.0. Obs 15366.1. Off 32.
    #    quad2.6174 at 72.7: 15366.0 ✓ exact.
    #    So for x>65.5, quad2.6174 is used. For x<65.5, quad2.3667.
    #    So switch at 65.5.
    #    Then quad2.6174 vs linear431: cross at 77.5 and 88.2 (computed earlier).
    #    At 79.4 obs 18061.8: quad2.6174=18016.2, linear431=18060.6. Linear wins.
    #    At 72.7 obs 15366.1: quad2.6174=15366.0 ✓, linear431=15172.9. Quad wins.
    #    So switch between 72.7 and 79.4, at ~77.5.
    #    For x>77.5 use linear431.
    #    Check 88.2: linear431=21853.4, obs 21854.2 ✓ (quad also 21854.2, coincide).
    #    Check 104.5: linear431=28878.7 ✓ obs 28878.7.
    #    Check 123.6: linear431=37110.8 vs obs 37109.9 ✓.
    #    Great. So positive side:
    #      floor up to ~4.5
    #      linear126 from 4.5 to ~19
    #      quad2.3667 from 19 to 65.5
    #      quad2.6174 from 65.5 to 77.5
    #      linear431 from 77.5 up
    #    That's a lot of pieces. Let me double check the floor->linear126 boundary.
    #    Floor=-20.4469, linear126: 126.1155x-610.674=-20.4469 -> x=4.680.
    #    At x=3 obs -20.4469 (floor). At x=6 obs 146.0 (linear). So boundary in (3,6), 4.68 plausible.
    #    Negative side: neg quad 2.0487x^2+44.64x+41.26 for x<-20.3.
    #    Check E3: -55.8 obs 3927.93. Neg quad: 2.0487*3113.64+44.64*(-55.8)+41.26=6378.9-2490.9+41.3=3929.3 ✓
    #    -63.9 obs 5554.33. Neg quad: 2.0487*4083.21+44.64*(-63.9)+41.26=8365.3-2852.5+41.3=5554.1 ✓
    #    Good, neg quad holds.
    #    Floor boundary negative: neg quad=-20.4469 at x=-20.31 (computed). At -20.3 obs -15.87 (above floor).
    #    Hmm -20.3 obs -15.87 but neg quad gives -20.68 and floor is -20.45. Neither matches -15.87.
    #    That's a transition artifact. Use -20.3 as boundary, accept error there.
    x = probe.get("x", [])
    ys = []
    FLOOR = -20.4469
    for v in x:
        if v is None:
            ys.append(None)
            continue
        try:
            v = float(v)
        except Exception:
            ys.append(None)
            continue
        if v < -20.3:
            y = 2.0487*v*v + 44.64*v + 41.26
        elif v <= 4.68:
            y = FLOOR
        elif v <= 19.0:
            y = 126.1155*v - 610.674
        elif v <= 65.5:
            y = 2.3667*v*v + 36.5*v + 235.6
        elif v <= 77.5:
            y = 2.6174*v*v - 2.55*v + 1717.7
        else:
            y = 431.0*v - 16160.8
        ys.append(y)
    return {"y": ys}

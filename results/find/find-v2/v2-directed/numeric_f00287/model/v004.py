import math

def predict(probe):
    # Left linear: y = -0.7*x for x <= -11.2 [E1,E2,E4]
    #   E4: -11.5,-11.2,-11.1 all -> 8.4 (flat!). -0.7*-11.5=8.05, -0.7*-11.2=7.84.
    #   So 8.4 is a plateau, not the line. -0.7x=8.4 at x=-12. So line ends at -12.
    #   E2: -12->8.4=-0.7*-12, -13->9.1, -14->9.8, -15->10.5. Line holds to -12.
    #   E4: -11.5..-11.1 -> 8.4 flat. So plateau 8.4 for x in [-12,-11]? 
    #   E2: -11->7.7, -10.5->7.7. E4: -10.05..-10.01->7.7, -9.99->7.0.
    #   So 7.7 plateau spans roughly [-11,-10], 8.4 plateau spans [-12,-11.1].
    #   Hmm two plateaus? Maybe rounding: values are rounded to 1 decimal? 
    #   -0.7*-11.5=8.05 -> 8.4? No. But observed 8.4 exactly.
    #   Actually maybe the function rounds x to nearest integer then -0.7*x? 
    #   round(-11.5)=-12 -> 8.4. round(-11.2)=-11 -> 7.7. But observed 8.4 for -11.2. No.
    #   Maybe floor? floor(-11.5)=-12->8.4, floor(-11.2)=-12->8.4, floor(-11.1)=-12->8.4. Yes!
    #   floor(-10.05)=-11->7.7, floor(-10.01)=-11->7.7, floor(-9.99)=-10->7.0. Yes!
    #   floor(-10.5)=-11->7.7, floor(-11)=-11->7.7, floor(-12)=-12->8.4. Yes!
    #   So left region: y = -0.7*floor(x) for x <= -6? Check -6.5: floor=-7 -> 4.9. Observed 4.9! 
    #   -6.2: floor=-7->4.9 observed 4.9. -6.1: floor=-7->4.9 observed 4.9. 
    #   -5.9: floor=-6->4.2 observed 4.2. -5.5: floor=-6->4.2 observed 4.2. 
    #   So left linear uses floor(x): y=-0.7*floor(x), valid until it hits constant.
    #   E1: -5->-402.3. floor(-5)=-5 -> 3.5, but observed -402.3. So boundary at -5.
    #   E4: -5.9,-5.5 -> 4.2 (still linear). E1: -5 -> constant. So boundary between -5.5 and -5.
    #   floor: -5.5->-6->4.2 linear; -5->-5->3.5 but constant. So x < -5 linear, x >= -5 constant.
    #   Wait but -5.9 floor=-6 -> 4.2 yes. -5.5 floor=-6 -> 4.2 yes. -5 floor=-5 -> 3.5 but observed constant.
    #   So threshold: x < -5 uses -0.7*floor(x); x >= -5 constant? But -5.5<-5 yes linear.
    #   Hmm what about -5.0 exactly? E1 -5 -> -402.3 constant. So x < -5 linear, x >= -5 constant.
    #   But wait, does floor apply or is it just that values happen to be integers? 
    #   E4 non-integers confirm floor. Good.
    # Constant middle: y ~ -402.3 for -5 <= x < 19 [E1,E2,E3,E4]
    #   E4: 18.6..18.95 -> -302.4 (not -402.3!). So right boundary is lower.
    #   -302.4: what's -302.4? -16.8*18 = -302.4. So 18.6..18.95 -> -16.8*18.
    #   floor(18.6)=18 -> -16.8*18=-302.4. Yes! Right linear uses floor too.
    #   E3: 16.5..18.5 -> -402.3 constant. E4: 18.6 -> -302.4. So boundary between 18.5 and 18.6.
    #   floor(18.5)=18 -> -302.4, but observed -402.3. So constant up to 18.5.
    #   floor(18.6)=18 -> -302.4 observed. So boundary at 18.5 < x.
    #   Hmm inconsistent with floor. Maybe threshold is x >= 18.5? But 18.5 gives -402.3.
    #   Let's say constant for x <= 18.5, right linear for x > 18.5.
    #   E3: 19->-319.2, 19.5->-319.2. -16.8*floor(19)=-319.2 yes. floor(19.5)=19 -> -319.2 yes.
    #   E4: 19.02,19.05,19.1 -> -319.2. floor=19 -> -319.2 yes.
    #   E1: 20->-336=-16.8*20. floor(20)=20 yes.
    #   So right linear: y = -16.8*floor(x) for x > 18.5.
    #   Check E1 40->-672=-16.8*40 yes. 60->-1008 yes. Good.
    #   But wait E1 20->-336, floor(20)=20 -> -336 yes.
    #   What about x=18.6: floor=18 -> -302.4 observed. Good.
    #   So right linear starts at x > 18.5, uses floor.
    #   Actually let's check: is it x > 18.5 or x >= 18.6? 18.5 constant, 18.6 linear.
    #   I'll use x > 18.5.
    # Left linear boundary: x < -5 uses -0.7*floor(x). Check -5.5 floor=-6 -> 4.2 yes.
    #   What about -5.0? constant. So x < -5 linear.
    #   But floor(-5.5)=-6, floor(-5.0)=-5. If threshold were on floor value, floor=-5 constant.
    #   Consistent: floor(x) <= -5 -> constant? floor(-5.5)=-6 linear, floor(-5)=-5 constant.
    #   So: if floor(x) <= -5 (i.e. x < -4? no). Let's just use x < -5 for linear.
    #   Hmm -4.5: floor=-5 -> would be constant under floor rule. But x<-5 says -4.5 is constant too (since -4.5 > -5). OK.
    #   Actually -4.5 > -5 so constant. Fine.
    #   But what about -5.0 exactly: x < -5 false -> constant. Good.
    out = []
    for x in probe.get("x", []):
        try:
            if x < -5:
                out.append(-0.7 * math.floor(x))
            elif x <= 18.5:
                out.append(-402.3)
            else:
                out.append(-16.8 * math.floor(x))
        except Exception:
            out.append(None)
    return {"y": out}

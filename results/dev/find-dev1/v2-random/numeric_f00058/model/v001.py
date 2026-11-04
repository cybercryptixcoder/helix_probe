def predict(probe):
    # Observations [E1]:
    # - For x in some central region, y is constant -84.3663 (looks like a floor/clamp).
    # - For large |x| (e.g. 66, 72.7, 88.2, -61.7), y is large positive ~ x^2-ish.
    #   Check: 88.2^2 = 7779, not 104398. 88.2^3 = 686k. Hmm.
    #   Try x^2 * something: 104398/7779 = 13.4. 66^2=4356, 21805/4356=5.0. Not consistent.
    #   Try exp? No, negative x gives positive y for -61.7 -> 34659.
    #   -61.7: 34659. 61.7^2=3807, ratio 9.1. 61.7^3=234k, no.
    #   Maybe x^2 * |x| / something? 88.2^3=686k, /6.57=104k. 66^3=287k/13.2=21805. No.
    #   Try a*x^2 + b*x + c? Fit three points.
    #   Points: (88.2,104398.3),(66,21806.0),(-61.7,34659.9),(72.7,44545.8)
    #   Let's fit quadratic through 88.2, 66, -61.7.
    #   Actually 72.7^2=5285, 44545/5285=8.43. 66^2 ratio 5.0. 88.2 ratio 13.4. Not x^2.
    #   Try x^3: 88.2^3=686128, ratio 0.152. 66^3=287496, ratio 0.0758. 72.7^3=384240, ratio 0.116. 61.7^3=234885, ratio 0.1476. Not consistent.
    #   Hmm, maybe it's a neural net approximating something. The constant -84.3663 in center.
    #   Let's guess: y = max(-84.3663, something). The "something" grows with |x|.
    #   Check 72.7 vs 66: 44545 vs 21806. Ratio 2.04 for x ratio 1.10. Exponent log(2.04)/log(1.10)=7.4. Steep.
    #   88.2 vs 72.7: 104398/44545=2.34, x ratio 1.213, exponent 4.5.
    #   Not a clean power. Could be exp-like: exp(88.2/k). 104398 -> ln=11.556. 66->ln(21806)=9.99. 
    #   Slope between: (11.556-9.99)/(88.2-66)=0.0705. For 72.7: ln(44545)=10.704. (10.704-9.99)/(72.7-66)=0.106. Not constant.
    #   This is hard. Best guess: quadratic-ish with floor.
    #   Try y = a*x^2 + b with floor -84.3663.
    #   (88.2,104398): a*7779+b=104398
    #   (66,21806): a*4356+b=21806
    #   Subtract: a*3423=82592 -> a=24.13, b=21806-4356*24.13=21806-105110=-83304. 
    #   Check 72.7: 24.13*5285-83304=127526-83304=44222 vs 44545. Close-ish!
    #   Check -61.7: 24.13*3807-83304=91863-83304=8559 vs 34659. Way off.
    #   So not symmetric. Negative side different.
    #   -61.7 -> 34659. If quadratic: a*3807+b=34659. With a=24.13,b=-83304 gives 8559. No.
    #   Maybe |x|^3? -61.7^3 magnitude 234885. 34659/234885=0.1476.
    #   88.2^3=686128, 104398/686128=0.1522. 66^3=287496, 21806/287496=0.0758. 72.7^3=384240, 44545/384240=0.1159.
    #   Not consistent either.
    #   Given MLP approximation, maybe it's something like x^2 for positive and something else negative.
    #   Actually check: 88.2^2=7779, 104398/7779=13.42. 72.7^2=5285, 44545/5285=8.43. 66^2=4356, 21806/4356=5.01.
    #   Ratios 13.42, 8.43, 5.01 for x=88.2,72.7,66. Roughly linear in x? 13.42/88.2=0.152, 8.43/72.7=0.116, 5.01/66=0.0759. Not linear.
    #   Hmm ratio ~ x^1.5? 88.2^1.5=828, 104398/828=126. No.
    #   I'll go with a rough quadratic fit for positive large x and separate for negative.
    #   Negative: only one point (-61.7,34659). Assume similar magnitude to positive at same |x|?
    #   At 61.7 positive would be ~24.13*3807-83304=8559. But observed 34659. So negative side is bigger.
    #   Maybe it's x^2 * something + floor. 
    #   Let's just do: y = max(-84.3663, k*x^2) with k fitted. 
    #   88.2: k=104398/7779=13.42. 66: k=5.01. Not constant.
    #   Try y = max(-84.3663, a*x^2+b*x+c) fit to 3 points (88.2,66,-61.7):
    #   a*7779+b*88.2+c=104398
    #   a*4356+b*66+c=21806
    #   a*3807+b*(-61.7)+c=34659
    #   Eq1-Eq2: a*3423+b*22.2=82592
    #   Eq1-Eq3: a*3972+b*149.9=69739
    #   From first: b=(82592-3423a)/22.2=3720.4-154.2a
    #   Sub: 3972a+149.9*(3720.4-154.2a)=69739
    #   3972a+557688-23115a=69739
    #   -19143a=-487949 -> a=25.49, b=3720.4-154.2*25.49=3720.4-3930.6=-210.2
    #   c=104398-25.49*7779-(-210.2)*88.2=104398-198287+18540=-75349
    #   Check 72.7: 25.49*5285-210.2*72.7-75349=134715-15281-75349=44085 vs 44545. Close!
    #   So quadratic fit works for positive side. For negative -61.7 it's forced by fit.
    #   But does it hold for other negatives? Unknown. Assume yes with floor.
    #   Floor: -84.3663. Where does quadratic cross -84.3663?
    #   25.49x^2-210.2x-75349=-84.3663 -> 25.49x^2-210.2x-75264.6=0
    #   x=(210.2±sqrt(44184+4*25.49*75264.6))/(2*25.49)
    #   = (210.2±sqrt(44184+7673972))/50.98=(210.2±sqrt(7718156))/50.98=(210.2±2778.2)/50.98
    #   Positive root: 2988.4/50.98=58.6. Negative root: -2568/50.98=-50.4.
    #   Hmm but -50.4 gave -84.3663 in E1! And -61.7 gave 34659. So crossing between -50.4 and -61.7. 
    #   Positive: 58.6. But 66 gave 21806, 72.7 gave 44545. 58.6 crossing means below 58.6 floor. 
    #   Check 66: 25.49*4356-210.2*66-75349=111034-13873-75349=21812. Yes matches 21806!
    #   So model: y = max(-84.3663, 25.49*x^2 - 210.2*x - 75349)
    #   Check x=2.9: 25.49*8.41-210.2*2.9-75349=214-610-75349=-75745 -> floor -84.3663. Matches!
    #   Check x=-20.3: 25.49*412-210.2*(-20.3)-75349=10502+4267-75349=-60580 -> floor. Matches!
    #   Check x=-24.3: 25.49*590+210.2*24.3-75349=15039+5108-75349=-55202 -> floor. Matches!
    #   Check x=-6.0: 25.49*36+1261-75349=918+1261-75349=-73170 -> floor. Matches!
    #   Check x=21.3: 25.49*454-210.2*21.3-75349=11572-4477-75349=-68254 -> floor. Matches!
    #   Check x=-50.4: 25.49*2540+210.2*50.4-75349=64745+10594-75349=-10 -> floor -84.3663. Matches!
    #   Check x=-61.7: 25.49*3807+210.2*61.7-75349=97040+12969-75349=34660. Matches 34659.94!
    #   Excellent! The model is y = max(-84.3663, 25.49*x^2 - 210.2*x - 75349)
    #   Let me refine coefficients using all points.
    #   Actually let me just use the fit. It's remarkably good.
    import math
    def f(x):
        try:
            v = 25.49*x*x - 210.2*x - 75349.0
            return max(-84.3663, v)
        except Exception:
            return None
    xs = probe.get("x", [])
    return {"y": [f(x) for x in xs]}

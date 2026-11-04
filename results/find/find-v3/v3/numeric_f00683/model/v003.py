import math

def predict(probe):
    # Model of the black box f(x).
    #
    # Beliefs (with evidence):
    # - Large positive x: f = 13.1*x - 3.5 [E1,E3,E5,E7,E9]. Slight drift but good.
    # - Small positive x (0,1): f = 15*x - 4.5 [E4].
    # - x == 0: special spike f(0) = -385.12 [E2].
    # - Negative side: NOT piecewise-linear with kink at -1. E10 shows values
    #   near -1 are around -9 to -11, NOT following 1.345*x-9.85 (which gives
    #   -11.2 at -1). E10: -0.9->-9.079, -0.8->-11.948, -1.2->-8.472,
    #   -1.4->-10.734, -1.8->-10.258. These are noisy around ~-10.
    #   E8: -2.2->-12.782, -2.8->-11.568, -3.2->-15.092, -3.8->-15.878,
    #   -4.2->-16.402, -4.8->-16.188, -5.2->-17.712, -5.8->-17.498,
    #   -6.2->-18.022, -6.8->-17.808, -7.2->-18.332, -7.8->-20.118,
    #   -8.5->-21.035, -9.0->-20.69, -10->-24.0, -10.5->-24.655,
    #   -12->-25.62, -15->-30.55, -20->-37.1, -25->-41.65.
    #   E6: -1.5->-11.865, -2->-12.52, -2.5->-14.175, -3.5->-15.485,
    #   -4->-14.14, -4.5->-15.795, -5.5->-16.105, -6.5->-18.415,
    #   -8->-21.38, -9.5->-22.345, -11->-25.31, -13->-27.93, -14->-28.24,
    #   -16->-29.86, -17->-31.17, -19->-31.79, -21->-38.41, -23->-41.03,
    #   -27->-45.27, -30->-50.2.
    #   Slope from -2 to -30: (-50.2+12.52)/(-28) = 1.345. Intercept ~ -9.8.
    #   But near -1 the values are ~-10, not -11.2. So there's a flattening
    #   near 0: the curve is concave (slope decreases as x->0-).
    #   Actually check: at -1.5, 1.345*-1.5-9.85=-11.87 matches E6 -11.865.
    #   At -1.2 E10 gives -8.472 (noisy, could be -11.5±noise? no, -8.5 is far).
    #   E10 -0.9->-9.079, -0.8->-11.948 (noisy). Mean near -1 ~ -10.
    #   Hmm, E4 -1->-11.21, -0.5->-9.555, -0.1->-8.031, -0.01->-7.9131.
    #   So as x->0-, f rises toward ~-7.9. There's a smooth curve.
    #   Let's fit a quadratic on negative side: f = a*x^2 + b*x + c.
    #   Use E4: -128->-178.58, -100->-141.9, -80->-114.7, -60->-89.5.
    #   Differences: slope between -128,-100: 36.68/28=1.31; -100,-80: 27.2/20=1.36;
    #   -80,-60: 25.2/20=1.26. Roughly linear slope ~1.3, so quadratic coeff small.
    #   Try f = 0.002*x^2 + 1.15*x - 8? At -128: 32.77-147.2-8=-122.4 no.
    #   Let's fit with points (-128,-178.58) and (-1,-11.21) and (-0.01,-7.9131).
    #   Actually the near-zero values: -0.5->-9.555, -0.1->-8.031, -0.01->-7.9131.
    #   Slope near 0: (-8.031+9.555)/0.4=3.81. So steep near 0, shallow far.
    #   That's concave down? No: slope 3.81 near 0, 1.3 far. Slope decreases as |x| grows.
    #   So f is concave (like sqrt or log). Try f = -7.9 + k*sqrt(|x|)?
    #   At -0.01: -7.9+k*0.1=-7.9131 -> k=-0.131. Hmm negative.
    #   Try f = c + b*x + a*x^2 with a>0 (concave up). Near 0 slope b, far slope b+2a*x.
    #   For x negative, slope = b+2a*x. At x=0 slope should be ~3.81 (from -0.5 to -0.1).
    #   At x=-100 slope ~1.3. So b+2a*(-100)=1.3, b=3.81 -> -200a=-2.51 -> a=0.01255.
    #   c: at x=-0.01, f=c+3.81*(-0.01)+0.01255*0.0001=c-0.0381=-7.9131 -> c=-7.875.
    #   Check x=-0.5: -7.875+3.81*(-0.5)+0.01255*0.25=-7.875-1.905+0.0031=-9.777 vs -9.555. Close.
    #   x=-1: -7.875-3.81+0.01255=-11.67 vs -11.21. Close-ish.
    #   x=-100: -7.875-381+125.5=-263.4 vs -141.9. WAY off. Quadratic too strong.
    #   So not quadratic. The slope near 0 is steep but far it's ~1.3 constant.
    #   Maybe piecewise: for x in (-1,0): steep linear; for x<=-1: shallow linear.
    #   E4 -1->-11.21, -0.5->-9.555: slope (-9.555+11.21)/0.5=3.31.
    #   -0.5 to -0.1: slope 3.81. -0.1 to -0.01: slope (-7.9131+8.031)/0.09=1.31.
    #   Hmm inconsistent. Noise is significant (~±1).
    #   Let's look at E10 more carefully (it's the latest, most relevant):
    #   -0.9->-9.079, -0.8->-11.948, -0.7->-9.817, -0.6->-9.686, -0.4->-10.424,
    #   -0.3->-9.293, -0.2->-10.162, -0.15->-10.0965, -0.05->-10.9655,
    #   -0.02->-10.9262, -0.005->-10.9065, -1.2->-8.472, -1.4->-10.734,
    #   -1.8->-10.258, -2.4->-13.044, -3.0->-11.83, -3.3->-13.223,
    #   -4.4->-15.664, -5.0->-17.45, -6.0->-17.76.
    #   These are noisy! -0.8->-11.948 but -0.7->-9.817. Noise ~±1.5.
    #   Mean near -0.5 is ~-10. Mean near -1 is ~-10. Mean near -2 is ~-11.5.
    #   Mean near -3 is ~-12.5. Mean near -5 is ~-17. 
    #   So it looks like f ~ -10 near 0, decreasing. Slope from -1 to -5: (-17+10)/4=1.75.
    #   From -5 to -30 (E6): (-50.2+17.76)/25=1.30.
    #   So slope ~1.3-1.75, roughly 1.35. Intercept: at x=-1, f~-10 -> -10 = 1.35*(-1)+c -> c=-8.65.
    #   At x=-0.5: 1.35*-0.5-8.65=-9.325 vs E4 -9.555. Good.
    #   At x=-0.1: -0.135-8.65=-8.785 vs -8.031. Off by 0.75.
    #   At x=-0.01: -0.0135-8.65=-8.66 vs -7.9131. Off by 0.75.
    #   Hmm near 0 it's higher (less negative). Maybe there's a small-x regime.
    #   But E10 near 0 (-0.05,-0.02,-0.005) gives ~-10.9, which is LOWER than -8.66.
    #   Contradicts E4! E4 -0.01->-7.9131 but E10 -0.005->-10.9065.
    #   These are inconsistent unless noisy. E10 noise seems large.
    #   Given noise, best fit: f = 1.35*x - 8.7 for x in [-30,0). 
    #   Check E4: -1->-10.05 vs -11.21 (off 1.16). -0.5->-9.375 vs -9.555 (ok).
    #   -0.1->-8.835 vs -8.031 (off 0.8). -0.01->-8.71 vs -7.9131 (off 0.8).
    #   E6: -1.5->-10.725 vs -11.865 (off 1.14). -2->-11.4 vs -12.52 (off 1.1).
    #   -30->-49.2 vs -50.2 (off 1). Consistent bias ~-1 for larger |x|.
    #   Maybe slope slightly higher: 1.38. -30: -41.4-8.7=-50.1 yes!
    #   -1: -1.38-8.7=-10.08 vs -11.21. Still off.
    #   Hmm. Let's use two segments: 
    #   x in [-30,-1]: f = 1.345*x - 9.85 (E6 fit, good for -1.5 to -30).
    #   x in (-1,0): f = 1.35*x - 8.7 (E4/E10 near 0).
    #   At x=-1: first gives -11.195, second gives -10.05. E4 says -11.21. So use first at -1.
    #   E10 -1.2->-8.472 (noisy, ignore). -1.4->-10.734 (first: -11.73, off 1).
    #   -1.8->-10.258 (first: -12.27, off 2). Hmm E10 is noisy.
    #   Let's just keep 1.345*x-9.85 for x<=-1 and use a flatter curve for -1<x<0.
    #   For -1<x<0: E4 -0.5->-9.555, -0.1->-8.031, -0.01->-7.9131.
    #   Fit: slope (-8.031+9.555)/0.4=3.81, but -0.01 is off. 
    #   Try f = 2*x - 8.5: -0.5->-9.5 (ok), -0.1->-8.7 (vs -8.031, off 0.67),
    #   -0.01->-8.52 (vs -7.9131, off 0.6). 
    #   Try f = 1.5*x - 8.7: -0.5->-9.45, -0.1->-8.85, -0.01->-8.715.
    #   E10 near 0: -0.05->-10.9655, -0.02->-10.9262, -0.005->-10.9065.
    #   These suggest f~-10.9 near 0, contradicting E4's -7.9. Noise is huge.
    #   Average E4 and E10 near 0: (-7.9 + -10.9)/2 = -9.4. 
    #   Use f = 1.5*x - 9.0 for -1<x<0: -0.5->-9.75, -0.1->-9.15, -0.01->-9.015.
    #   Compromise. 
    # - For x <= -30: E4 -35->-54.75, -45->-67.85, -60->-89.5, -80->-114.7,
    #   -100->-141.9, -128->-178.58. Slope ~1.33, intercept ~-8.2.
    #   Check -30: 1.33*-30-8.2=-48.1 vs E6 -50.2. Off 2. 
    #   Maybe same line 1.345*x-9.85 works: -128->-182 vs -178.58 (off 3.4).
    #   Use 1.33*x-8.5 for x<-30: -128->-178.74 yes! -100->-141.5 vs -141.9 ok.
    #   -60->-88.3 vs -89.5 ok. -35->-55.05 vs -54.75 ok.
    # - For x >= 1: f = 13.1*x - 3.5.
    # - For 0 < x < 1: f = 15*x - 4.5.
    # - x == 0: -385.12.

    try:
        xs = probe["x"]
        ys = []
        for x in xs:
            x = float(x)
            if x == 0.0:
                y = -385.12
            elif x < -30.0:
                y = 1.33 * x - 8.5
            elif x <= -1.0:
                y = 1.345 * x - 9.85
            elif x < 0.0:
                y = 1.5 * x - 9.0
            elif x < 1.0:
                y = 15.0 * x - 4.5
            else:
                y = 13.1 * x - 3.5
            ys.append(y)
        return {"y": ys}
    except Exception:
        return {"y": [None] * len(probe.get("x", []))}

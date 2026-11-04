def predict(probe):
    # f is approximately linear with slope ~4.76 [E1, E2, E3]
    # BUT there is a small nonlinearity near zero: the curve is slightly S-shaped
    #   f(0)≈3.9, f(1)≈8.9, f(-1)≈-0.24, f(0.5)≈6.59, f(-0.5)≈1.96 [E2, E4]
    #   Small-magnitude points deviate from 4.76*x: at x=0.5, 4.76x=2.38 but f=6.59;
    #   at x=-0.5, 4.76x=-2.38 but f=1.96. So there's a positive offset near 0.
    #   At |x|>=~10 the slope is very close to 4.76 with tiny offset [E2, E4]
    # Fit: use slope 4.76 with a smooth bump/offset near zero.
    #   From E4: residual (y - 4.76x): x=0.5:+4.2, 1.5:+4.15, 3:+4.07, 5:+3.98,
    #   8:+3.84, 12:+3.66, 15:+3.52, 25:+3.06, 35:+2.6, -0.5:+4.34, -1.5:+4.21,
    #   -3:+4.38, -5:+4.54, -8:+4.77, -12:+5.07, -15:+5.3, -25:+5.44, -35:+6.78
    #   Residual is roughly ~4-5 near zero, growing on negative side at large |x|.
    # Simpler: the slope is slightly less than 4.76 near zero and there's an offset.
    # Use a piecewise: for |x| small, add offset ~4; blend to 0 by |x|~? 
    # Actually residual stays ~4-5 out to 35. Check E2: x=10: 51.35-47.6=3.75;
    #   x=20: 98.49-95.2=3.29; x=40:192.77-190.4=2.37; x=60:287.06-285.6=1.46;
    #   x=80:381.34-380.8=0.54; x=100:475.62-476=-0.38; x=120:569.9-571.2=-1.3
    #   Negative: x=-10:-42.68+47.6=4.92; -20:-89.52+95.2=5.68; -40:-183.26+190.4=7.14;
    #   -60:-276.99+285.6=8.61; -80:-370.72+380.8=10.08; -100:-464.46+476=11.54;
    #   -120:-558.19+571.2=13.01
    # So residual ≈ 4 - 0.05*x roughly (linear in x!). i.e. f(x) ≈ 4.76x + 4 - 0.05x
    #   = 4.71x + 4. Check: x=0 -> 4 (obs 3.9 ok). x=120: 4.71*120+4=569.2 (obs 569.9 ok)
    #   x=-120: -565.2+4=-561.2 (obs -558.2, off by 3). x=100:475 (obs 475.6 ok).
    #   x=-100: -471+4=-467 (obs -464.5, off 2.5). Good enough.
    # So: f(x) ≈ 4.71*x + 4.  Slope 4.71, intercept 4.
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            ys.append(4.71 * x + 4.0)
        except Exception:
            ys.append(None)
    return {"y": ys}

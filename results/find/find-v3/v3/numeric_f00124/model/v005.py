def predict(probe):
    # Beliefs:
    # x>=0: y = 106.0528 + 111.4278*x [E2,E3,E4,E5,E7]
    # x<=-2: y = -25.4452 - 26.0717*x (linear tail) [E2,E6,E8]
    # -2<x<0: smooth curve with minimum near x=-1.05 (y~6.42).
    # E10 gives dense intermediate samples across the whole transition:
    #   -2.0:26.6982,-1.95:25.3946,-1.85:22.7875,-1.75:20.1803,-1.65:17.5731,
    #   -1.55:14.966,-1.45:12.3588,-1.35:10.1415,-1.25:8.2083,-1.15:6.8547,
    #   -1.05:6.4189,-1.0:6.8494,-0.95:8.2994,-0.9:10.6298,-0.85:14.0401,
    #   -0.8:18.223,-0.75:22.8773,-0.72:25.9521,-0.68:30.2818,-0.6:39.1961
    # Combined with E8 this is a smooth curve, not piecewise linear/quadratic.
    # The left branch (-2..-1.05) is nearly linear: slope ~ -22.5 (from -2 to -1.05
    #   drop 26.6982-6.4189=20.279 over 0.95 -> slope -21.35, slightly curving).
    # The right branch (-1.05..-0.6) accelerates from ~0 to +111 slope.
    # Use a single smooth quadratic through the transition, fit to E8+E10.
    # Fit y = a*x^2 + b*x + c on the transition points.
    # Using vertex form around x0=-1.05, y0=6.4189:
    #   at x=-2: 26.6982 -> a*(0.95)^2 = 20.279 -> a=22.47 (left)
    #   at x=-0.6: 39.1961 -> a*(0.45)^2 = 32.777 -> a=161.9 (right)
    # Asymmetric: steeper on right. Use separate quadratics per side of vertex.
    # Left (-2..-1.05): through (-2,26.6982),(-1.5,13.6624),(-1.05,6.4189)
    #   Fit quadratic. Points: (-2,26.6982),(-1.5,13.6624),(-1.05,6.4189)
    #   Let u=x+1.05. Points: u=-0.95:26.6982, u=-0.45:13.6624, u=0:6.4189
    #   c=6.4189. a*0.9025 - b*0.95 = 20.2793
    #         a*0.2025 - b*0.45 = 7.2435
    #   From 2nd: b = (a*0.2025 - 7.2435)/0.45 = 0.45a - 16.0967
    #   Sub: 0.9025a - 0.95*(0.45a-16.0967) = 20.2793
    #        0.9025a - 0.4275a + 15.2919 = 20.2793
    #        0.475a = 4.9874 -> a=10.499, b=0.45*10.499-16.0967=-11.372
    #   Check u=-0.95: 10.499*0.9025 +11.372*0.95... wait sign.
    #   y = a*u^2 + b*u + c with b=-11.372: at u=-0.95: 10.499*0.9025 + (-11.372)*(-0.95)+6.4189
    #     = 9.475 + 10.803 + 6.419 = 26.697 ✓
    #   at u=-0.45: 10.499*0.2025 + (-11.372)*(-0.45)+6.419 = 2.126+5.117+6.419=13.662 ✓
    # Right (-1.05..-0.6): through (-1.05,6.4189),(-0.85,14.0401),(-0.6,39.1961)
    #   u=x+1.05. u=0:6.4189, u=0.2:14.0401, u=0.45:39.1961
    #   c=6.4189. a*0.04 + b*0.2 = 7.6212
    #         a*0.2025 + b*0.45 = 32.7772
    #   From 1st: b=(7.6212-0.04a)/0.2 = 38.106 - 0.2a
    #   Sub: 0.2025a + 0.45*(38.106-0.2a)=32.7772
    #        0.2025a + 17.1477 - 0.09a = 32.7772
    #        0.1125a = 15.6295 -> a=138.93, b=38.106-27.786=10.320
    #   Check u=0.2: 138.93*0.04+10.320*0.2+6.419=5.557+2.064+6.419=14.040 ✓
    #   Check u=0.35 (x=-0.7): 138.93*0.1225+10.320*0.35+6.419=17.019+3.612+6.419=27.05
    #     vs obs 28.0616 (off 1.0). Slight curvature mismatch near seam.
    #   Check u=0.45: 138.93*0.2025+10.320*0.45+6.419=28.133+4.644+6.419=39.196 ✓
    # The right branch is slightly convex beyond quadratic; add small cubic? Keep quadratic.
    # For x in [-0.7,0]: line 106.0528+111.4278*x [E4,E8,E10]
    #   check -0.7: 28.0616 ✓, -0.68: 30.2818 ✓, -0.6: 39.1961 ✓
    def f(x):
        if x >= -0.7:
            return 106.0528 + 111.4278*x
        elif x > -1.05:
            u = x + 1.05
            return 138.93*u*u + 10.320*u + 6.4189
        elif x > -2:
            u = x + 1.05
            return 10.499*u*u - 11.372*u + 6.4189
        else:
            return -25.4452 - 26.0717*x
    return {"y": [f(x) for x in probe["x"]]}
